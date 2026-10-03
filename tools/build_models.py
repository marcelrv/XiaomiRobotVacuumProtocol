#!/usr/bin/env python3
"""Build data/models.json and data/feature_gates.json.

usage: python build_models.py --work <dir with feat/ and fdefs/> --data ../data

Inputs  (data/):  bundles.json, catalog_names.json, openhab_models.json, legacy_models.json
        (work/):  feat/<bundleId>.json   FeatureManager evaluation (js/eval_features.mjs)
                  fdefs/<bundleId>.json  FeatureManager predicate definitions (js/extract_feature_defs.mjs)
Outputs (data/):  models.json          one record per bundled model (+ catalog / openHAB-only models)
                  feature_gates.json   predicate definitions + per-model evaluation + fw feature code usage

Evaluation classes for one predicate and one model (6 scenarios: location cn/us/de x firmware flags none/all)
  Y   true in every scenario                       (gated by product only, or not gated)
  N   false in every scenario                      (this product is excluded by the code)
  FW  false without firmware flags, true with them (product allows it, the robot's feature list/bit mask decides)
  REG depends on the robot's location (cn/us/de), see `raw`
  RT  result depends on runtime state the evaluator cannot know (touched app state), see `rt`
  ERR the predicate threw
  ?   anything else (see raw)
"""
import argparse
import collections
import json
import os
import re
import sys

SCEN = ['cn/none', 'cn/all', 'us/none', 'us/all', 'de/none', 'de/all']


