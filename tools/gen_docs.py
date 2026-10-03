#!/usr/bin/env python3
"""Generate the Markdown reference from data/*.json and the hand-written curated YAML in tools/curated/.

usage: python tools/gen_docs.py [--check]

Generated files (do not edit by hand; edit tools/curated/*.yaml or the data builders):
  docs/commands/index.md            every RPC method string with evidence, category and model coverage
  docs/commands/<category>.md       one page per category (curated text + data-derived evidence blocks)
  docs/commands/alternate-table.md  the `user.*` method table
  docs/devices/*.md, docs/reference/*.md (see gen_devices / gen_reference)
`--check` regenerates in memory and fails if any generated file differs from what is on disk.
"""
import argparse
import collections
import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import examples as EX  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
CUR = os.path.join(ROOT, 'tools', 'curated')
OUT = {}   # path (relative to ROOT, forward slashes) -> text


def load_json(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as fh:
        return json.load(fh)


def load_yaml(path):
    with open(path, encoding='utf-8') as fh:
        return yaml.safe_load(fh)


def short(bid):
    """roborock.vacuum.a65 -> a65 ; rockrobo.vacuum.v1 -> v1 ; a65@01cc8681 -> a65@01cc8681"""
    return bid.replace('roborock.vacuum.', '').replace('rockrobo.vacuum.', '')


def natkey(s):
    s = short(s)
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)]


def anchor_id(method):
    return method


def clip(t, n):
    t = ((t or '').strip().splitlines() or [''])[0]
    if len(t) <= n:
        return t
    cut = t[:n].rsplit(' ', 1)[0]
    return cut.rstrip(',;:') + '…'


def md_escape(t):
    return (t or '').replace('|', '\\|')


def nav(path_parts, title):
    """Breadcrumb line."""
    return ' / '.join(path_parts)


class Ctx:
    def __init__(self):
        self.bundles = load_json('bundles.json')['bundles']
        self.best = {b['model']: b for b in self.bundles if b['kind'] == 'best'}
        self.commands = load_json('commands.json')['methods']
        self.cats = load_yaml(os.path.join(CUR, 'categories.yaml'))['categories']
        self.cat_of = {}
        for c in self.cats:
            for m in c['methods']:
                self.cat_of[m] = c['id']
        self.all_models = sorted(self.best, key=natkey)
        self.curated = {}
        cdir = os.path.join(CUR, 'commands')
        if os.path.isdir(cdir):
            for fn in sorted(os.listdir(cdir)):
                if fn.endswith('.yaml'):
                    y = load_yaml(os.path.join(cdir, fn)) or {}
                    for item in y.get('commands', []):
                        if item['method'] in self.curated:
                            raise SystemExit('duplicate curated entry for %s' % item['method'])
                        self.curated[item['method']] = item
                        item['_file'] = fn

    def cmd_link(self, method, from_page=None):
        cat = self.cat_of.get(method)
        if cat is None:
            if method.startswith('user.'):
                return '[`%s`](alternate-table.md#%s)' % (method, anchor_id(method))
            return '`%s`' % method
        page = '%s.md' % cat
        return '[`%s`](%s#%s)' % (method, page, anchor_id(method))


def fmt_models(models, total):
    if len(models) == total:
        return 'all %d' % total
    return '%d: %s' % (len(models), ' '.join(short(m) for m in sorted(models, key=natkey)))


def availability(ctx, cmd):
    called = cmd['models_called']
    wrap = cmd['models_wrapper_only']
    decl = cmd['models_declared_only']
    inact = cmd['models_inactive_only']
    present = set(called) | set(wrap) | set(decl) | set(inact)
    absent = [m for m in ctx.all_models if ('roborock.vacuum.' + short(m) if False else m) not in present]
    return called, wrap, decl, inact, absent


def evidence_badge(cmd):
    n = len(cmd['models_called'])
    if n:
        return '✅ Bundle'
    if cmd['models_wrapper_only']:
        return '✅ Bundle (wrapper only)'
    if cmd['models_parameter_only']:
        return '✅ Bundle (parameter value only)'
    if cmd['models_declared_only']:
        return '✅ Bundle (declared only)'
    return '✅ Bundle (alternate table only)'


