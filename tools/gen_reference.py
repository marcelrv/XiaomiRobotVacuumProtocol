"""Generated reference pages: states, errors, fan/water/mop values, other enumerations, status fields.
Called from gen_docs.py (`run(ctx, G)`); all numbers come from data/*.json, wording from tools/curated/*.yaml."""
import json
import os

import yaml

SRC = 'Generated from [`data/enums.json`](../../data/enums.json).'


def presence(G, ctx, models):
    models = sorted(set(models), key=G.natkey)
    total = len(ctx.all_models)
    if len(models) == total:
        return 'all %d' % total
    missing = [m for m in ctx.all_models if m not in models]
    if len(missing) <= 8:
        return 'all except ' + ' '.join(G.short(m) for m in missing)
    return '%d: %s' % (len(models), ' '.join(G.short(m) for m in models))


def newest(ctx, models):
    return max(models, key=lambda m: (ctx.best[m]['sdk_api_level'] or 0, ctx.best[m]['build_date_utc'] or ''))


def pick_latest(ctx, groups):
    """groups: list of (value, bundles); return (latest value, [other values])."""
    pool = [g for g in groups if g[0] not in (None, '', {})] or groups
    best = max(pool, key=lambda g: max((ctx.best[b]['sdk_api_level'] or 0, ctx.best[b]['build_date_utc'] or '') for b in g[1]))
    others = [g[0] for g in pool if g is not best]
    return best[0], others


def cell(t):
    if t is None:
        return '—'
    if isinstance(t, dict):
        if 'cond' in t:
            c = t['cond'].replace('_DeviceModelManager.DMM.', '').replace('_DeviceModelManager.', '')[:60].replace('`', "'")
            return 'if `%s`: %s; else: %s' % (c, cell(t['then']), cell(t['otherwise']))
        return str(t)
    return str(t).replace('|', '\\|').replace('\n', ' ')


def states_page(G, ctx, enums):
    L = ['# Robot state codes', '', '[Home](../../README.md) / Reference / State codes', '',
         'The `state` field of the status object ([status fields](status-fields.md)) and the app\'s own wording for each code. '
         'English strings are the plugin\'s own (`en_strings`); where several wordings occur the newest bundle is shown first. ' + SRC, '',
         '| Code | Origin | App constant | English wording (newest bundle) | Other wording | Present in |', '|---:|---|---|---|---|---|']
    for st in enums['states']:
        groups = [(n['text'], n['bundles']) for n in st['names']]
        latest, others = pick_latest(ctx, groups)
        allb = [b for n in st['names'] for b in n['bundles']]
        code = st['code']
        origin = 'computed' if code in (100, 103, 202) or code >= 6301 else 'display table only' if code in (101, 102) else '`state`'
        L.append('| %d | %s | `%s` | %s | %s | %s |' % (code, origin, st['constant'], cell(latest) or '—', cell('; '.join(o for o in others if o)) if any(others) else '', presence(G, ctx, allb)))
    L += ['', 'Origin: `state` = decoded from the status field `state`; computed = derived by the app from other fields (next section); display table only = an entry of the display map for which this analysis found no code path that assigns it (101 `OFF_LINE`, 102 `UNKNOW`, whose constant is not defined in the app\'s state enumeration). '
          'Codes 23 and 25 both map to the constant `WASHING_DUSTER`; the app uses different strings for them in different plugin generations.', '',
          '## Computed states', '',
          'Newer plugins do not show the raw firmware code for some situations; they compute a display state from several status '
          'fields (✅ Bundle · a65 m10010 `getComputedState`). These codes can therefore **not** be read from the `state` field:', '',
          '| Computed code | Condition |', '|---:|---|',
          '| 100 | `state == 8` (charging) and `battery == 100` |',
          '| 103 | `lock_status == 1` |',
          '| 202 | `state == 15` and `stop_fan_motor_work_status == 1` (stopping air-drying) |',
          '| 6 | `state == 15` otherwise (docking is shown as "returning to dock") |',
          '| 6310 | `state == 6` and `back_type == 1` (going to wash the mop) |',
          '| 6301 / 6302 / 6303 | `state == 5` with `clean_mop_status` 2 (mop only) / 7 / 6 |',
          '| 6304 / 6305 / 6306 | `state == 18` (room clean) with `clean_mop_status` 2 / 7 / 6 |',
          '| 6307 / 6308 / 6309 | `state == 17` (zone clean) with `clean_mop_status` 2 / 7 / 6 |', '',
          'A "wait for charge" label replaces the text of state 8 when valley-electricity charging is waiting '
          '(`charge_status == 0`).', '',
          '## Groupings used by the app', '',
          '| Predicate | States |', '|---|---|',
          '| cleaning | 5, 17, 18, 11 |',
          '| ready for a new clean | 2, 3, 10 or charging (8, 100) and no unfinished job |',
          '| resumable | 10, 2, 3, 12 or a back-to-dock task or charging |',
          '| on dock | 8, 100, 14, 22, 23 |',
          '| in a back-to-dock task | 6, 26, 22 or drying |', '',
          '(a65 m10010 `isCleaning`, `isReadyToNewClean`, `isReadyForCleanTaskResume`, `isOnDock`, `isInBackDockTask`.)', '',
          '## Differences from the legacy table', '',
          '⚪ Legacy [status.md](../../status.md) lists codes 0-18 and 100. Codes 0-3, 5-18 and 100 occur in the bundles\' display map (13 only in the 17 older bundles). '
          'Code 4 ("Remote Control" in the legacy table and in 🔶 openHAB) is **not** in the display map; the display map uses **7** for remote control '
          '(openHAB: 7 = "Manual Mode"). The app itself contains two disagreeing tables: its `RobotStateCode` constants list `REMOTE: 4` and `SEARCH_FOR_DOCK: 7` (a65 m12515), '
          'while the display map used for the status text maps 7 to the remote-control string. This looks like a renumbering inside the app; it does not prove that firmware never reports 4. '
          'The bundles add 22, 23, 25, 26, 28, 29, 30, 101, 102, 103, 202 and the computed 6301-6310.', '',
          '## See also', '', '- [Status fields](status-fields.md)', '- [Errors](errors.md)', '- [Status command](../commands/status.md)', '']
    G.OUT['docs/reference/states.md'] = '\n'.join(L)


