"""Generated concept page: docs/concepts/feature-flags.md (the three feature words and the FeatureManager gates).
Called from gen_docs.py (`run(ctx, G)`). Sources: data/feature_gates.json, tools/curated/legacy_fw_features.yaml."""
import collections
import os

import yaml

FW_MEANING = {
    103: 'clean-time feature (`isCleanTimeSupported`)',
    111: 'FDS endpoint (`isSupportFDSEndPoint`)',
    112: 'automatic splitting of rooms (`isSupportAutoSplitSegments`)',
    113: 'delete-map button of the saved-map list when multi-floor is off (`showDeleteButton`, inside the map-list `render`)',
    114: 'cleaning rooms in a chosen order (`isSupportOrderSegmentClean`)',
    116: 'room (segment) support (`isMapSegmentSupported`); consulted only for the products `RubyPlus` and `RubySC`, every other product returns true without it',
    118: 'custom clean mode synchronisation (`syncCustomMode`, `resetCleanMode`, `customModeDidChange`, `handleModeTabDidChange`, `updateCustomMode`)',
    119: 'LED switch (`isSupportLedStatusSwitch`, `isLedSwitchVisible`)',
    120: 'multi-floor maps (`isMultiFloorSupported`)',
    122: 'timer summary (`isSupportFetchTimerSummary`, `fetchListDataFromRobot`); not used for the product `Tanos_CN`',
    123: 'order clean (`isOrderCleanSupported`)',
    124: 'analysis page (`isAnalysisSupported`)',
    125: 'remote control (`isRemoteSupported`)',
    130: 'voice-control debug entry (`isSupportVoiceCtrolDebug`)',
}