def transport_text(cmd):
    via = cmd.get('via', {})
    parts = []
    if cmd['cloud_wrapper'] or via.get('cloud'):
        parts.append('cloud route (`callMethodFromCloud`; inside Mi Home this is the same call as `callMethod`)')
    if via.get('local'):
        parts.append('forced local route (`callMethodForceWay` -> `callMethodFromLocal`)')
    if via.get('map'):
        parts.append('map download (`getMapData` -> RPC returning a file name, then HTTPS download; see [maps](../concepts/maps-overview.md))')
    if not parts or via.get('rpc') or cmd['wrapper_fns'] or cmd['models_called']:
        parts.insert(0, 'miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`)')
    return '; '.join(dict.fromkeys(parts))


def sources_block(ctx, cmd):
    rows = []
    pb = cmd['per_bundle']
    pick = []
    for st in ('called', 'wrapper', 'declared', 'inactive'):
        for bid in sorted((b for b in pb if '@' not in b and pb[b]['status'] == st), key=natkey, reverse=True):
            pick.append(bid)
        if pick:
            break
    # newest bundle first, then an old one for contrast
    pick = sorted(pick, key=lambda b: ctx.best[b]['sdk_api_level'] or 0, reverse=True)
    sel = pick[:2] + (pick[-1:] if len(pick) > 2 else [])
    for bid in dict.fromkeys(sel):
        row = pb[bid]
        b = ctx.best[bid]
        bits = []
        if row['wrapper_modules']:
            bits.append('wrapper m%s' % ','.join(str(x) for x in row['wrapper_modules']) + (' (`%s`)' % ', '.join(row['api']) if row['api'] else ''))
        if row['modules']:
            bits.append('call sites ' + ', '.join('m%d' % x for x in row['modules'][:5]))
        if row['keys']:
            bits.append('table key `%s`' % ', '.join(row['keys']))
        rows.append('- `%s@%s` · %s · anchor `"%s"`' % (short(bid), b['version'], '; '.join(bits) or 'Methods table', cmd['method'] if not row['keys'] else row['keys'][0]))
    return rows


def called_total(cmd):
    return bool(cmd['models_called'] or cmd['models_wrapper_only'])


def render_command(ctx, m):
    cmd = ctx.commands[m]
    cur = ctx.curated.get(m, {})
    if (cur.get('response') or '').strip().startswith('❓ Unknown') and cmd.get('reads'):
        cur = dict(cur, response=None)      # the code reads fields at the call site: use them instead of an unknown marker
    total = len(ctx.all_models)
    called, wrap, decl, inact, absent = availability(ctx, cmd)
    out = []
    title = cur.get('title') or ''
    out.append('<a id="%s"></a>' % anchor_id(m))
    out.append('### `%s`%s' % (m, (' — ' + title) if title else ''))
    out.append('')
    if cur.get('summary'):
        out.append(cur['summary'].strip())
        out.append('')
    out.append('| | |')
    out.append('|---|---|')
    out.append('| Evidence | %s — %s |' % (evidence_badge(cmd), 'called by the plugin of %s model(s)' % fmt_models(called, total) if called else (cur.get('evidence_note') or 'no call site found in the bundles')))
    extra = []
    if wrap:
        extra.append('wrapper only: %s' % fmt_models(wrap, total))
    if decl:
        extra.append('declared only: %s' % fmt_models(decl, total))
    if cmd['models_parameter_only']:
        extra.append('parameter value of another call only: %s' % fmt_models(cmd['models_parameter_only'], total))
    if inact:
        extra.append('alternate table only: %s' % fmt_models(inact, total))
    if extra:
        out.append('| Other bundles | %s |' % '; '.join(extra))
    out.append('| Transport | %s |' % transport_text(cmd))
    if cur.get('gating'):
        out.append('| Gating | %s |' % md_escape(cur['gating'].strip().replace('\n', ' ')))
    gate_names = sorted({n for t in (cmd.get('guards') or []) for n in re.findall(r'\b(is[A-Z]\w+)\(', t) if n not in ('isMiApp',)})
    if gate_names:
        out.append('| Call-site gate | the call sits behind %s (tests found in the enclosing code of the call sites; [feature flags](../concepts/feature-flags.md)) |' % ', '.join('`%s`' % n for n in gate_names))
    out.append('')
    for key, label in (('request', 'Request'), ('response', 'Response')):
        if cur.get(key):
            out.append('**%s**' % label)
            out.append('')
            out.append(cur[key].rstrip())
            out.append('')
    if not cur.get('response'):
        out.append('**Response**')
        out.append('')
        reads = cmd.get('reads') or []
        if reads:
            out.append('Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): '
                       + ', '.join('`%s` (%d)' % (ch, n) for ch, n in reads[:8]) + '. Types and units are not stated by the code unless a field is described elsewhere on this page.')
        elif cmd['models_called']:
            out.append('The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).')
        else:
            out.append('Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).')
        out.append('')
    if not cur.get('request') and cmd['call_shapes']:
        out.append('**Call shape in the app code** (as found; variable names are the plugin\'s)')
        out.append('')
        for s in cmd['call_shapes'][:4]:
            out.append('- `%s` (%s, %s)' % (s['src'].replace('`', "'")[:140], short(s['bundle']), s['kind']))
        out.append('')
    if not cur.get('examples') and called_total(cmd) and not m.startswith('user.'):
        params = EX.example_params(cur.get('request'), cmd['call_shapes'], m)
        if params is not None:
            out += ['**Example** — constructed from app code (typed sample values)', '', '```json', EX.example_json(m, params), '```', '']
    for ex in cur.get('examples', []) or []:
        out.append('**Example** — %s' % ex.get('label', 'constructed from app code'))
        out.append('')
        out.append('```json')
        out.append(ex['json'].rstrip())
        out.append('```')
        out.append('')
    if cur.get('behaviour'):
        out.append('**Behaviour in the app**')
        out.append('')
        out.append(cur['behaviour'].rstrip())
        out.append('')
    if cur.get('legacy'):
        out.append('**Legacy documentation**')
        out.append('')
        out.append(cur['legacy'].rstrip())
        out.append('')
    if cur.get('related'):
        out.append('**Related:** ' + ', '.join(ctx.cmd_link(r) for r in cur['related']))
        out.append('')
    out.append('<details><summary>Sources</summary>')
    out.append('')
    out.extend(sources_block(ctx, cmd))
    out.append('')
    out.append('</details>')
    out.append('')
    return '\n'.join(out)