def errors_page(G, ctx, enums):
    L = ['# Error codes', '', '[Home](../../README.md) / Reference / Error codes', '',
         'The `error_code` (or `dock_error_status`) of the status object and the plugin\'s own explanation. The *internal name* is the '
         'plugin\'s key for the entry (✅ Bundle · `Errors` table of the Main constants module). Titles are the app\'s English strings; '
         'the newest bundle is shown, other wordings are collapsed in the last column. ' + SRC, '',
         '| Code | Internal name | Title (newest) | Detail (newest) | Present in | Variants |', '|---:|---|---|---|---|---|']
    import re as _re

    def err_cell(t):
        c = cell(t)
        if c == '—':
            return c
        if _re.search(r'[\u4e00-\u9fff]', c):
            return '*(Chinese debug text, no English string)*'
        c = _re.sub(r'\{([A-Za-z0-9_]+)\}', lambda m: '*(no English string; key `%s`)*' % m.group(1), c)
        return c

    rows = []
    for e in enums['errors']:
        groups = [(json.dumps(x['entry'], sort_keys=True), x['bundles']) for x in e['entries']]
        latest_s, others = pick_latest(ctx, groups)
        latest = json.loads(latest_s)
        allb = [b for x in e['entries'] for b in x['bundles']]
        det = latest.get('detail') or latest.get('subtitle')
        rows.append(dict(code=e['code'], name=latest['name'], title=err_cell(latest.get('title')), det=err_cell(det), pres=presence(G, ctx, allb), var=len(others) or ''))
    # collapse runs of consecutive codes with identical content
    i = 0
    while i < len(rows):
        j = i
        while j + 1 < len(rows) and rows[j + 1]['code'] == rows[j]['code'] + 1 and all(rows[j + 1][k] == rows[i][k] for k in ('name', 'title', 'det', 'pres', 'var')):
            j += 1
        r = rows[i]
        code = str(r['code']) if j == i else '%d-%d' % (r['code'], rows[j]['code'])
        L.append('| %s | `%s` | %s | %s | %s | %s |' % (code, r['name'], r['title'], r['det'], r['pres'], r['var']))
        i = j + 1
    L += ['', '## Notes', '',
          '- Source tables: the `Errors` table of the main constants module in every bundle, and in the a01, c1 and e2 bundles additionally `ErrorsCodeToastMap`, which carries code 20 (`Mouse`).',
          '- A run of consecutive codes with identical content is shown as one row (for example 100-122).',
          '- The same internal name can carry different wording per product line; e.g. code 29 (`FindAItem`) reads "Unable to cross the carpet" for the product `TanosS` and "Suspected pet waste found" otherwise in the newest bundles, '
          'and an item-detection text in older ones. A text of the form `if ...: ...; else: ...` means the plugin chooses the string by product at run time.',
          '- Titles shown as *(no English string; key ...)* are keys that are missing from the bundle\'s English string table; entries shown as Chinese debug text exist only as Chinese test strings in the plugin (for example the image-frame error 30).',
          '- Codes 100-159 and 253-255 are mapped to generic "inner error" entries; the plugin shows a service-contact text for them.',
          '- Code 644 is the plugin\'s "bin full" entry (`Binfull`). Code 254 is an *inner error* entry ("Internal error") present only in the newer bundles, and 255 is also an inner error. '
          '⚪ Legacy listed 254 as "Bin full" (openHAB 🔶 does too).',
          '- Code 20 is **not** "Unknown Error" (⚪ Legacy / 🔶 openHAB wording): the a01, c1 and e2 bundles map it to `Mouse`, "Please clean the motion tracking sensor and place the robot back to its original location and start it."; no other bundle has an entry for 20.',
          '- ⚪ Legacy [status.md](../../status.md) lists codes 0-24, 254, 255 and -1. Codes above 25 in the table are new.', '']
    L += ['<a id="app-side-codes"></a>', '## App-side codes (not robot error codes)', '',
          'These numbers are produced by the plugin itself and never appear in `error_code`.', '']
    ve = enums.get('video_errors') or {}
    if ve:
        L += ['### Live-view (video) errors', '', '| Code | App name | English hint | Present in |', '|---:|---|---|---|']
        for name, rows in ve.items():
            groups = [(r['resolve'], r['bundles']) for r in rows]
            latest, _o = pick_latest(ctx, groups)
            L.append('| %s | `%s` | %s | %s |' % (rows[0]['code'], name, cell(latest), presence(G, ctx, [b for r in rows for b in r['bundles']])))
        L.append('')
    mo = enums.get('simple_enums', {}).get('mapOpErrorCode')
    if mo:
        L += ['### Map operation errors (`mapOpErrorCode`)', '', '| Name | Value | Present in |', '|---|---:|---|']
        for k, vv in mo['values'].items():
            L.append('| `%s` | %s | %s |' % (k, vv[0]['value'], presence(G, ctx, [b for v in vv for b in v['bundles']])))
        L.append('')
    L += ['Other plugin-level codes: `-10002` = access denied (the status poll treats it as "invalid connection"); `PluginNeedsUpdate` (−1) and '
          '`Unknown` (−999) for map fetch failures; `LoadMapDuplicated` (−100) and `DeviceNotAvaliable` (−101) in the multi-floor page.', '',
          '## See also', '', '- [Status fields](status-fields.md)', '- [States](states.md)', '']
    G.OUT['docs/reference/errors.md'] = '\n'.join(L)


