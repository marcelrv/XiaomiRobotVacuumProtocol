#!/usr/bin/env python3
"""Build data/bundles.json and data/commands.json from the raw extractor output.

usage: python build_commands.py --corpus <corpus dir with INDEX.json> --rpc <dir with <bundleId>.json> --out ../data

Inputs  : <corpus>/INDEX.json (unpack_plugins.py) and <rpc>/<bundleId>.json (js/extract_rpc.mjs)
Outputs : bundles.json   inventory of every unpacked bundle (best + regional variants) and code families
          commands.json  every RPC method string the plugin code can send, with per-bundle evidence

How a bundle names its RPC methods
  * The "Protocol" module holds `Methods` tables  (Key -> 'rpc_method_string').  Which table is active depends on
    the device model: models listed in `saphireModelList` get the alternate ("saphire"/"tanos") table, all others the
    default ("ruby") table.
  * Newer bundles also have a "RobotApi" module: one wrapper function per RPC call.
  * Other modules call RRMISDK.callMethod / asyncCallMethod / callMethodForceWay / ... directly.

Evidence per (bundle, method)
  table    method string is in the *active* Methods table of the bundle's own model
  inactive method string is only in a table that is not active for the bundle's own model
  ref      number of `Methods.<Key>` references outside the Protocol and RobotApi modules that are call arguments or
           otherwise used (not as a parameter value)
  param    number of references used as a *parameter value* of another call (e.g. get_prop ["get_status"])
  lit      number of call sites with the method string as literal outside the RobotApi module
  api      RobotApi wrapper function names (readable names only; minified aliases dropped)
  use      number of uses of those wrappers from other modules
  status   called   = ref / lit / use > 0     (the plugin contains a call site)
           wrapper  = wrapper exists but no use found
           parameter= only used as a parameter value of another call
           declared = only listed in the active Methods table
           inactive = only listed in a table that is not active for that model
  via      call routes seen: rpc (callMethod/asyncCallMethod), local (callMethodForceWay*), cloud (...FromCloud),
           map (getMapData / getAndDecBase64Data / downloadMap)
"""
import argparse
import collections
import datetime
import json
import os
import re
import sys


def load(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def iso(ms):
    try:
        return datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc).strftime('%Y-%m-%d')
    except Exception:  # noqa: BLE001
        return None


SAPHIRE_RX = re.compile(r"saphireModelList = \[([^\]]*)\]")
MINIFIED_ALIAS_RX = re.compile(r'^[A-Za-z$_]{1,2}$')


def saphire_models(corpus, model, hashdir):
    base = os.path.join(corpus, model, *(['variants', hashdir] if hashdir else []), 'android')
    mb = os.path.join(base, 'modules')
    texts = []
    if os.path.isdir(mb):
        for fn in os.listdir(mb):
            p = os.path.join(mb, fn)
            if os.path.getsize(p) > 20000:
                with open(p, encoding='utf-8', errors='replace') as fh:
                    t = fh.read()
                if 'roborock.sweeper.e2v3' in t:
                    texts.append(t)
    else:
        with open(os.path.join(base, 'main.bundle'), encoding='utf-8', errors='replace') as fh:
            texts.append(fh.read())
    for t in texts:
        m = SAPHIRE_RX.search(t)
        if m:
            return re.findall(r"'([^']+)'", m.group(1))
        m = re.search(r"-1!=\[([^\]]*roborock\.sweeper\.e2v3[^\]]*)\]\.indexOf", t)
        if m:
            return re.findall(r"'([^']+)'", m.group(1))
    return []


def route(callee):
    c = callee or ''
    if 'FromCloud' in c:
        return 'cloud'
    if 'ForceWay' in c:
        return 'local'
    if re.search(r'getMapData|getAndDecBase64Data|getRobotData|downloadMap', c):
        return 'map'
    return 'rpc'


