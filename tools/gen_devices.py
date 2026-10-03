"""Generated device pages: docs/devices/<model>.md, index.md and the two matrices.
Called from gen_docs.py (`run(ctx, G)`). Sources: data/models.json, bundles.json, commands.json, feature_gates.json,
catalog_names.json, openhab_models.json, legacy_models.json and tools/curated/models.yaml (optional per-model notes)."""
import collections
import json
import os
import re

import yaml


def split_camel(n):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', n)


def rel(models, ctx, G):
    return ' '.join(G.short(m) for m in sorted(models, key=G.natkey))


def definition_text(d):
    bits = []
    if d['codes']:
        bits.append('fw code ' + ', '.join(str(c) for c in d['codes']))
    for b in d['bits']:
        if 'mask' in b:
            m = int(b['mask'], 16) if b['mask'].lower().startswith('0x') else int(b['mask'])
            idx = m.bit_length() - 1 if m and (m & (m - 1)) == 0 else None
            bits.append('%s bit %s' % ({'hi': 'high', 'lo': 'low', 'str': 'string'}[b['word']], idx if idx is not None else b['mask']))
        else:
            bits.append('%s bit %d' % ({'hi': 'high', 'lo': 'low', 'str': 'string'}[b['word']], b['bit']))
    if d['products']:
        bits.append('product: ' + ', '.join(d['products'][:6]) + ('…' if len(d['products']) > 6 else ''))
    if d['region']:
        bits.append('region')
    if d['userGate']:
        bits.append('account list')
    return '; '.join(bits)