def run(ctx, G):
    f = G.load_json('feature_gates.json')
    models = G.load_json('models.json')
    nbundled = len(ctx.all_models)
    preds = f['predicates']
    ev = f['evaluation']
    cls = collections.Counter()
    for m, e in ev.items():
        if '@' in m:
            continue
        for p, v in e['predicates'].items():
            cls[v['cls']] += 1
    fw_uses = f['fw_code_uses']
    # bit tables
    lo, hi, st = {}, {}, {}
    for label, names in f['new_feature_bits'].items():
        word, b = label.split(':')
        n = int(b[3:]) if b.startswith('bit') else None
        if n is None:
            continue
        {'lo': lo, 'hi': hi, 'str': st}[word][n] = names
    str_bundles = set()
    for n, defs in preds.items():
        for d in defs:
            if any(b['word'] == 'str' for b in d['definition']['bits']):
                str_bundles.update(x.split('@')[0] for x in d['bundles'])
    str_models = sorted(str_bundles, key=G.natkey)
    legacy = yaml.safe_load(open(os.path.join(G.CUR, 'legacy_fw_features.yaml'), encoding='utf-8'))['captures']

    L = ['# Feature flags and capability gates', '',
         '[Home](../../README.md) / Concepts / Feature flags', '',
         'The Mi Home plugin decides which controls to show from three kinds of information: **what the robot reports** '
         '(firmware feature codes and two feature words), **what the product is** (model id mapped to a product code name) and '
         '**where the robot is** (location). This page lists the three robot-reported sets with the app code that reads them, and explains how the '
         'per-model gate tables in [devices](../devices/index.md) were obtained. Because the gates live in the plugin, this is the closest '
         'evidence the bundles give for "model X offers feature Y" (see [what a bundle does and does not prove](../methodology.md#what-a-bundle-does-and-does-not-prove)).', '',
         '## Where the robot reports its features', '',
         '| Source | Used by | Shape |', '|---|---|---|',
         '| [`get_fw_features`](../commands/status.md#get_fw_features) | called by %s | `result` = array of feature codes |' % ' '.join(G.short(m) for m in sorted(ctx.commands['get_fw_features']['models_called'], key=G.natkey)),
         '| [`app_get_init_status`](../commands/status.md#app_get_init_status) `result[0].feature_info` | called by %d bundles (wrapped only in %s) | array of feature codes (`101`…`130`) |' % (len(ctx.commands['app_get_init_status']['models_called']), ' '.join(G.short(m) for m in sorted(ctx.commands['app_get_init_status']['models_wrapper_only'], key=G.natkey))),
         '| `result[0].new_feature_info` | `FeatureManager` | one number; the app tests bits of the low 32-bit word with `&` and bits of the high word with `/ 2^32 >> n & 1` |',
         '| `result[0].new_feature_info_str` | `FeatureManager` of %d bundles (%s) | string of hex digits, length a multiple of 8; the app parses digit groups with `parseInt("0x" + str.slice(...))` |' % (len(str_models), ' '.join(G.short(m) for m in str_models)),
         '| `result[0].local_info.location` | `FeatureManager` | `prc` is rewritten to `cn`; compared with `cn` / `us` / `de` |',
         '| `result[0].local_info.featureset` | `RobotStatusManager` | bit 0 = "FCC state" (`isFCC`, `isFCCOrCE`) |', '',
         'All of this is ✅ Bundle (a65 m10007 `fetchDeviceLocation`, m10037 `FeatureManager`; the other bundles were extracted by script). '
         'Which codes or bits a particular robot **sets** is not in the bundles; the only evidence is the user-contributed captures in [legacy captures](#legacy-captures).', '',
         '<a id="feature-codes"></a>',
         '## Firmware feature codes (`feature_info`)', '',
         '`FeatureManager.isSupportFeature(code)` is true when the code is in the array. These are all codes that any bundle tests with a literal number; '
         'a code that is not in the table is not tested by any of the %d bundles.' % nbundled, '',
         '| Code | Gates (bundle code) | Bundles testing it | Legacy list |', '|---:|---|---:|---|']
    legacy_txt = {103: 'Clean Time Supported', 111: 'Supports FSEndPoint', 112: 'Supports AutoSplitSegments', 113: 'Supportrs Delete Map feature',
                  114: 'Supports OrderSegmentClean', 115: 'Spot Clean', 116: 'Map Segment Supported', 119: 'Supports Led Status Switch', 120: 'Multi Floor Supported',
                  122: 'Supports FetchTimer Summary', 123: 'Orders Clean Supported', 124: 'Analysis Supported', 125: 'Remote Supported'}
    for code in sorted(int(c) for c in fw_uses):
        n = len({m.split('@')[0] for m in fw_uses[str(code)]})
        L.append('| %d | %s | %d | %s |' % (code, FW_MEANING.get(code, '(`%s`)' % ', '.join(sorted({u['fn'] or '?' for us in fw_uses[str(code)].values() for u in us}))), n, legacy_txt.get(code, '')))
    others = [c for c in range(101, 131) if str(c) not in fw_uses]
    L += ['', 'Codes without a literal test in any bundle: %s. The legacy list names `115` ("Spot Clean") and has no name for the others (the legacy captures below report codes such as 117 and 121 for real robots, so the app tests do not cover every code robots send); '
          'the bundles neither confirm nor contradict `115`.' % ', '.join(str(c) for c in others), '',
          '⚪ Legacy named the codes `103`, `111`-`116`, `119`, `120` and `122`-`125`. The bundles test all of them except `115`; `113` is confirmed as the delete-map button. The bundles additionally test `118` and `130`, which the legacy list leaves blank.', '']

    def bit_table(title, anchor, table, intro):
        out = ['<a id="%s"></a>' % anchor, '## %s' % title, '', intro, '', '| Bit | Predicate in the plugin (number of bundles defining it) |', '|---:|---|']
        for b in sorted(table):
            names = table[b]
            out.append('| %d | %s |' % (b, ', '.join('`%s` (%d)' % (n, c) for n, c in sorted(names.items()))))
        return out + ['']

    L += bit_table('Feature word 1: `new_feature_info`, low word', 'new_feature_info', lo,
                   'Tested as `robotNewFeatures & mask` (✅ Bundle · a65 m10037). The same bit has different predicate names in different bundles when the code differs by generation; both names are listed.')
    L += bit_table('Feature word 1: `new_feature_info`, high word', 'new_feature_info-high', hi,
                   'Tested as `robotNewFeatures / Math.pow(2, 32) >> n & 1`; bit numbers are within the high word (bit 0 = 2^32 of the number).')
    L += bit_table('Feature word 2: `new_feature_info_str`', 'feature-word-new_feature_info_str', st,
                   'Hex string read from its right end: bit 0 is the lowest bit of the last hex digit. `slice(-8)` covers bits 0-31 (the predicates mask the 32-bit value); the digits before it carry bits 32-35 (`slice(-9, -8)`), 36-39 (`slice(-10, -9)`) and 40-43 (`slice(-11, -10)`). '
                   'Each predicate additionally requires a non-empty string whose length is a multiple of 8 (most of them). Present in the code of %d bundles (%s); '
                   'older generations never read the string. The relation between `new_feature_info` and `new_feature_info_str` (whether the string repeats the number) is ❓ Unknown: the bundles use them independently and assign different meanings to the same bit number. '
                   '`isSupportIncrementalMap` is a special case: low-word bit 13 of the string in Mi Home, but bit 22 in the Roborock app (`RRMISDK.isMiApp` branch).' % (len(str_models), ' '.join(G.short(m) for m in str_models)))

    L += ['## Other gates in `FeatureManager`', '',
          '- **Product** (`DMM.currentProduct`, `RRMISDK.isTanosS()` and similar): the model id is looked up in the plugin\'s `DeviceModelManager` / model-group tables, which return a product code name; '
          'see the product column of [devices](../devices/index.md) and [model generations](model-generations.md).',
          '- **Region**: `deviceLocation` (`cn`, `us`, `de`, …) and `isFCC` / `isCE` / `isOversea`.',
          '- **Account lists**: some predicates test the Mi Home account id against lists baked into the plugin (`userGate` in `data/feature_gates.json`). The lists themselves are deliberately not reproduced here; '
          'such predicates are classified as runtime-dependent.',
          '- **Runtime state**: the app version, the Mi Home account, debug flags, device status fields.', '',
          '<a id="how-the-gates-were-evaluated"></a>',
          '## How the gates were evaluated', '',
          'For every bundle the script `tools/js/eval_features.mjs` loads the plugin\'s own `FeatureManager` and `DeviceModelManager` (or model-group) modules into a Node `vm` context '
          'in which every other module is an inert stub, sets the device model id, and binds `isMiApp = true` (the plugin runs inside Mi Home; a second pass with `false` marks the Roborock-app-only gates), evaluates the model-group helpers of the older plugins (`isTanosV()`, `isSapphire()`, ... each a list of model ids) for the device model, and calls each zero-argument predicate under six scenarios: location `cn`, `us`, `de` × firmware reports **nothing** (empty code list, `new_feature_info = 0`, empty string) or **everything** '
          '(codes 101-140, all bits set, string of `f`). Results are classified:', '',
          '| Class | Meaning | Count over the %d bundled models (predicate × model) |' % nbundled, '|---|---|---:|']
    desc = {'Y': 'true in every scenario (no firmware or region dependence)', 'FW': 'false without the robot reporting the flag, true with it (the product allows the feature)',
            'REG': 'depends on the location (the flag may or may not also be needed)', 'RT': 'touches runtime state of the app (version, account, debug flags) that the sandbox cannot supply',
            'N': 'false in every scenario (product excluded, or an input the sandbox does not provide)', 'ERR': 'the predicate threw (usually a missing runtime input)', 'INV': 'true only while the robot does not report the flag (inverse firmware dependence)', 'RA': 'false in Mi Home but true when `isMiApp` is false: the gate belongs to the Roborock app (for example the live-view monitor of the older plugins)'}
    for k in ('Y', 'FW', 'REG', 'RT', 'INV', 'RA', 'N', 'ERR'):
        L.append('| `%s` | %s | %d |' % (k, desc[k], cls.get(k, 0)))
    L += ['', 'What this proves: the plugin shows the feature for this model id when the robot reports the flag. What it does not prove: that the robot reports the flag; that a firmware answers the underlying RPC. '
          '`N` can also mean "needs an input the sandbox lacks", so an `N` is evidence of "never enabled by the app in these scenarios", not of "robot cannot do it". '
          'Generated tables: [feature matrix](../devices/matrix-features.md) and the per-model pages. Raw results: [`data/feature_gates.json`](../../data/feature_gates.json).', '',
          '<a id="legacy-captures"></a>',
          '## Legacy captures', '',
          '⚪ Legacy: `get_fw_features` / `feature_info` lists that users posted for real robots (firmware as written in the legacy page). Unverified; the bundles contain no robot data.', '',
          '| Model | Name (legacy) | Firmware | Codes reported |', '|---|---|---|---|']
    for c in legacy:
        L.append('| `%s` | %s | %s | %s |' % (G.short(c['model']), c['name'], '❓ not stated' if c['firmware'] == '?' else c['firmware'], ', '.join(str(x) for x in c['codes'])))
    L += ['', 'Observations that can be checked against the code tables above: the capture of the old `v1` (`101, 102, 104, 105`) contains codes that no bundle tests; the S5 capture contains `102`, `103`, `104`, `105`, '
          'of which only `103` is tested by a bundle.', '',
          '## See also', '', '- [Feature matrix](../devices/matrix-features.md)', '- [`app_get_init_status`](../commands/status.md#app_get_init_status)',
          '- [Model generations](model-generations.md)', '- [Methodology](../methodology.md)', '']
    G.OUT['docs/concepts/feature-flags.md'] = '\n'.join(L)
    gen_generations(ctx, G)
    gen_methodology(ctx, G)
    gen_unverified(ctx, G)
    gen_readme(ctx, G)