def load(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def classify(rs):
    if rs and rs[0].get('ra'):
        return 'RA'          # off inside Mi Home, on in the Roborock app (tests !isMiApp)
    if any(r.get('err') for r in rs):
        return 'ERR'
    if any(r.get('rt') for r in rs):
        return 'RT'
    v = [bool(r['v']) for r in rs]
    if all(v):
        return 'Y'
    if not any(v):
        return 'N'
    none, full = v[0::2], v[1::2]
    if not any(none) and all(full):
        return 'FW'
    if all(none) and not any(full):
        return 'INV'          # true only while the robot does NOT report the firmware flag
    if (v[0], v[1]) == (v[2], v[3]) == (v[4], v[5]):
        return '?'
    return 'REG'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--data', required=True)
    args = ap.parse_args()
    D = args.data
    bundles = load(os.path.join(D, 'bundles.json'))['bundles']
    cat = load(os.path.join(D, 'catalog_names.json'))
    oh = load(os.path.join(D, 'openhab_models.json'))
    legacy = load(os.path.join(D, 'legacy_models.json'))
    best = {b['model']: b for b in bundles if b['kind'] == 'best'}

    # ---- feature gates
    gates = dict(meta=dict(generator='tools/build_models.py', scenarios=SCEN,
                           classes={'Y': 'true in every scenario', 'N': 'false in every scenario', 'FW': 'needs firmware flag (product allows)',
                                    'REG': 'depends on robot location', 'RT': 'depends on runtime app state', 'ERR': 'predicate threw', '?': 'other'}),
                 predicates={}, evaluation={}, fw_code_uses={}, new_feature_bits={})
    products = {}
    for b in bundles:
        fp = os.path.join(args.work, 'fdefs', b['id'] + '.json')
        if not os.path.exists(fp):
            continue
        fd = load(fp)
        for name, d in fd['methods'].items():
            pr = gates['predicates'].setdefault(name, {})
            key = json.dumps({k: d[k] for k in ('codes', 'bits', 'products', 'region', 'userGate', 'calls')}, sort_keys=True)
            pr.setdefault(key, []).append(b['id'])
        if b['kind'] == 'best':
            for u in fd.get('uses', []):
                gates['fw_code_uses'].setdefault(str(u['code']), {}).setdefault(b['id'], []).append(dict(fn=u['fn'], ctx=(u['ctx'] or '')[:60]))
    gates['predicates'] = {n: [dict(definition=json.loads(k), bundles=bs) for k, bs in v.items()] for n, v in sorted(gates['predicates'].items())}
    # bit -> predicate map from the newest bundle that defines it
    for n, defs in gates['predicates'].items():
        for d in defs:
            for bit in d['definition']['bits']:
                if 'mask' in bit:
                    mval = int(bit['mask'], 16) if bit['mask'].lower().startswith('0x') else int(bit['mask'])
                    idx = mval.bit_length() - 1 if mval and (mval & (mval - 1)) == 0 else None
                else:
                    idx = bit['bit']
                label = '%s:bit%s' % (bit['word'], idx) if idx is not None else '%s:mask%s' % (bit['word'], bit['mask'])
                gates['new_feature_bits'].setdefault(label, {})[n] = len([x for x in d['bundles'] if '@' not in x])

    # DeviceModelManager table of the newest bundle: product code name for every model id it lists (cross-reference for older bundles)
    newest = None
    for b in bundles:
        if b['kind'] == 'best' and b['has_robot_api']:
            if newest is None or (b['sdk_api_level'] or 0) > (newest['sdk_api_level'] or 0):
                newest = b
    ev_new = load(os.path.join(args.work, 'feat', newest['id'] + '.json')) if newest else None
    dmm_models = {}
    if ev_new and ev_new.get('deviceInfo'):
        for sname, s in ev_new['deviceInfo']['series'].items():
            for m in s['models']:
                dmm_models[m] = dict(series=sname, product=s['product'])
    models = {}
    for model, b in sorted(best.items()):
        fp = os.path.join(args.work, 'feat', b['id'] + '.json')
        ev = load(fp) if os.path.exists(fp) else None
        rec = dict(id=model, bundle=b['id'], generation=None, product_codenames=[], series=None, aliases=[], family=[],
                   names={}, project=dict(version=b['version'], sdk_api_level=b['sdk_api_level'], build_date_utc=b['build_date_utc'], regions=b['regions'], file=b['file'], hash=b['hash']),
                   identical_code_as=b['identical_code_as'])
        if ev:
            rec['generation'] = 'B (DeviceModelManager)' if ev['generation'] == 'dmm' else 'A (model groups)'
            res = ev['results'].get(model, {})
            if ev.get('deviceInfo'):
                for sname, s in ev['deviceInfo']['series'].items():
                    if model in s['models']:
                        rec['product_codenames'] = [s['product']]
                        rec['series'] = sname
                        rec['aliases'] = [m for m in s['models'] if re.fullmatch(re.escape(model) + r'v\d', m)]
                        rec['series_members'] = [m for m in s['models'] if m != model and m not in rec['aliases']]
                        rec['volume'] = s.get('volume')
            elif ev.get('groups'):
                rec['product_codenames'] = sorted(re.sub(r'^is', '', g) for g, ms in ev['groups'].items() if model in ms)
            ge = {}
            for pname, rs in res.get('methods', {}).items():
                ge[pname] = dict(cls=classify(rs), raw=''.join('T' if r.get('v') is True else 'F' if r.get('v') is False else 'E' for r in rs))
                rt = sorted({x for r in rs for x in (r.get('rt') or [])})
                if rt:
                    ge[pname]['rt'] = rt[:4]
            gates['evaluation'][model] = dict(bundle=b['id'], generation=ev['generation'], predicates=ge)
        # names with source tags
        names = {}
        crec = cat['models'].get(model)
        if crec:
            by = collections.defaultdict(list)
            for region, x in crec.items():
                by[x.get('name')].append(region)
            names['catalog'] = [dict(name=n, regions=sorted(r)) for n, r in by.items()]
        if model in oh['models']:
            names['openhab'] = oh['models'][model]['name']
        if model in legacy['models']:
            lg = legacy['models'][model]
            names['legacy'] = lg.get('readme_name') or lg.get('fw_features_name')
        rec['names'] = names
        if model in dmm_models:
            rec['product_in_newest_bundle'] = dict(dmm_models[model], bundle=newest['id'])
        models[model] = rec
    # models known only through catalog / openHAB / DeviceModelManager tables
    other = {}
    all_ids = set(cat['models']) | set(oh['models']) | set(legacy['models'])
    alias_rx = re.compile(r'^(.*[^.])v([2-9])$')   # roborock.vacuum.a09v2 is a hardware revision alias of a09

    def is_alias(m):
        mm = alias_rx.match(m)
        return bool(mm) and not m.endswith('.v1') and mm.group(1) not in ('roborock.vacuum.', 'roborock.sweeper.') and not m.endswith('.v2')

    for m in sorted(all_ids | {x for x in dmm_models if not is_alias(x)}):
        if m in models or is_alias(m) and m not in all_ids:
            continue
        o = dict(id=m, bundle=None)
        if m in cat['models']:
            o['catalog'] = {r: x.get('name') for r, x in cat['models'][m].items()}
        if m in oh['models']:
            o['openhab'] = oh['models'][m]
        if m in legacy['models']:
            o['legacy'] = legacy['models'][m]
        if m in dmm_models:
            o['deviceModelManager'] = dict(dmm_models[m], bundle=newest['id'])
        other[m] = o
    out = dict(meta=dict(generator='tools/build_models.py', bundled_models=len(models), other_models=len(other),
                         deviceModelManager_source=newest['id'] if newest else None), bundled=models, other=other)
    with open(os.path.join(D, 'models.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(D, 'feature_gates.json'), 'w', encoding='utf-8') as fh:
        json.dump(gates, fh, indent=1, ensure_ascii=False)
    print('models', len(models), 'other', len(other), 'predicates', len(gates['predicates']))


if __name__ == '__main__':
    sys.exit(main())