def compact(s, n=60):      # code snippets in the data files stay short (module id + short anchor)
    return re.sub(r'\s+', ' ', s or '')[:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--corpus', required=True)
    ap.add_argument('--rpc', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    index = load(os.path.join(args.corpus, 'INDEX.json'))
    bundles = []
    for model, e in sorted(index.items()):
        for kind, info in [('best', e['best'])] + [('variant', v) for v in e.get('variants', [])]:
            if not info:
                continue
            h8 = info['hash'][:8]
            bid = model if kind == 'best' else f'{model}@{h8}'
            proj = info.get('project') or {}
            rpcf = os.path.join(args.rpc, bid + '.json')
            r = load(rpcf) if os.path.exists(rpcf) else {}
            bundles.append(dict(
                id=bid, model=model, kind=kind, file=re.sub(r'^[a-z]+\.[a-z]+\.[a-z0-9_]+-v\d-', '', info['file']), hash=info['hash'], regions=info.get('regions'),
                sdk_in_name=info.get('sdk_in_name'), build_in_name=info.get('build_in_name'),
                version=proj.get('version'), version_code=proj.get('version_code'),
                sdk_api_level=proj.get('sdk_api_level'), min_sdk_api_level=proj.get('min_sdk_api_level'),
                build_date_utc=iso(proj.get('build_time')), project_models_field=proj.get('models'),
                package_path=proj.get('package_path'), bundle_type=proj.get('bundle_type') or 'plain',
                minified=proj.get('bundle_minify'), format=info.get('format'),
                modules=r.get('modules') or info.get('modules'), main_bundle_md5=info.get('main_bundle_md5'),
                module_ids=r.get('ids'), has_robot_api=bool((r.get('ids') or {}).get('robotApi')),
                saphire_model_list=saphire_models(args.corpus, model, h8 if kind == 'variant' else None),
            ))
    fam = collections.defaultdict(list)
    for b in bundles:
        fam[b['main_bundle_md5']].append(b['id'])
    for b in bundles:
        b['identical_code_as'] = [m for m in fam[b['main_bundle_md5']] if m != b['id']]

    methods = {}

    def M(name):
        return methods.setdefault(name, dict(table_keys=collections.Counter(), wrapper_fns=set(), per_bundle={}, shapes=collections.OrderedDict(),
                                             guards=collections.Counter(), via=collections.Counter(), cloud_wrapper=False,
                                             reads=collections.defaultdict(set)))

    for b in bundles:
        r = load(os.path.join(args.rpc, b['id'] + '.json'))
        ids = r.get('ids') or {}
        proto = set(ids.get('protocol') or [])
        apimods = set(ids.get('robotApi') or [])
        helpers = apimods | set(ids.get('rrmisdk') or [])      # modules that only wrap RPCs (RobotApi, RRMISDK)
        roles = {}
        for t in r['tables']:
            ctx = t['ctx'] or {}
            name = ctx.get('name') or ctx.get('kind')
            if name in ('rubyMethods', 'cond-then'):
                roles['default'] = t['entries']
            elif name in ('saphireMethods', 'cond-else'):
                roles['saphire'] = t['entries']
            elif name == 'tanosMethods':
                roles['tanos'] = t['entries']
        alt = 'tanos' if 'tanos' in roles else 'saphire'
        in_alt = b['model'] in (b['saphire_model_list'] or [])
        active_role = alt if in_alt else 'default'
        active = roles.get(active_role, {})
        b['methods_table'] = dict(active_role=active_role, in_saphire_list=in_alt,
                                  table_sizes={k: len(v) for k, v in roles.items()},
                                  dead_tables=[k for k in roles if k != active_role])
        # ---- wrapper layer
        api_fn = collections.defaultdict(list)      # method -> [(fn, fromCloud)]
        api_route = collections.defaultdict(set)    # method -> routes of its wrapper definitions
        for fn, lst in (r.get('robotApi') or {}).items():
            for rec in lst:
                m = rec['method']
                name = m['value'] if m['kind'] == 'lit' else active.get(m['value'])
                if name:
                    api_fn[name].append((fn, bool(rec.get('fromCloud')), rec['args'][0] if rec['args'] else ''))
                    api_route[name].add(route(rec.get('callee')))
        uses = collections.Counter(u['fn'] for u in r.get('apiUses', []))
        refs = collections.Counter(x['key'] for x in r['methodsRefs'] if x['module'] not in proto and x['module'] not in helpers and x.get('ctx') == 'arg0')
        prefs = collections.Counter(x['key'] for x in r['methodsRefs'] if x['module'] not in proto and x.get('ctx') != 'arg0' and not (x['module'] in helpers and x.get('ctx') == 'other'))
        ref_mods = collections.defaultdict(set)
        for x in r['methodsRefs']:
            if x['module'] not in proto and x['module'] not in helpers and x.get('ctx') == 'arg0':
                ref_mods[x['key']].add(x['module'])
        use_mods = collections.defaultdict(set)
        for u in r.get('apiUses', []):
            use_mods[u['fn']].add(u['module'])
        lit_calls = collections.Counter()
        direct = collections.defaultdict(list)       # method -> call records (outside RobotApi)
        for c in r['rpcCalls']:
            if c['module'] in helpers:
                continue
            a0 = c['arg0']
            nm = a0['value'] if a0['kind'] == 'lit' else (active.get(a0['value']) if a0['kind'] == 'methods' else None)
            if not nm:
                continue
            if a0['kind'] == 'lit':
                lit_calls[nm] += 1
            direct[nm].append(c)
        # call sites grouped by owning function: reply reads are attributed to a method when it is the only method called in that function
        site_methods = collections.defaultdict(set)
        for nm2, lst in direct.items():
            for c in lst:
                site_methods[(c['module'], c.get('fnStart'))].add(nm2)
        fn_to_names = collections.defaultdict(set)
        for nm2, fl in api_fn.items():
            for f, _c, _a in fl:
                fn_to_names[f].add(nm2)
        for u in r.get('apiUses', []):
            for nm2 in fn_to_names.get(u['fn'], ()):
                site_methods[(u['module'], u.get('fnStart'))].add(nm2)
        inactive = set()
        for role, tab in roles.items():
            if role != active_role:
                inactive |= set(tab.values())
        names = set(active.values()) | set(lit_calls) | set(api_fn) | inactive
        for name in names:
            keys = sorted(k for k, v in active.items() if v == name)
            fns = sorted({f for f, _c, _a in api_fn.get(name, []) if not MINIFIED_ALIAS_RX.match(f)})
            allfns = {f for f, _c, _a in api_fn.get(name, [])}
            call_mods = {c['module'] for c in direct.get(name, [])}
            for k in keys:
                call_mods |= ref_mods[k]
            for f in allfns:
                call_mods |= use_mods[f]
            row = dict(table=name in active.values(), keys=keys, ref=sum(refs[k] for k in keys), param=sum(prefs[k] for k in keys), lit=lit_calls.get(name, 0),
                       api=fns, use=sum(uses[f] for f in allfns), modules=sorted(call_mods)[:8],
                       wrapper_modules=sorted(apimods) if allfns else [])
            if row['ref'] or row['lit'] or row['use']:
                row['status'] = 'called'
            elif allfns:
                row['status'] = 'wrapper'
            elif row['param']:
                row['status'] = 'parameter'
            elif row['table']:
                row['status'] = 'declared'
            else:
                row['status'] = 'inactive'
            rec = M(name)
            rec['per_bundle'][b['id']] = row
            if row['use']:
                for rt in api_route.get(name, ()):
                    rec['via'][rt] += 1
            for k in keys:
                rec['table_keys'][k] += 1
            rec['wrapper_fns'].update(fns)
            if any(c for _f, c, _a in api_fn.get(name, [])):
                rec['cloud_wrapper'] = True
            for f, _c, a in api_fn.get(name, []):
                s = compact(a)
                if s and s not in rec['shapes'] and len(rec['shapes']) < 10:
                    rec['shapes'][s] = (b['id'], 'wrapper')
            for c in direct.get(name, []):
                if len(site_methods.get((c['module'], c.get('fnStart')), ())) == 1:
                    for ch in c.get('reads') or []:
                        rec['reads'][ch].add(b['model'])
                rec['via'][route(c['callee'])] += 1
                s = compact(c['args'][0] if c['args'] else '')
                if s and s not in rec['shapes'] and len(rec['shapes']) < 10:
                    rec['shapes'][s] = (b['id'], 'call')
                for g in c['guards'][:3]:
                    rec['guards'][compact(g, 60)] += 1
        for u in r.get('apiUses', []):
            for name, fl in api_fn.items():
                if u['fn'] in {f for f, _c, _a in fl}:
                    s = compact(u['fn'] + '(' + ', '.join(u['args']) + ')')
                    rec = M(name)
                    if len(site_methods.get((u['module'], u.get('fnStart')), ())) == 1 and b['kind'] == 'best':
                        for ch in u.get('reads') or []:
                            rec['reads'][ch].add(b['model'])
                    if s not in rec['shapes'] and len(rec['shapes']) < 14 and not MINIFIED_ALIAS_RX.match(u['fn']):
                        rec['shapes'][s] = (b['id'], 'use')
                    for g in u['guards'][:3]:
                        rec['guards'][compact(g, 60)] += 1
    out_methods = {}
    for name, rec in sorted(methods.items()):
        pb = rec['per_bundle']
        best = lambda st: sorted(x for x in pb if pb[x]['status'] == st and '@' not in x)  # noqa: E731
        out_methods[name] = dict(
            method=name,
            user_prefixed=name.startswith('user.'),
            table_keys=dict(rec['table_keys']),
            wrapper_fns=sorted(rec['wrapper_fns']),
            cloud_wrapper=rec['cloud_wrapper'],
            via=dict(rec['via']),
            models_called=best('called'), models_wrapper_only=best('wrapper'), models_declared_only=best('declared'),
            models_parameter_only=best('parameter'), models_inactive_only=best('inactive'),
            variants_seen=sorted(x for x in pb if '@' in x),
            call_shapes=[dict(src=k, bundle=v[0], kind=v[1]) for k, v in rec['shapes'].items()],
            guards=[g for g, _n in rec['guards'].most_common(10)],
            reads=[[ch, len(ms)] for ch, ms in sorted(rec['reads'].items(), key=lambda kv: (-len(kv[1]), kv[0])) if ch != 'result'][:12],
            per_bundle=pb,
        )
    meta = dict(generator='tools/build_commands.py', bundles=len(bundles), best_bundles=sum(1 for b in bundles if b['kind'] == 'best'),
                methods=len(out_methods))
    with open(os.path.join(args.out, 'bundles.json'), 'w', encoding='utf-8') as fh:
        json.dump(dict(meta=meta, bundles=bundles), fh, indent=1, ensure_ascii=False)
    with open(os.path.join(args.out, 'commands.json'), 'w', encoding='utf-8') as fh:
        # compact: one method record per line (the file is large; per-bundle evidence dominates it)
        fh.write('{"meta": %s,\n"methods": {\n' % json.dumps(meta))
        fh.write(',\n'.join('%s: %s' % (json.dumps(k), json.dumps(v, ensure_ascii=False, separators=(',', ':'))) for k, v in out_methods.items()))
        fh.write('\n}}\n')
    print(meta)


if __name__ == '__main__':
    sys.exit(main())