def gen_generations(ctx, G):
    mods = G.load_json('models.json')['bundled']
    mods = mods if isinstance(mods, list) else list(mods.values())
    bundles = {b['model']: b for b in ctx.bundles if b['kind'] == 'best'}
    gen = collections.defaultdict(list)
    prod = collections.defaultdict(list)
    ver = collections.defaultdict(list)
    for m in mods:
        gen[m['generation'][0]].append(m['id'])
        pn = m['product_codenames'][0] if m['product_codenames'] else (m.get('product_in_newest_bundle') or {}).get('product')
        own = bool(m['product_codenames'])
        prod[(pn or '?')].append((m['id'], own))
        ver[m['project']['version']].append(m)
    L = ['# Model generations and families', '',
         '[Home](../../README.md) / Concepts / Model generations', '',
         'The plugins of the %d analysed models come in two code generations and three file formats. Models that share a plugin share its code, '
         'so the differences between them are decided by the gates described in [feature flags](feature-flags.md).' % len(mods), '',
         '## Plugin generations', '',
         '| Generation | Models | What distinguishes it in the code |', '|---|---|---|',
         '| **A** (%d) | %s | No `DeviceModelManager` module (the product is found with group functions of the `RRMISDK` module such as `isTanosS6()`, each a list of model ids) and no retry protocol in the call wrapper. Most generation-A bundles still contain a `RobotApi` wrapper and, in some, the MIoT tunnel code. |' % (len(gen['A']), ' '.join(G.short(x) for x in sorted(gen['A'], key=G.natkey))),
         '| **B** (%d) | %s | A `DeviceModelManager` module (`DMM`) with a `Products` enumeration and a `DeviceInfoMap` (series → model ids, product, volume range); `FeatureManager` reads `DMM.currentProduct`. The call wrapper has the retry protocol ([transports](transports.md#retry-protocol)). |' % (len(gen['B']), ' '.join(G.short(x) for x in sorted(gen['B'], key=G.natkey))), '',
         'The boundary is by presence of the `DeviceModelManager` module (✅ Bundle · `deviceModelManager` module id per bundle in [`data/bundles.json`](../../data/bundles.json)). '
         'Bundle versions ≈ app plugin versions (`project.json` `version`); they are **not** firmware versions.', '',
         '## File formats', '',
         '| Format | Bundles |', '|---|---|']
    fmt = collections.defaultdict(list)
    for m, b in bundles.items():
        key = 'plain JavaScript (one `main.bundle`)' if b['format'] == 'plain-js' else ('Metro indexed RAM bundle, minified' if b.get('minified') else 'Metro indexed RAM bundle, not minified')
        fmt[key].append(m)
    for k, v in fmt.items():
        L.append('| %s | %s |' % (k, ' '.join(G.short(x) for x in sorted(v, key=G.natkey))))
    L += ['', '## Plugin versions', '', '| Plugin version | Build date (UTC) | Models |', '|---|---|---|']
    for v in sorted(ver, key=lambda s: [int(x) for x in s.split('.')]):
        dates = sorted({m['project']['build_date_utc'] for m in ver[v]})
        L.append('| %s | %s | %s |' % (v, dates[0] if len(dates) == 1 else '%s … %s' % (dates[0], dates[-1]), ' '.join(G.short(m['id']) for m in sorted(ver[v], key=lambda m: G.natkey(m['id'])))))
    L += ['', '## Product code names', '',
          'The plugin groups models into "products" with code names (not marketing names). The name is taken from the model\'s own bundle where it has one; '
          'models of generation A without a `DeviceModelManager` get their code name from the newest bundle\'s model table (marked with `*`; that bundle lists models it was not built for). The spelling differs between the two sources (for example `Rubyplus` from an own bundle, `RUBYPLUS` from the model table): each is the enumeration value as that bundle spells it.', '',
          '| Product code name | Models |', '|---|---|']
    for k in sorted(prod, key=lambda s: s.lower()):
        L.append('| `%s` | %s |' % (k, ' '.join('%s%s' % (G.short(x), '' if own else '*') for x, own in sorted(prod[k], key=lambda t: G.natkey(t[0])))))
    L += ['', '## Revision-suffixed ids', '',
          'Most bundles recognise a model id together with revision-suffixed ids `v2` … `v5` (for example `roborock.vacuum.a65v2`); they are listed on the device pages. '
          'A bundle is shared by all of them.', '',
          '## Two special tables', '',
          '- Bundles of `a01`, `c1`, `e2` choose a third method table (`tanosMethods`) instead of the default one ([`user.*` table](../commands/alternate-table.md)).',
          '- A `user.`-prefixed alternate table exists in every bundle but is selected only for models in the plugin\'s `saphireModelList`, which names the Xiaowa / Sapphire robots (e2, c1, a01 family); no analysed bundle activates it for its own model (details in [alternate table](../commands/alternate-table.md)).', '',
          '## See also', '', '- [Devices](../devices/index.md)', '- [Feature flags](feature-flags.md)', '- [Methodology](../methodology.md)', '']
    G.OUT['docs/concepts/model-generations.md'] = '\n'.join(L)