def run(ctx, G):
    models = G.load_json('models.json')
    gates = G.load_json('feature_gates.json')
    cat = G.load_json('catalog_names.json')
    oh = G.load_json('openhab_models.json')
    notes_p = os.path.join(G.CUR, 'models.yaml')
    notes = (yaml.safe_load(open(notes_p, encoding='utf-8')) or {}).get('models', {}) if os.path.exists(notes_p) else {}
    bundled = models['bundled']
    cmds = ctx.commands
    cats = ctx.cats
    cat_methods = {c['id']: c['methods'] for c in cats}
    total = len(ctx.all_models)

    # code families = identical main.bundle among best bundles
    fam = collections.defaultdict(list)
    for m in ctx.all_models:
        fam[ctx.best[m]['main_bundle_md5']].append(m)
    fam_list = sorted(fam.values(), key=lambda g: G.natkey(g[0]))
    fam_id = {}
    for i, g in enumerate(fam_list, 1):
        for m in g:
            fam_id[m] = 'F%02d' % i

    def status_of(model, method):
        row = cmds[method]['per_bundle'].get(model)
        return row['status'] if row else None

    # ---------------------------------------------------------------- per-model pages
    for m in ctx.all_models:
        b = ctx.best[m]
        rec = bundled[m]
        s = G.short(m)
        variants = [x for x in ctx.bundles if x['model'] == m and x['kind'] == 'variant']
        ev = gates['evaluation'].get(m, {})
        preds = ev.get('predicates', {})
        L = ['# %s' % m, '', '[Home](../../README.md) / [Devices](index.md) / %s' % s, '']
        names = rec['names']
        cat_names = '; '.join('%s (%s)' % (x['name'], ', '.join(x['regions'])) for x in names.get('catalog', [])) or '—'
        L += ['| | |', '|---|---|',
              '| Model id | `%s` |' % m,
              '| Marketing name | %s — *Mi Home cloud device catalog* |' % cat_names,
              '| openHAB binding name | %s |' % (('%s — 🔶 openHAB' % names['openhab']) if names.get('openhab') else '—'),
              '| Legacy repo name | %s |' % (('%s — ⚪ Legacy' % names['legacy']) if names.get('legacy') else '—'),
              '| Plugin generation | %s |' % rec['generation'],
              '| Product code name (own bundle) | %s |' % (', '.join('`%s`' % x for x in rec['product_codenames']) or '—'),
              '| Product code name (newest bundle\'s model table) | %s |' % (('`%s` (series `%s`, from `%s`)' % (rec['product_in_newest_bundle']['product'], rec['product_in_newest_bundle']['series'], G.short(rec['product_in_newest_bundle']['bundle'])))
                                                                        if rec.get('product_in_newest_bundle') else '❓ Unknown (not listed)'),
              '| Revision-suffixed ids (`<model>v2` ... the plugin treats as the same model) | %s |' % (', '.join('`%s`' % a.replace('roborock.vacuum.', '') for a in rec['aliases']) or '—'),
              '| Other models in the same plugin series | %s |' % (', '.join('`%s`' % x.replace('roborock.vacuum.', '') for x in rec.get('series_members', [])) or '—'),
              '| Speaker volume range (plugin model table) | %s |' % (('%s-%s' % (rec['volume']['min'], rec['volume']['max'])) if rec.get('volume') else '❓ Unknown (no range in this plugin)'),
              '| Plugin version / SDK / build | %s / %s / %s |' % (b['version'], b['sdk_api_level'], b['build_date_utc']),
              '| Bundle file | `%s` |' % b['file'],
              '| Bundle format | %s, %s modules%s |' % (b['format'], b['modules'], ', minified' if b['minified'] else ''),
              '| Code family | `%s` — identical bundle code: %s |' % (fam_id[m], rel([x for x in fam[b['main_bundle_md5']] if x != m], ctx, G) or 'none (unique code)'),
              '| Regions with this build | %s |' % ', '.join(b['regions'] or []),
              '| `project.json` `models` field | `%s` (see [methodology](../methodology.md#metadata-quirks)) |' % b['project_models_field'] if b['project_models_field'] else '| `project.json` `models` field | absent |',
              '']
        if notes.get(s):
            L += ['## Notes', '', notes[s].strip(), '']
        # regional variants
        L += ['## Regional builds', '']
        if variants:
            L += ['Other bundles seen for this model (different zip hash):', '', '| Hash (8) | Regions | Plugin version | SDK | Build date | Method differences vs. the build above |', '|---|---|---|---|---|---|']
            for v in variants:
                diff = []
                for meth, c in cmds.items():
                    a = c['per_bundle'].get(m, {}).get('status')
                    bb = c['per_bundle'].get(v['id'], {}).get('status')
                    if a != bb:
                        diff.append('`%s` %s→%s' % (meth, a or '—', bb or '—'))
                L.append('| `%s` | %s | %s | %s | %s | %s |' % (v['hash'][:8], ', '.join(v['regions'] or []), v['version'], v['sdk_api_level'], v['build_date_utc'],
                                                          ('; '.join(diff[:8]) + ('; …+%d' % (len(diff) - 8) if len(diff) > 8 else '')) if diff else 'none'))
            L.append('')
        else:
            L += ['One bundle hash in all regions where this model was found (%s): no regional differences.' % ', '.join(b['regions'] or []), '']
        # commands
        L += ['## Commands the plugin can send', '',
              'Counts of method strings per category: **called** (call site found) / wrapper-only or declared-only / not present. '
              'Details per command are in the [command reference](../commands/index.md).', '',
              '| Category | Called | Wrapper / declared only | Not present | App gates for the category (class for this model) |', '|---|---:|---:|---:|---|']
        tc = tw = 0
        gated_off = []
        for c in cats:
            called = [x for x in c['methods'] if status_of(m, x) == 'called']
            wd = [x for x in c['methods'] if status_of(m, x) in ('wrapper', 'declared', 'parameter')]
            none = [x for x in c['methods'] if status_of(m, x) is None]
            tc += len(called)
            tw += len(wd)
            gl = [(x, preds[x]['cls']) for x in c.get('gates', []) if x in preds]
            gtxt = ', '.join('`%s`: %s' % (x, cl) for x, cl in gl)
            if gl and called and all(cl in ('N', 'RA') for _x, cl in gl):
                gtxt += ' — **all gates off**'
                gated_off.append(c['title'])
            L.append('| [%s](../commands/%s.md) | %d | %d | %d | %s |' % (c['title'], c['id'], len(called), len(wd), len(none), gtxt))
        L += ['| **Total** | **%d** | **%d** | | |' % (tc, tw), '']
        L += ['"App gates" are the `FeatureManager` predicates that the app pages for the category test, evaluated for this model ([classes](#feature-gates-featuremanager-predicates)). '
              'A category whose gates all evaluate `N` or `RA` is present in the shared plugin code but never opened by its UI gates for this model (evaluation, not a robot test): %s.' % (', '.join(gated_off) if gated_off else 'none for this model'), '']
        L += ['<details><summary>All called method strings</summary>', '']
        for c in cats:
            called = [x for x in c['methods'] if status_of(m, x) == 'called']
            if called:
                L.append('- **%s**: %s' % (c['title'], ', '.join(G_link(ctx, x) for x in called)))
        L += ['', '</details>', '']
        # gating
        grouped = collections.defaultdict(list)
        for p, v in preds.items():
            grouped[v['cls']].append(p)
        L += ['## Feature gates (FeatureManager predicates)', '',
              'Result of executing the plugin\'s own `FeatureManager` for this model id under six runtime situations '
              '(location cn/us/de × firmware flags none/all), with the plugin running inside Mi Home (`isMiApp = true`; a second pass with `false` finds the Roborock-app-only gates). Method: [feature flags](../concepts/feature-flags.md#how-the-gates-were-evaluated). '
              'Classes (letter used in the [feature matrix](matrix-features.md)): `Y` (Y) enabled regardless of firmware; `FW` (F) enabled only if the robot reports the firmware flag; '
              '`REG` (R) depends on the robot location; `RT` (r) depends on app runtime state; `N` (-) never enabled in the scenarios; `INV` (i) enabled only while the robot does not report the flag; `RA` (a) off inside Mi Home, on in the Roborock app (the predicate tests `!isMiApp`); '
              '`ERR` (e) the predicate threw in the sandbox.', '']
        order = ['Y', 'FW', 'REG', 'RT', 'INV', 'RA', 'ERR', '?', 'N']
        L += ['| Class | Count | Predicates |', '|---|---:|---|']
        for cl in order:
            if grouped.get(cl):
                names_ = sorted(grouped[cl])
                shown = ', '.join('`%s`' % x for x in names_)
                L.append('| %s | %d | %s |' % (cl, len(names_), shown))
        L.append('')
        # status fields
        sf = G.load_json('status_fields.json')['fields']
        n_sf = sum(1 for f, v in sf.items() if m in v['models'])
        L += ['## Status parser', '', 'The status parser of this bundle reads %d distinct status fields (of %d seen across bundles): see [status fields](../reference/status-fields.md).' % (n_sf, len(sf)), '']
        # methods table
        mt = b['methods_table']
        L += ['## Method table selection', '',
              'Active `Methods` table: `%s`%s. Table sizes in the bundle: %s. %s' % (
                  mt['active_role'], ' (the model id is in `saphireModelList`)' if mt['in_saphire_list'] else '',
                  ', '.join('%s %d' % (k, v) for k, v in mt['table_sizes'].items()),
                  'Tables not selected for this model: %s.' % ', '.join(mt['dead_tables']) if mt['dead_tables'] else ''), '']
        L += ['## See also', '', '- [Devices index](index.md)', '- [Feature matrix](matrix-features.md)', '- [Command matrix](matrix-commands.md)', '- [Methodology](../methodology.md)', '']
        G.OUT['docs/devices/%s.md' % s] = '\n'.join(L)

    # ---------------------------------------------------------------- index
    I = ['# Devices', '', '[Home](../../README.md) / Devices', '',
         'All %d Roborock/Rockrobo vacuum models for which a Mi Home plugin bundle was analysed. One page per model; the pages are generated from '
         '[`data/models.json`](../../data/models.json). Names are tagged by source: **Mi Home cloud device catalog** (per region), 🔶 openHAB binding, ⚪ legacy repo text.' % total, '',
         '| Model | Name (catalog) | Plugin | Generation | Product code name | Code family | Regions |', '|---|---|---|---|---|---|---|']
    for m in ctx.all_models:
        rec = bundled[m]
        b = ctx.best[m]
        nm = ' / '.join(sorted({x['name'] for x in rec['names'].get('catalog', [])})) or (rec['names'].get('openhab') or rec['names'].get('legacy') or '—')
        prod = (rec['product_codenames'] or [rec.get('product_in_newest_bundle', {}).get('product', '—')])[0]
        I.append('| [`%s`](%s.md) | %s | %s | %s | `%s` | %s | %s |' % (G.short(m), G.short(m), nm, b['version'], rec['generation'][0], prod, fam_id[m], ','.join(b['regions'] or [])))
    I += ['', '"Generation": **A** = older plugin without a `DeviceModelManager` and without the retry protocol, **B** = newer plugin with a `DeviceModelManager` (product table) and the retry protocol — see [model generations](../concepts/model-generations.md).', '',
          '## Code families', '',
          'Bundles with byte-identical `main.bundle` run the same code; differences between such models can only come from model gating inside the code.', '',
          '| Family | Models | Plugin version |', '|---|---|---|']
    for g in fam_list:
        I.append('| %s | %s | %s |' % (fam_id[g[0]], rel(g, ctx, G), ctx.best[g[0]]['version']))
    I += ['', '## Not bundled / unverified', '', 'Models known only from the Mi Home catalog, the openHAB binding or the bundles\' model tables (no plugin of their own): see [appendix](../appendix/unverified-models.md).', '',
          '## See also', '', '- [Feature matrix](matrix-features.md)', '- [Command matrix](matrix-commands.md)', '- [Methodology](../methodology.md)', '']
    G.OUT['docs/devices/index.md'] = '\n'.join(I)

    # ---------------------------------------------------------------- command matrix
    M = ['# Command matrix', '', '[Home](../../README.md) / [Devices](index.md) / Command matrix', '',
         'Generated from [`data/commands.json`](../../data/commands.json). `●` = call site found in the model\'s plugin, `○` = wrapper-only, parameter-only or declared-only, blank = the method string is not present in that bundle. '
         'Columns are the code families of the [devices index](index.md#code-families) (models of one family run identical code).', '',
         '## Called methods per model and category', '', '| Model | ' + ' | '.join('[%s](../commands/%s.md)' % (c['id'], c['id']) for c in cats) + ' |', '|---|' + '---:|' * len(cats)]
    for m in ctx.all_models:
        M.append('| [%s](%s.md) | ' % (G.short(m), G.short(m)) + ' | '.join(str(sum(1 for x in c['methods'] if status_of(m, x) == 'called')) for c in cats) + ' |')
    M += ['', '(Category sizes: ' + ', '.join('%s %d' % (c['id'], len(c['methods'])) for c in cats) + '.)', '']
    reps = [g[0] for g in fam_list]
    for c in cats:
        M += ['## %s' % c['title'], '', '| Method | ' + ' | '.join('%s' % fam_id[r] for r in reps) + ' |', '|---|' + ':-:|' * len(reps)]
        for x in c['methods']:
            cells_ = []
            for r in reps:
                st = status_of(r, x)
                cells_.append('●' if st == 'called' else '○' if st in ('wrapper', 'declared', 'parameter') else '')
            M.append('| %s | ' % G_link(ctx, x) + ' | '.join(cells_) + ' |')
        M.append('')
    M += ['## Family key', '', '| Family | Models |', '|---|---|'] + ['| %s | %s |' % (fam_id[g[0]], rel(g, ctx, G)) for g in fam_list] + ['']
    G.OUT['docs/devices/matrix-commands.md'] = '\n'.join(M)

    # ---------------------------------------------------------------- feature matrix
    newest_defs = {}
    for p, defs in gates['predicates'].items():
        best_def = max(defs, key=lambda d: max((ctx.best[x.split('@')[0]]['sdk_api_level'] or 0) if x.split('@')[0] in ctx.best else 0 for x in d['bundles']))
        newest_defs[p] = best_def['definition']
    F = ['# Feature matrix', '', '[Home](../../README.md) / [Devices](index.md) / Feature matrix', '',
         'Result of executing every `FeatureManager` predicate of each model\'s own plugin for that model id '
         '([method](../concepts/feature-flags.md#how-the-gates-were-evaluated)). Cells: `Y` enabled for the product, `F` product allows it but the robot must report the firmware flag, '
         '`R` depends on location, `r` depends on app runtime state, `-` never enabled, `i` enabled only while the robot does not report the flag, `a` off in Mi Home but on in the Roborock app, `e` the predicate threw in the sandbox, blank = predicate not present in that plugin version. '
         'Generated from [`data/feature_gates.json`](../../data/feature_gates.json).', '']
    cellmap = {'Y': 'Y', 'FW': 'F', 'REG': 'R', 'RT': 'r', 'ERR': 'e', 'INV': 'i', 'RA': 'a', '?': '?', 'N': '-'}
    for genlabel, gens in (('B (newer plugins)', 'dmm'), ('A (older plugins)', 'groups')):
        cols = [m for m in ctx.all_models if gates['evaluation'].get(m, {}).get('generation') == gens]
        names_ = sorted({p for m in cols for p in gates['evaluation'][m]['predicates']})
        # hide predicates that are '-' everywhere
        names_ = [p for p in names_ if any(gates['evaluation'][m]['predicates'].get(p, {}).get('cls', 'N') != 'N' for m in cols)]
        F += ['## Generation %s' % genlabel, '', '| Predicate | Definition (newest bundle) | ' + ' | '.join(G.short(m) for m in cols) + ' |', '|---|---|' + ':-:|' * len(cols)]
        for p in names_:
            row = []
            for m in cols:
                v = gates['evaluation'][m]['predicates'].get(p)
                row.append(cellmap[v['cls']] if v else '')
            d = newest_defs.get(p)
            F.append('| `%s` | %s | ' % (p, definition_text(d).replace('|', '\\|') if d else '') + ' | '.join(row) + ' |')
        F.append('')
    G.OUT['docs/devices/matrix-features.md'] = '\n'.join(F)


def G_link(ctx, method):
    cat = ctx.cat_of.get(method)
    if cat is None:
        return '`%s`' % method
    return '[`%s`](../commands/%s.md#%s)' % (method, cat, method)