def gen_commands(ctx):
    for cat in ctx.cats:
        parts = ['# %s' % cat['title'], '',
                 '[Home](../../README.md) / [Commands](index.md) / %s' % cat['title'], '',
                 cat['intro'].strip(), '']
        extra = ctx.curated.get('__category__' + cat['id'])
        cdir = os.path.join(CUR, 'commands', cat['id'] + '.yaml')
        if os.path.exists(cdir):
            y = load_yaml(cdir)
            if y.get('overview'):
                parts += [y['overview'].rstrip(), '']
        parts += ['## Commands in this category', '',
                  '| Method | Summary | Evidence |', '|---|---|---|']
        for m in cat['methods']:
            cur = ctx.curated.get(m, {})
            parts.append('| [`%s`](#%s) | %s | %s |' % (m, anchor_id(m), md_escape((cur.get('summary') or cur.get('title') or '').strip().split('\n')[0])[:110], evidence_badge(ctx.commands[m])))
        parts.append('')
        for m in cat['methods']:
            parts.append(render_command(ctx, m))
        parts += ['## See also', '', '- [Command index](index.md)', '- [Evidence legend](../../README.md#evidence-legend)', '']
        OUT['docs/commands/%s.md' % cat['id']] = '\n'.join(parts)


def gen_command_index(ctx):
    total = len(ctx.all_models)
    lines = ['# Command index', '',
             '[Home](../../README.md) / Commands', '',
             'Every RPC method string that the %d analysed Mi Home plugin bundles (one per model) can send to the robot, '
             'with the evidence found in the bundles. Generated from [`data/commands.json`](../../data/commands.json).' % total, '',
             '- **Called** = the plugin code contains a call site (directly, through a `Protocol.Methods.<Key>` reference or through a `RobotApi` wrapper that is used).',
             '- **Wrapper only / declared only** = the string is wrapped or listed but no call site was found.',
             '- A call site proves that the app *can send* the call; it does not prove that a particular firmware answers it. See [methodology](../methodology.md#what-a-bundle-does-and-does-not-prove).',
             '']
    for cat in ctx.cats:
        lines += ['## %s' % cat['title'], '', '| Method | Summary | Called by | Wrapper / declared only |', '|---|---|---|---|']
        for m in cat['methods']:
            cmd = ctx.commands[m]
            cur = ctx.curated.get(m, {})
            lines.append('| [`%s`](%s.md#%s) | %s | %s | %s |' % (
                m, cat['id'], anchor_id(m), md_escape(clip((cur.get('summary') or cur.get('title') or ''), 110)),
                'all %d' % total if len(cmd['models_called']) == total else str(len(cmd['models_called'])),
                ('%d / %d' % (len(cmd['models_wrapper_only']), len(cmd['models_declared_only']))) if (cmd['models_wrapper_only'] or cmd['models_declared_only']) else '—'))
        lines.append('')
    users = sorted(m for m in ctx.commands if m.startswith('user.'))
    lines += ['## Alternate (`user.*`) table', '',
              '%d method strings with the `user.` prefix exist in the bundles; see [alternate table](alternate-table.md).' % len(users), '']
    OUT['docs/commands/index.md'] = '\n'.join(lines)