def gen_methodology(ctx, G):
    bundles = ctx.bundles
    best = [b for b in bundles if b['kind'] == 'best']
    variants = [b for b in bundles if b['kind'] == 'variant']
    methods = ctx.commands
    base = [m for m in methods if not m.startswith('user.')]
    users = [m for m in methods if m.startswith('user.')]
    st_count = collections.Counter()
    for m in base:
        x = methods[m]
        st_count['called' if x['models_called'] else 'wrapper' if x['models_wrapper_only'] else 'declared' if x['models_declared_only'] else 'parameter' if x['models_parameter_only'] else 'alternate'] += 1
    per = collections.defaultdict(collections.Counter)
    for m, x in methods.items():
        for bid, pb in x['per_bundle'].items():
            per[bid][pb['status']] += 1
    quirk = [b for b in best if b.get('project_models_field') and b['project_models_field'] != b['model']]
    noproj = [b for b in best if not b.get('project_models_field')]
    multi = sorted({v['model'] for v in variants}, key=G.natkey)
    import re as _re
    n_eq_sdk = n_eq_min = n_both = 0
    for b in bundles:
        mm = _re.search(r'signed_(\d+)_', b['file'])
        first = int(mm.group(1)) if mm else None
        a, c = first == b['sdk_api_level'], first == b['min_sdk_api_level']
        n_eq_sdk += a
        n_eq_min += c
        n_both += a and c
    status_fields = G.load_json('status_fields.json')['fields']
    L = ['# Methodology', '',
         '[Home](../README.md) / Methodology', '',
         'How the facts in this repository were derived, what they prove and what they do not, and how to regenerate everything. '
         'Short version: the **Mi Home plugin bundles** (the React-Native programs the official app runs for each robot model) were unpacked and analysed by script; '
         'every table that lists models, commands or enumerations is generated from the resulting datasets in [`data/`](../data/).', '',
         '<a id="what-a-bundle-does-and-does-not-prove"></a>',
         '## What a bundle does and does not prove', '',
         'A plugin bundle is the app side of the protocol. It proves:', '',
         '- that the official app **can send** a method, with exactly the parameters its code builds, and how it interprets the reply (field names, units, enumerations, ranges the UI allows);',
         '- the **strings** the app shows for states, errors and modes (taken from its English string table);',
         '- the **gates** inside the plugin: which controls it shows for which model id, firmware feature bit, region or product line.', '',
         'It does **not** prove:', '',
         '- that a particular robot **firmware** answers a given call (the bundle ships for a model family, the firmware varies per robot and release);',
         '- what the firmware does behind the call beyond what the UI shows; replies that the app never reads are invisible;',
         '- anything about the packet transport (the host app does that, [transports](concepts/transports.md)).', '',
         'Wording used throughout: "called by the plugin of model X" means a call site exists in the bundle of X. "Wrapper only" means the app has a wrapper function for the call but no caller was found; '
         '"declared only" means the string is in the method table but never used. A plugin version is **not** a firmware version.', '',
         '## Sources and priority', '',
         '1. **Plugin bundles** are the evidence (✅ Bundle). %d bundles, one per model (the newest build seen), plus %d regional builds that differ from them.' % (len(best), len(variants)),
         '2. The **openHAB miio binding** is a cross-check only (🔶 openHAB). Anything found only there is tagged and never mixed into the verified text.',
         '3. The **earlier content of this repository** (⚪ Legacy) was written from device captures and community knowledge. It is kept where a bundle confirms it or where it is the only source; corrections are listed in [corrections](appendix/corrections.md).',
         '4. The **Mi Home cloud device catalog** (per region) gives marketing names (tagged "Mi Home cloud device catalog"). Web searches were not used for facts.', '',
         'The legend of the evidence badges is in the [README](../README.md#evidence-legend).', '',
         '<a id="how-the-bundles-were-obtained"></a>',
         '## How the bundles were obtained', '',
         'The bundles are the plugins the Mi Home app downloads from the Xiaomi cloud when a device of that model is opened. They were collected with an openHAB miio binding support tool (`CloudAPKDownloader`, not yet published upstream); this section describes what that tool does, as read from its source.', '',
         '- **Model list.** The models come from the Mi Home cloud device catalog of each region (the catalog is a JSON document with a `list` of devices, each with `model` and `name`).',
         '- **Per region.** For every region server (`de`, `cn`, `ru`, `sg`, `in`, `us`) the tool asks the cloud\'s plugin service for the latest v2 plugin of each model, sending the region, the platform `Android`, the model and a plugin **`api_version`** (default `10119`, the value sent by Mi Home 11.9.521). '
         'The cloud returns a download URL only when the `api_version` it is sent is at least the plugin\'s required SDK level; models without a URL are recorded as unavailable and skipped on later runs.',
         '- **Old plugins.** An older, Java-based plugin type ("v1") is requested through a separate endpoint only on demand (the tool states that v1 has been phased out). Those files are native-Android packages without readable JavaScript and were not analysed (%d such files were seen).' % 17,
         '- **Shared plugins.** Some models are served by a shared standard plugin and have no download of their own (the cloud lists them with an empty URL and status 8).',
         '- **Login.** The cloud requires a Xiaomi account login; no credentials or session data are part of this repository.', '',
         '**File names.** The cloud serves each v2 plugin under a URL whose last path segment is the file name, in the pattern',
         '',
         '```',
         'signed_<sdk>_<n>_<n>_ANDROID_bundle_<md5>.zip',
         '```',
         '',
         'The model id is not part of that name. The download tool stores each file as `<model>-v2-<that name>` (a local convention of the tool, not a cloud name), and the unpack script accepts both forms ([tools](../tools/README.md)). '
         'What the numbers mean was checked against `project.json`:', '',
         '- The **first number** equals `sdk_api_level` of `project.json` in %d of the %d bundles and `min_sdk_api_level` in %d of them (both in %d); it is always one of the two. '
         'This fits the cloud rule that the request\'s `api_version` must reach the plugin\'s required SDK level, but the bundles do not say which `project.json` field the cloud uses, so this page never equates it with only one of them.' % (n_eq_sdk, len(bundles), n_eq_min, n_both),
         '- The **second number** is the same for all builds of a model that were seen; the **third number** grows with newer builds of the same model. Their meaning is **not verified** (neither matches `version_code` or `developer_id` of `project.json`).',
         '- The **trailing 32-hex value** is the md5 that identifies the zip. This page and the device pages therefore identify a bundle by model, plugin `version`, `sdk_api_level` and the first 8 hex digits of that md5.', '',
         '## What was extracted', '',
         '| Result | Count |', '|---|---:|',
         '| Plugin bundles analysed (best build per model) | %d |' % len(best),
         '| Further regional builds (different md5) | %d (of %d models) |' % (len(variants), len(multi)),
         '| Method strings found in any bundle | %d |' % len(methods),
         '| of which base strings (without `user.` prefix) | %d |' % len(base),
         '| of which `user.*` strings ([alternate table](commands/alternate-table.md)) | %d |' % len(users),
         '| Base strings called by at least one plugin | %d |' % st_count['called'],
         '| Base strings only wrapped | %d |' % st_count['wrapper'],
         '| Base strings only declared in a method table | %d |' % st_count['declared'],
         '| Base strings found only in the alternate (`user.`) table or as a parameter | %d |' % (st_count['alternate'] + st_count['parameter']),
         '| Status fields read by a status parser | %d ([status fields](reference/status-fields.md)) |' % len(status_fields),
         '', 'Every one of the %d method strings has an entry in the [command index](commands/index.md) or the [alternate table](commands/alternate-table.md); `tools/check_coverage.py` verifies this in both directions.' % len(methods), '',
         '## Bundle inventory', '',
         'One row per model: the bundle that the pages of this repository use as the evidence for the model. Columns "called", "wrapper" and "declared" count method strings by their best evidence in that bundle. '
         '`SDK` is `sdk_api_level` from `project.json`. Hash = first 8 hex digits of the md5 in the zip name.', '',
         '| Model | Plugin | SDK | Build date | Format | Modules | Regions | Hash | called | wrapper | declared |', '|---|---|---:|---|---|---:|---|---|---:|---:|---:|']
    for b in sorted(best, key=lambda b: G.natkey(b['model'])):
        p = per[b['id']]
        L.append('| [`%s`](devices/%s.md) | %s | %s | %s | %s | %d | %s | `%s` | %d | %d | %d |' % (
            G.short(b['model']), G.short(b['model']), b['version'], b['sdk_api_level'], b['build_date_utc'],
            {'plain-js': 'plain JS', 'indexed-ram': 'RAM' + (' (minified)' if b.get('minified') else '')}.get(b['format'], b['format']),
            b['modules'], ','.join(b['regions']), b['hash'][:8], p['called'], p['wrapper'], p['declared']))
    L += ['', '## Regional builds', '',
          'The same model can have several builds (different md5, region). Per model the newest build is used in the tables; the other builds were compared method by method and the differences are listed on the device page under "Regional builds". '
          'The following %d models have more than one build; every other model has a single md5 in all regions where it was found (for the ten models a26 a29 a37 a46 a52 a64 a66 a69 a74 a76 this was checked explicitly across the six regions CN, DE, IN, RU, SG, US).' % len(multi), '',
          '| Build | Regions | Plugin | SDK | Build date |', '|---|---|---|---:|---|']
    for v in sorted(variants, key=lambda b: G.natkey(b['id'])):
        L.append('| `%s` | %s | %s | %s | %s |' % (G.short(v['id']), ','.join(v['regions']), v['version'], v['sdk_api_level'], v['build_date_utc']))
    L += ['', '<a id="metadata-quirks"></a>',
          '## Metadata quirks', '',
          'Package metadata is not reliable and is never used as evidence on its own.', '',
          '- **`project.json` `models` field.** %d of the %d best bundles carry `"models": "roborock.vacuum.t4v2"` regardless of the model they were built for (%s). %d older bundles have no such field. Model attribution therefore comes from the catalog entry the plugin was requested for, i.e. from the download tool\'s file name.' % (len(quirk), len(best), ', '.join(G.short(b['model']) for b in sorted(quirk, key=lambda b: G.natkey(b['model']))), len(noproj)),
          '- **Package path.** Every bundle reports the same package path (`com.roborock.tanos`) in its metadata; the plugins are builds of one code base.',
          '- **Shared code.** Several models share a byte-identical `main.bundle` ([code families](devices/index.md#code-families)); their differences can only come from the model gates inside the code.',
          '- **Names.** `a29` and `a30` carry the same marketing name in the catalog ("Roborock G10"); the catalog and openHAB occasionally disagree (see [corrections](appendix/corrections.md#bundle-vs-openhab-conflicts)).',
          '- **Model ids with suffixes.** The plugin treats `a65v2` … `a65v5` (revision-suffixed ids) as the same model; they are not separate bundles. Whether they are hardware revisions is not stated by the bundles.', '',
          '## Extraction method', '',
          'Scripts live in [`tools/`](../tools/README.md); the pipeline `tools/run_pipeline.py` runs them in order.', '',
          '| Step | Script | Result |', '|---|---|---|',
          '| unpack | `unpack_plugins.py` | one folder per model with `main.bundle` or per-module files (Metro RAM bundles are split into `modules/m<id>.js`), resources, `project.json` |',
          '| RPC calls | `js/extract_rpc.mjs`, `build_commands.py` | AST scan: `Methods` tables, `RobotApi` / `RRMISDK` wrappers (also minified exports), call sites with parameter shapes and the reply fields read at the call site → `data/commands.json`, `data/bundles.json` |',
          '| enumerations | `js/extract_enums.mjs`, `build_enums.py` | named constant tables and string tables → `data/enums.json` |',
          '| consumables, cloud calls | `js/extract_consumables.mjs`, `js/extract_cloud_calls.mjs`, `build_consumables.py`, `build_cloud.py` | consumable keys and lives, cloud / smart-home calls → `data/consumables.json`, `data/cloud_calls.json` |',
          '| status fields | `js/extract_status_fields.mjs`, `build_status.py` | fields read by the status parser → `data/status_fields.json` |',
          '| feature gates | `js/extract_feature_defs.mjs`, `js/eval_features.mjs`, `build_models.py` | predicate definitions and their sandbox evaluation per model → `data/feature_gates.json`, `data/models.json` |',
          '| maps | `js/extract_map_schema.mjs`, `build_map_blocks.py` | block table of the app\'s map parser → `data/map_blocks.json` |',
          '| names | `catalog_names.py`, `openhab_models.py`, `legacy_models.py` | name sources → `data/catalog_names.json`, `data/openhab_models.json`, `data/legacy_models.json` |',
          '| pages | `gen_docs.py` (+ `gen_reference.py`, `gen_devices.py`, `gen_maps.py`, `gen_concepts.py`) | the generated Markdown (including the legacy-capture appendix and the cloud-calls page); hand-written text lives in `tools/curated/` |', '',
          'The curated text (parameter semantics, behaviour notes, legacy comparisons) was written by reading the call sites; claims name the module that was read (`model@version · m<id>`). '
          'Module ids are numeric and only meaningful inside one bundle; to look one up use the unpacked `modules/m<id>.js` of that bundle.', '',
          '## Limits', '',
          '- Dynamic behaviour (what firmware answers, what the host SDK does) is not observable from static code.',
          '- Parameter shapes come from call sites; where several call sites differ, the page lists the variants. Example payloads are labelled **constructed from app code** (built from the code, values invented) or **legacy capture (unverified)**.',
          '- Feature-gate evaluation uses a sandbox with stubs for runtime inputs; predicates that depend on them are classified `RT`/`N` and not interpreted ([feature flags](concepts/feature-flags.md#how-the-gates-were-evaluated)).',
          '- Account-specific allow lists inside the plugin (Mi Home user ids) are deliberately not recorded.',
          '- Models without a bundle (known only from the cloud catalog, openHAB or the plugins\' model tables) appear only in the [unverified models](appendix/unverified-models.md) appendix.',
          '- No proprietary source code is reproduced; short identifiers, method names, enumeration tables and one-line patterns are quoted.', '',
          '## Regenerating', '',
          '```',
          'python tools/run_pipeline.py --plugins-root <folder with the downloaded plugin zips per region> --work <scratch folder> --node <path to node> \\',
          '       --catalog-dir <folder with the per-region device catalog JSON> --openhab <path to the openHAB miio binding>',
          'python tools/gen_docs.py            # writes the generated Markdown',
          'python tools/gen_docs.py --check    # fails if a generated file would change',
          'python tools/check_links.py         # relative links and anchors in all Markdown files',
          '```', '',
          'Details and prerequisites are in [`tools/README.md`](../tools/README.md). The plugin downloads themselves are not part of this repository.', '',
          '## Contributing', '',
          'Corrections and captures are welcome. Please state the model, the firmware version and the exact request and reply. A new capture is added as ⚪ Legacy or as a labelled example until a bundle confirms it; '
          'if you have a plugin bundle for a model that is missing here, run the pipeline on it and open a pull request with the regenerated `data/` files.', '',
          '## See also', '', '- [README](../README.md)', '- [Devices](devices/index.md)', '- [Corrections](appendix/corrections.md)', '- [Open questions](appendix/open-questions.md)', '']
    G.OUT['docs/methodology.md'] = '\n'.join(L)