def fan_page(G, ctx, enums):
    s = enums['simple_enums']
    L = ['# Fan power, water flow and mop mode values', '', '[Home](../../README.md) / Reference / Fan, water and mop', '',
         'Codes used by [`set_custom_mode`](../commands/cleaning-modes.md#set_custom_mode), '
         '[`set_water_box_custom_mode`](../commands/cleaning-modes.md#set_water_box_custom_mode), '
         '[`set_mop_mode`](../commands/cleaning-modes.md#set_mop_mode) and reported in the status fields `fan_power`, `water_box_mode`, `mop_mode`. ' + SRC, '',
         '<a id="fan-power"></a>', '## Fan power', '',
         'Three generations of codes occur. Which one a robot uses is not selected by a command; the plugin chooses its table by '
         'model (see [device pages](../devices/index.md)).', '',
         '| Generation | Code → app label | Evidence (bundles) |', '|---|---|---|']
    for name in ('CleanModeMap', 'CleanModeMapOld'):
        for row in enums['fan_tables'].get(name, []):
            t = {k: v for k, v in row['table'].items() if v}
            if not t:
                continue
            hi, lo = any(int(k) >= 101 for k in t), any(int(k) < 101 for k in t)
            label = 'both families (percentage-style and 101...)' if hi and lo else 'extended codes (101...)' if hi else 'percentage-style codes'
            codes = ', '.join('%s → %s' % (k, v) for k, v in sorted(t.items(), key=lambda kv: int(kv[0])))
            L.append('| %s (`%s`) | %s | %s |' % (label, name, codes, presence(G, ctx, row['bundles'])))
    for name in ('FanModel_sapphire', 'FanModel_sapphireCC', 'FanModel_sapphire_liteC_and_liteD'):
        for row in enums['fan_tables'].get(name, []):
            t = row['table']
            L.append('| Xiaowa/E-series table `%s` | %s | %s |' % (name, ', '.join('%s: %s' % (k, v) for k, v in t.items()), presence(G, ctx, row['bundles'])))
    csm = s.get('CleanSettingMode')
    if csm:
        L += ['', '### Picker presets (`CleanSettingMode`)', '', '| Preset | Code | Present in |', '|---|---:|---|']
        for k, vv in csm['values'].items():
            for v in vv:
                L.append('| %s | %s | %s |' % (k, v['value'], presence(G, ctx, v['bundles'])))
    L += ['', '<a id="water-box-mode"></a>', '## Water box mode', '', '| Table | Code → label | Present in |', '|---|---|---|']
    empty_wb = []
    for row in enums['fan_tables'].get('WaterBoxModeMap', []):
        t = {k: v for k, v in row['table'].items() if v}
        if not t:
            empty_wb += row['bundles']
            continue
        L.append('| `WaterBoxModeMap` | %s | %s |' % (', '.join('%s → %s' % (k, v) for k, v in sorted(t.items())), presence(G, ctx, row['bundles'])))
    if empty_wb:
        L.append('| `WaterBoxModeMap` (table present, no entries) | - | %s |' % presence(G, ctx, empty_wb))
    wsm = s.get('WaterSettingMode')
    if wsm:
        L += ['', '### Picker presets (`WaterSettingMode`)', '', '| Preset | Code | Present in |', '|---|---:|---|']
        for k, vv in wsm['values'].items():
            for v in vv:
                L.append('| %s | %s | %s |' % (k, v['value'], presence(G, ctx, v['bundles'])))
    L += ['', '<a id="mop-mode"></a>', '## Mop mode', '', '| Preset | Code | Present in |', '|---|---:|---|']
    for key in ('MopSettingMode', 'GarnetMopMode'):
        e = s.get(key)
        if e:
            for k, vv in e['values'].items():
                for v in vv:
                    L.append('| %s (`%s`) | %s | %s |' % (k, key, v['value'], presence(G, ctx, v['bundles'])))
    mc = s.get('ModeConstants')
    if mc:
        L += ['', '<a id="mode-constants"></a>', '## Mode code constants', '',
              'Named constants of the app (exported by its mode-setting module); they complete the tables above: `CustomCleanMode` is the "customize" fan code, `CustomWaterMode` the "customize" water code, `CustomMopMode` the "customize" mop code.', '',
              '| Constant | Code | Present in |', '|---|---:|---|']
        for k, vv in mc['values'].items():
            for v in vv:
                L.append('| `%s` | %s | %s |' % (k, v['value'], presence(G, ctx, v['bundles'])))
    L += ['', '## Notes', '',
          '- The legacy tables ⚪ ([custom_mode.md](../../custom_mode.md), [water_box_custom_mode.md](../../water_box_custom_mode.md)) are consistent with the bundles: '
          '101–106 extended fan codes, 200–204 and 207 water codes; new are fan code 108 (Max+), the mop "customize" code 302 and the route-mode codes 300, 301, 303, 304 and 305 ([mode code constants](#mode-constants)).',
          '- `105` is both "Gentle" in the fan table and the "mop only" marker (`NoClean`) used by the picker; the plugin treats a fan power of 105 as a pure-mop task.',
          '- Which codes a **firmware** accepts is not determinable from the bundles; the tables show what the app can display and send.', '',
          '## See also', '', '- [Cleaning modes commands](../commands/cleaning-modes.md)', '- [Status fields](status-fields.md)', '']
    G.OUT['docs/reference/fan-water-mop.md'] = '\n'.join(L)