def gen_alternate(ctx):
    users = sorted(m for m in ctx.commands if m.startswith('user.'))
    lines = ['# The `user.*` method table', '', '[Home](../../README.md) / [Commands](index.md) / Alternate table', '',
             'Every bundle contains a second `Methods` table in which most method strings carry the prefix `user.` '
             '(and two differ otherwise: `app_home` instead of `app_charge`, `app_get_status` instead of `get_status`). '
             'The plugin selects it when the device model is in `saphireModelList`. The list read from the bundles (20 of 42 carry a readable list; the others were not matched) names the Xiaowa / Sapphire robots: `roborock.vacuum.e2`, `roborock.sweeper.e2v2`, `roborock.sweeper.e2v3`, `roborock.vacuum.c1`, `roborock.sweeper.c1v2`, `roborock.sweeper.c1v3`, and in the a01-family bundles also `a01`, `a01v2`, `a01v3`, `a04`, `a04v2`, `a04v3`. In the bundles outside the a01 family that were read (for example s5 and a15) the selection is `modelType == \'rubys\' ? rubyMethods : saphireMethods`, so the `user.*` table is the table of that robot line. No analysed bundle is built for a model that activates it: the bundles of a01, c1 and e2 select a third table (`tanosMethods`) instead.', '']
    lines += ['<!-- evidence on selection logic is written in concepts/transports.md -->', '',
              '| Alternate method | Equivalent in default table | Active for a shipped bundle? |', '|---|---|---|']
    for m in users:
        base = m[len('user.'):]
        eq = {'user.app_home': 'app_charge', 'user.app_get_map': 'get_map / app_get_map', 'user.app_resume_zoned_clean': 'resume_zoned_clean'}.get(m, base)
        cmd = ctx.commands[m]
        act = 'yes (%s)' % ', '.join(short(x) for x in cmd['models_called']) if cmd['models_called'] else 'no'
        lines.append('<a id="%s"></a>\n| `%s` | %s | %s |' % (m, m, '`%s`' % eq, act) if False else '| <a id="%s"></a>`%s` | `%s` | %s |' % (m, m, eq, act))
    lines += ['', '## See also', '', '- [Transports and dispatch](../concepts/transports.md)', '']
    OUT['docs/commands/alternate-table.md'] = '\n'.join(lines)


def write_all(check=False):
    changed = []
    for rel, text in sorted(OUT.items()):
        p = os.path.join(ROOT, *rel.split('/'))
        if not text.endswith('\n'):
            text += '\n'
        old = None
        if os.path.exists(p):
            with open(p, encoding='utf-8', newline='') as fh:
                old = fh.read()
        if old != text:
            changed.append(rel)
            if not check:
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write(text)
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    ctx = Ctx()
    missing = sorted(m for m in ctx.commands if not m.startswith('user.') and m not in ctx.cat_of)
    if missing:
        raise SystemExit('methods without category: %s' % missing)
    gen_commands(ctx)
    gen_command_index(ctx)
    gen_alternate(ctx)
    me = sys.modules[__name__]
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    for modname in ('gen_reference', 'gen_devices', 'gen_maps', 'gen_concepts', 'gen_legacy', 'gen_cloud', 'gen_openhab'):
        try:
            mod = __import__(modname)
        except ModuleNotFoundError as exc:
            if exc.name != modname:
                raise
            continue
        mod.run(ctx, me)
    changed = write_all(args.check)
    print(('would change' if args.check else 'wrote'), len(changed), 'files; total generated', len(OUT))
    if args.check and changed:
        print('\n'.join(changed))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