def gen_unverified(ctx, G):
    other = G.load_json('models.json')['other']
    meta = G.load_json('models.json')['meta']
    L = ['# Models without a plugin bundle (unverified)', '',
         '[Home](../../README.md) / Appendix / Unverified models', '',
         'These model ids are known from sources other than a plugin bundle of their own, so **nothing on the command, enumeration or gate pages was verified for them**. '
         'Each row shows where the id appears: the openHAB miio binding (🔶 openHAB), the earlier content of this repository (⚪ Legacy), the Mi Home cloud device catalog, '
         'or the model table (`DeviceModelManager`) inside the newest analysed plugin (%s; ✅ Bundle, but only as "the plugin knows this id and groups it under this product code name"). '
         'Hardware-revision aliases such as `a65v2` are not listed; they belong to the bundled model.' % G.short(meta['deviceModelManager_source']), '',
         'The product code name is the grouping of models into product lines, not a statement about capabilities; no capability is inferred for these models.', '',
         '| Model id | openHAB name (🔶) | Legacy name (⚪) | Catalog name | Plugin model table: series / product code name (✅) |', '|---|---|---|---|---|']
    for m in sorted(other, key=G.natkey):
        o = other[m]
        oh = o.get('openhab', {}).get('name', '') if o.get('openhab') else ''
        lg = ''
        if o.get('legacy'):
            lg = o['legacy'].get('readme_name') or o['legacy'].get('fw_features_name') or ''
        cat = '; '.join(sorted({v for v in (o.get('catalog') or {}).values() if v}))
        d = o.get('deviceModelManager')
        L.append('| `%s` | %s | %s | %s | %s |' % (m, oh, lg, cat, ('`%s` / `%s`' % (d['series'], d['product'])) if d else ''))
    L += ['', 'Counts: %d ids. The marketing names in the "Catalog name" column come from the Mi Home cloud device catalog; the openHAB column shows the binding\'s own wording.' % len(other), '',
          '## See also', '', '- [Devices](../devices/index.md)', '- [Methodology](../methodology.md)', '- [Open questions](open-questions.md)', '']
    G.OUT['docs/appendix/unverified-models.md'] = '\n'.join(L)