def other_enums_page(G, ctx, enums):
    L = ['# Other enumerations decoded by the app', '', '[Home](../../README.md) / Reference / Other enumerations', '',
         'Small tables found in the bundles (located by their key set, so they are present even in minified bundles). ' + SRC, '']
    for name, e in sorted(enums['simple_enums'].items(), key=lambda kv: kv[0].lower()):
        if name in ('CleanSettingMode', 'WaterSettingMode', 'MopSettingMode', 'GarnetMopMode', 'mapOpErrorCode'):
            continue
        L += ['<a id="%s"></a>' % name.lower(), '## `%s`' % name, '', e['description'] + '.', '', '| Name | Value | Present in |', '|---|---|---|']
        for k, vv in e['values'].items():
            for v in vv:
                L.append('| `%s` | %s | %s |' % (k, v['value'], presence(G, ctx, v['bundles'])))
        L.append('')
    for name, rows in enums.get('code_maps', {}).items():
        L += ['<a id="%s"></a>' % name.lower(), '## `%s`' % name, '', '| Code | Meaning | Present in |', '|---:|---|---|']
        for k, vv in sorted(rows.items(), key=lambda kv: int(kv[0])):
            for v in vv:
                L.append('| %s | `%s` | %s |' % (k, v['value'], presence(G, ctx, v['bundles'])))
        L.append('')
    for name, rows in enums.get('clean_resume', {}).items():
        L += ['<a id="%s"></a>' % name.lower(), '## `%s` (value of `in_cleaning`)' % name, '', '| Code:meaning | Present in |', '|---|---|']
        for r in sorted(rows, key=lambda r: r['entry']):
            L.append('| `%s` | %s |' % (r['entry'], presence(G, ctx, r['bundles'])))
        L.append('')
    tt = enums.get('text_tables', {})
    for name, title in (('CleanStartType', 'Clean record start types (`start_type`)'), ('CleanFinishCleanReasons', 'Clean record finish reasons (`finish_reason`)'), ('obstacleNames', 'Obstacle types of map blocks 13–16 (type code → app name)')):
        if name in tt:
            L += ['<a id="%s"></a>' % name.lower(), '## %s' % title, '', 'App wording (English, newest bundle first).', '', '| Code | Text | Present in |', '|---:|---|---|']
            for k, rows in tt[name].items():
                groups = [(r['text'], r['bundles']) for r in rows]
                latest, _o = pick_latest(ctx, groups)
                L.append('| %s | %s | %s |' % (k, cell(latest), presence(G, ctx, [b for r in rows for b in r['bundles']])))
            L.append('')
    L += ['## See also', '', '- [Fan, water and mop values](fan-water-mop.md)', '- [States](states.md)', '']
    G.OUT['docs/reference/other-enums.md'] = '\n'.join(L)