def gen_readme(ctx, G):
    mods = G.load_json('models.json')['bundled']
    mods = mods if isinstance(mods, list) else list(mods.values())
    methods = ctx.commands
    base = [m for m in methods if not m.startswith('user.')]
    n_called = sum(1 for m in base if methods[m]['models_called'])
    L = ['<a id="xiaomi-robot-vacuum-protocol"></a>', '# Xiaomi / Roborock Robot Vacuum Protocol', '',
         'The command reference for Xiaomi and Roborock robot vacuums that speak the **miIO** protocol: which methods exist, what parameters they take, what they return, '
         'which robot models the official app offers them for, and how maps are encoded. Every statement carries its evidence level: **Mi Home plugin bundles** (the programs the official app runs for each model) are the evidence; '
         'where a fact comes from elsewhere or cannot be determined, the page says so.', '',
         '**For:** integrators (openHAB, Home Assistant, ioBroker, python-miio), tinkerers, and anyone asking "what does command X do, with which parameters, on which robot?".', '',
         '## Quick start', '',
         '1. [Get the token and the IP address](docs/getting-started/get-token-and-ip.md) of your robot.',
         '2. [Send a first command](docs/getting-started/first-command.md), for example `{"id": 1, "method": "get_prop", "params": ["get_status"]}`.',
         '3. Look up what you want to do in the [command index](docs/commands/index.md) and what your model offers on its [device page](docs/devices/index.md).', '',
         'Implementations of the protocol: [openHAB](https://github.com/openhab/openhab-addons/tree/main/bundles/org.openhab.binding.miio) (Java), '
         '[python-miio](https://github.com/rytilahti/python-miio) (Python), [ioBroker mihome-vacuum](https://github.com/iobroker-community-adapters/ioBroker.mihome-vacuum) and '
         '[ioBroker roborock](https://github.com/copystring/ioBroker.roborock/) (JavaScript).', '',
         '<a id="evidence-legend"></a>',
         '## Evidence legend', '',
         'Every page marks where a fact comes from:', '',
         '| Badge | Meaning |', '|---|---|',
         '| ✅ **Bundle** | Verified in at least one Mi Home plugin bundle. The page names the models and, for non-trivial facts, a source anchor in the form `model@plugin version · m<module id> · "string anchor"` (module ids are numeric and local to one bundle). |',
         '| 🔶 **openHAB** | Only in the openHAB miio binding; not seen in any bundle. Cross-check only. |',
         '| ⚪ **Legacy** | Only in the earlier content of this repository (device captures, community knowledge); not confirmed by a bundle. |',
         '| ❓ **Unknown** | Not determinable; the page says what was checked. |', '',
         'Important distinction: **"the bundle calls it" is not "this robot\'s firmware answers it".** A call site proves that the official app can send the call and how it builds the parameters; it does not prove that a particular firmware responds. '
         'Details and limits: [methodology](docs/methodology.md#what-a-bundle-does-and-does-not-prove). Example payloads are labelled **constructed from app code** (values invented) or **legacy capture (unverified)**.', '',
         '## Contents', '',
         '| Section | What is in it |', '|---|---|',
         '| [Getting started](docs/getting-started/index.md) | token and IP, first command, troubleshooting |',
         '| [Concepts](docs/concepts/index.md) | [miIO protocol](docs/concepts/miio-protocol.md), [JSON-RPC envelope](docs/concepts/json-rpc-envelope.md), [transports and dispatch](docs/concepts/transports.md), [feature flags](docs/concepts/feature-flags.md), [model generations](docs/concepts/model-generations.md), [maps overview](docs/concepts/maps-overview.md) |',
         '| [Commands](docs/commands/index.md) | all %d method strings found in the bundles, in 16 categories, with the [`user.*` alternate table](docs/commands/alternate-table.md) |' % len(methods),
         '| [Reference](docs/reference/index.md) | [states](docs/reference/states.md), [errors](docs/reference/errors.md), [fan, water and mop values](docs/reference/fan-water-mop.md), [status fields](docs/reference/status-fields.md), [consumables](docs/reference/consumables.md), [dock](docs/reference/dock.md), [clean record](docs/reference/clean-record.md), [voice packs](docs/reference/voice-packs.md), [units](docs/reference/units.md), [other enumerations](docs/reference/other-enums.md) |',
         '| [Devices](docs/devices/index.md) | one page per model, [command matrix](docs/devices/matrix-commands.md), [feature matrix](docs/devices/matrix-features.md) |',
         '| [Maps](docs/maps/index.md) | [RR map file format](RRMapFile/RRFileFormat.md), sample files and viewers in [`RRMapFile/`](RRMapFile/README.md) |',
         '| [Methodology](docs/methodology.md) | how the facts were derived, bundle inventory, limits, regeneration |',
         '| [Appendix](docs/appendix/index.md) | [corrections](docs/appendix/corrections.md), [legacy captures](docs/appendix/legacy-captures.md), [unverified models](docs/appendix/unverified-models.md), [open questions](docs/appendix/open-questions.md), [glossary](docs/appendix/glossary.md) |',
         '| [Tools and data](tools/README.md) | scripts that regenerate everything, and the machine-readable datasets in [`data/`](data/) |', '',
         '## Analysed models', '',
         '%d models were analysed from their own plugin bundle; pages are generated from [`data/models.json`](data/models.json). Names are tagged with their source on the device pages (Mi Home cloud device catalog, openHAB binding, legacy text). '
         'Models known only from other sources are in the [unverified models](docs/appendix/unverified-models.md) appendix.' % len(mods), '',
         '| Model | Name (Mi Home cloud device catalog) | Plugin | Generation |', '|---|---|---|---|']
    for m in sorted(mods, key=lambda x: G.natkey(x['id'])):
        names = sorted({c['name'] for c in m['names'].get('catalog', [])})
        nm = ' / '.join(names) or (m['names'].get('openhab') or m['names'].get('legacy') or '')
        L.append('| [`%s`](docs/devices/%s.md) | %s | %s | %s |' % (m['id'], G.short(m['id']), nm, m['project']['version'], m['generation'][0]))
    L += ['', 'Generation A = older plugin, B = newer plugin ([model generations](docs/concepts/model-generations.md)).', '',
          '## Numbers', '',
          '%d method strings found in the bundles: %d base strings and %d with the `user.` prefix. %d of the %d base strings have a call site in at least one plugin. Per-bundle counts are in the [methodology](docs/methodology.md#bundle-inventory).' % (len(methods), len(base), len(methods) - len(base), n_called, len(base)), '',
          '## Vacuum Commands', '', 'The old command table of this page is replaced by the [command index](docs/commands/index.md).', '',
          '## Generic MiIO Commands', '', 'See [generic miIO methods](docs/concepts/miio-protocol.md#generic-methods).', '',
          '## Ruby variant commands', '', 'See the [`user.*` alternate table](docs/commands/alternate-table.md).', '',
          '## Stable links', '',
          'Pages that earlier lived at the repository root (`status.md`, `custom_mode.md`, `fw_features.md`, `Protocol.md`, ...) remain as short pointers to their new place; the files in `RRMapFile/` did not move.', '',
          '## Contributing', '',
          'Corrections, captures from real robots and plugin bundles for missing models are welcome; see [methodology](docs/methodology.md#contributing). '
          'The documentation is generated from data and curated text: edit the curated files in [`tools/curated/`](tools/curated/) rather than the generated pages, and regenerate with the scripts described in [`tools/README.md`](tools/README.md).', '',
          '## License', '', 'See [LICENSE](LICENSE).', '']
    G.OUT['README.md'] = '\n'.join(L)