def status_page(G, ctx):
    sf = json.load(open(os.path.join(G.DATA, 'status_fields.json'), encoding='utf-8'))['fields']
    cur = yaml.safe_load(open(os.path.join(G.CUR, 'status_fields.yaml'), encoding='utf-8'))
    total = len(ctx.all_models)
    L = ['# Status fields', '', '[Home](../../README.md) / Reference / Status fields', '',
         'The object returned as `result[0]` of `get_prop ["get_status"]` ([`get_prop`](../commands/status.md#get_prop)). The table lists the fields that '
         'the plugin\'s status parser reads, their interpretation (read from the app code) and in how many of the %d analysed bundles the parser '
         'reads them. A field that is not read by a bundle may still be sent by the robot. Presence columns are generated from '
         '[`data/status_fields.json`](../../data/status_fields.json); the interpretation is curated in `tools/curated/status_fields.yaml`.' % total, '']
    seen = set()
    for g in cur['groups']:
        L += ['## ' + g['title'], '', '| Field | Type | Meaning (from the app code) | Read by | Evidence |', '|---|---|---|---|---|']
        for f in g['fields']:
            seen.add(f['field'])
            n = len(sf.get(f['field'], {}).get('models', []))
            rb = f.get('read_by') or (('%d / %d' % (n, total)) if f['field'] in sf else 'not found by the extractor')
            anchor = '<a id="%s"></a>' % f['anchor'] if f.get('anchor') else ''
            L.append('| %s`%s` | %s | %s | %s | %s |' % (anchor, f['field'], f['type'], f['meaning'].replace('|', '\\|'), rb, f.get('evidence') or ''))
        L.append('')
    extra = sorted(set(sf) - seen)
    if extra:
        L += ['## Other fields read by the parser', '', '`' + '`, `'.join(extra) + '`', '']
    L += ['## Legacy-only fields', '', 'Fields documented by the pre-existing repo text that **no** bundle reads: ' +
          ', '.join('`%s`' % x['field'] for x in cur['legacy_only']) + '. They may still be returned by firmware; the bundles say nothing about them (⚪ Legacy).', '',
          '## Decoding notes', '',
          '- `map_status`: `value % 4` = 0 no map, 1 map without rooms, 3 map with rooms; `value >> 2` = saved-map id; id 63 is treated as "none".',
          '- Truthiness: the plugin often uses `!!status.x` or `== 1`; treat anything non-zero as on only where the table says so.',
          '- Units: `clean_area` mm², `clean_time` s, `battery` %. The `fan_power` code families are in [fan, water and mop values](fan-water-mop.md).', '',
          '## See also', '', '- [States](states.md)', '- [Errors](errors.md)', '- [Command: get_prop](../commands/status.md#get_prop)', '']
    G.OUT['docs/reference/status-fields.md'] = '\n'.join(L)


def consumables_page(G, ctx):
    data = G.load_json('consumables.json')['consumables']
    L = ['# Consumables: keys and nominal lives', '', '[Home](../../README.md) / [Reference](index.md) / Consumables', '',
         'The consumables the plugin shows on its supplies page, with the key of the [`get_consumable`](../commands/consumables.md#get_consumable) reply, '
         'the nominal life written in the plugin and the English name. Generated from [`data/consumables.json`](../../data/consumables.json) '
         '(`tools/js/extract_consumables.mjs`). The 22 RAM-bundle plugins with a `suppliesKey` table list all consumables; the 20 older plugins (a01 a08 a09 a10 a11 a14 a15 a19 a23 c1 e2 m1s p5 s4 s5 s5e s6 t4 t6 v1) use an older page layout with five time-based consumables whose lives are read from the layout by index.', '',
         '| Reply key | English name | Nominal life | Unit | Defined in |', '|---|---|---:|---|---|']
    for c in data:
        for v in c['variants']:
            life = '' if v['total'] is None else v['total']
            unit = {True: 'hours (time keys)', False: 'counts'}.get(v['units_time'], 'not stated (no life value)')
            L.append('| `%s` | %s | %s | %s | %s |' % (c['key'], v['name'], life, unit, presence(G, ctx, v['models'])))
    L += ['', 'The unit column follows the plugin\'s `isUnitsTime` flag: time keys are shown in hours (the app divides the reported seconds by 3600), the other keys count uses. '
          'The life of a consumable is the value the progress bar is drawn against; whether a robot enforces it is not shown by the bundles.', '',
          '## See also', '', '- [Consumable commands](../commands/consumables.md)', '- [Units](units.md)', '']
    G.OUT['docs/reference/consumables.md'] = '\n'.join(L)


def run(ctx, G):
    enums = G.load_json('enums.json')
    states_page(G, ctx, enums)
    errors_page(G, ctx, enums)
    fan_page(G, ctx, enums)
    other_enums_page(G, ctx, enums)
    status_page(G, ctx)
    consumables_page(G, ctx)
