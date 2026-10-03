# Methodology

[Home](../README.md) / Methodology

How the facts in this repository were derived, what they prove and what they do not, and how to regenerate everything. Short version: the **Mi Home plugin bundles** (the React-Native programs the official app runs for each robot model) were unpacked and analysed by script; every table that lists models, commands or enumerations is generated from the resulting datasets in [`data/`](../data/).

<a id="what-a-bundle-does-and-does-not-prove"></a>
## What a bundle does and does not prove

A plugin bundle is the app side of the protocol. It proves:

- that the official app **can send** a method, with exactly the parameters its code builds, and how it interprets the reply (field names, units, enumerations, ranges the UI allows);
- the **strings** the app shows for states, errors and modes (taken from its English string table);
- the **gates** inside the plugin: which controls it shows for which model id, firmware feature bit, region or product line.

It does **not** prove:

- that a particular robot **firmware** answers a given call (the bundle ships for a model family, the firmware varies per robot and release);
- what the firmware does behind the call beyond what the UI shows; replies that the app never reads are invisible;
- anything about the packet transport (the host app does that, [transports](concepts/transports.md)).

Wording used throughout: "called by the plugin of model X" means a call site exists in the bundle of X. "Wrapper only" means the app has a wrapper function for the call but no caller was found; "declared only" means the string is in the method table but never used. A plugin version is **not** a firmware version.

## Sources and priority

1. **Plugin bundles** are the evidence (✅ Bundle). 42 bundles, one per model (the newest build seen), plus 20 regional builds that differ from them.
2. The **openHAB miio binding** is a cross-check only (🔶 openHAB). Anything found only there is tagged and never mixed into the verified text.
3. The **earlier content of this repository** (⚪ Legacy) was written from device captures and community knowledge. It is kept where a bundle confirms it or where it is the only source; corrections are listed in [corrections](appendix/corrections.md).
4. The **Mi Home cloud device catalog** (per region) gives marketing names (tagged "Mi Home cloud device catalog"). Web searches were not used for facts.

The legend of the evidence badges is in the [README](../README.md#evidence-legend).

<a id="how-the-bundles-were-obtained"></a>
## How the bundles were obtained

The bundles are the plugins the Mi Home app downloads from the Xiaomi cloud when a device of that model is opened. They were collected with an openHAB miio binding support tool (`CloudAPKDownloader`, not yet published upstream); this section describes what that tool does, as read from its source.

- **Model list.** The models come from the Mi Home cloud device catalog of each region (the catalog is a JSON document with a `list` of devices, each with `model` and `name`).
- **Per region.** For every region server (`de`, `cn`, `ru`, `sg`, `in`, `us`) the tool asks the cloud's plugin service for the latest v2 plugin of each model, sending the region, the platform `Android`, the model and a plugin **`api_version`** (default `10119`, the value sent by Mi Home 11.9.521). The cloud returns a download URL only when the `api_version` it is sent is at least the plugin's required SDK level; models without a URL are recorded as unavailable and skipped on later runs.
- **Old plugins.** An older, Java-based plugin type ("v1") is requested through a separate endpoint only on demand (the tool states that v1 has been phased out). Those files are native-Android packages without readable JavaScript and were not analysed (17 such files were seen).
- **Shared plugins.** Some models are served by a shared standard plugin and have no download of their own (the cloud lists them with an empty URL and status 8).
- **Login.** The cloud requires a Xiaomi account login; no credentials or session data are part of this repository.

**File names.** The cloud serves each v2 plugin under a URL whose last path segment is the file name, in the pattern

```
signed_<sdk>_<n>_<n>_ANDROID_bundle_<md5>.zip
```

The model id is not part of that name. The download tool stores each file as `<model>-v2-<that name>` (a local convention of the tool, not a cloud name), and the unpack script accepts both forms ([tools](../tools/README.md)). What the numbers mean was checked against `project.json`:

- The **first number** equals `sdk_api_level` of `project.json` in 41 of the 62 bundles and `min_sdk_api_level` in 30 of them (both in 9); it is always one of the two. This fits the cloud rule that the request's `api_version` must reach the plugin's required SDK level, but the bundles do not say which `project.json` field the cloud uses, so this page never equates it with only one of them.
- The **second number** is the same for all builds of a model that were seen; the **third number** grows with newer builds of the same model. Their meaning is **not verified** (neither matches `version_code` or `developer_id` of `project.json`).
- The **trailing 32-hex value** is the md5 that identifies the zip. This page and the device pages therefore identify a bundle by model, plugin `version`, `sdk_api_level` and the first 8 hex digits of that md5.

## What was extracted

| Result | Count |
|---|---:|
| Plugin bundles analysed (best build per model) | 42 |
| Further regional builds (different md5) | 20 (of 15 models) |
| Method strings found in any bundle | 295 |
| of which base strings (without `user.` prefix) | 248 |
| of which `user.*` strings ([alternate table](commands/alternate-table.md)) | 47 |
| Base strings called by at least one plugin | 229 |
| Base strings only wrapped | 10 |
| Base strings only declared in a method table | 7 |
| Base strings found only in the alternate (`user.`) table or as a parameter | 2 |
| Status fields read by a status parser | 59 ([status fields](reference/status-fields.md)) |

Every one of the 295 method strings has an entry in the [command index](commands/index.md) or the [alternate table](commands/alternate-table.md); `tools/check_coverage.py` verifies this in both directions.

## Bundle inventory

One row per model: the bundle that the pages of this repository use as the evidence for the model. Columns "called", "wrapper" and "declared" count method strings by their best evidence in that bundle. `SDK` is `sdk_api_level` from `project.json`. Hash = first 8 hex digits of the md5 in the zip name.

| Model | Plugin | SDK | Build date | Format | Modules | Regions | Hash | called | wrapper | declared |
|---|---|---:|---|---|---:|---|---|---:|---:|---:|
| [`a01`](devices/a01.md) | 1.0.51 | 10051 | 2021-03-03 | plain JS | 1033 | IN,SG,US | `7f803c31` | 73 | 8 | 11 |
| [`a08`](devices/a08.md) | 1.0.47 | 10047 | 2020-12-04 | plain JS | 1417 | IN,RU,SG,US | `a87b7356` | 114 | 9 | 10 |
| [`a09`](devices/a09.md) | 1.0.48 | 10048 | 2020-12-25 | plain JS | 1420 | CN | `26566684` | 114 | 9 | 10 |
| [`a10`](devices/a10.md) | 1.0.50 | 10050 | 2021-02-08 | plain JS | 1426 | IN,SG,US | `35117b7d` | 114 | 9 | 10 |
| [`a11`](devices/a11.md) | 1.0.34 | 10034 | 2020-04-09 | plain JS | 883 | CN | `7d6d95bf` | 101 | 7 | 10 |
| [`a14`](devices/a14.md) | 1.0.53 | 10053 | 2021-04-14 | plain JS | 1680 | CN | `ccbb120c` | 131 | 9 | 10 |
| [`a15`](devices/a15.md) | 1.0.53 | 10053 | 2021-04-14 | plain JS | 1680 | IN,RU,SG,US | `ccbb120c` | 131 | 9 | 10 |
| [`a19`](devices/a19.md) | 1.0.52 | 10052 | 2021-03-29 | plain JS | 1427 | DE,US | `7307f790` | 114 | 9 | 10 |
| [`a23`](devices/a23.md) | 1.0.53 | 10053 | 2021-04-01 | plain JS | 1680 | CN | `5ff2ea2c` | 131 | 9 | 10 |
| [`a26`](devices/a26.md) | 1.0.84 | 10084 | 2023-07-21 | RAM (minified) | 1582 | CN,DE,IN,RU,SG,US | `842a376b` | 202 | 21 | 8 |
| [`a27`](devices/a27.md) | 1.0.84 | 10084 | 2023-07-21 | RAM (minified) | 1582 | DE,IN,RU,SG,US | `30bb940d` | 202 | 21 | 8 |
| [`a29`](devices/a29.md) | 1.0.75 | 10075 | 2022-11-04 | RAM (minified) | 1957 | CN,DE,IN,RU,SG,US | `ebafd1e5` | 194 | 20 | 8 |
| [`a30`](devices/a30.md) | 1.0.75 | 10075 | 2022-11-04 | RAM (minified) | 1957 | IN,SG | `91562698` | 194 | 20 | 8 |
| [`a34`](devices/a34.md) | 1.0.70 | 10070 | 2022-06-23 | RAM | 1902 | IN,SG,US | `32e69096` | 177 | 19 | 8 |
| [`a37`](devices/a37.md) | 1.0.70 | 10070 | 2022-06-23 | RAM | 1902 | CN,DE,IN,RU,SG,US | `1628ce0b` | 177 | 19 | 8 |
| [`a38`](devices/a38.md) | 1.0.70 | 10070 | 2022-06-24 | RAM | 1902 | DE | `35c449b2` | 177 | 19 | 8 |
| [`a40`](devices/a40.md) | 1.0.70 | 10070 | 2022-06-23 | RAM | 1902 | DE | `a6941126` | 177 | 19 | 8 |
| [`a46`](devices/a46.md) | 1.0.84 | 10084 | 2023-07-21 | RAM (minified) | 1582 | CN,DE,IN,RU,SG,US | `5e5b8e0f` | 202 | 21 | 8 |
| [`a51`](devices/a51.md) | 1.0.83 | 10083 | 2023-07-07 | RAM (minified) | 1563 | DE,IN,RU,SG,US | `8aa7de52` | 200 | 21 | 8 |
| [`a52`](devices/a52.md) | 1.0.70 | 10070 | 2022-07-21 | RAM | 1922 | CN,DE,IN,RU,SG,US | `ffbb9479` | 177 | 19 | 8 |
| [`a62`](devices/a62.md) | 1.0.69 | 10069 | 2022-05-10 | RAM | 1883 | CN,DE,IN,RU,SG,US | `6fdbaa08` | 179 | 12 | 8 |
| [`a64`](devices/a64.md) | 1.0.95 | 10095 | 2024-06-27 | RAM | 1570 | CN,DE,IN,RU,SG,US | `772b9968` | 202 | 21 | 8 |
| [`a65`](devices/a65.md) | 1.0.95 | 10095 | 2024-06-27 | RAM | 1570 | RU,US | `ca959e57` | 202 | 21 | 8 |
| [`a66`](devices/a66.md) | 1.0.84 | 10084 | 2023-07-21 | RAM (minified) | 1582 | CN,DE,IN,RU,SG,US | `4f7ec77a` | 202 | 21 | 8 |
| [`a69`](devices/a69.md) | 1.0.86 | 10086 | 2023-10-09 | RAM (minified) | 1563 | CN,DE,IN,RU,SG,US | `c2c7596b` | 200 | 21 | 8 |
| [`a70`](devices/a70.md) | 1.0.83 | 10083 | 2023-06-30 | RAM (minified) | 1563 | DE,IN,RU,SG,US | `aa6df036` | 200 | 21 | 8 |
| [`a72`](devices/a72.md) | 1.0.92 | 10092 | 2024-04-17 | RAM | 1585 | IN,RU,US | `5ba3547d` | 209 | 19 | 8 |
| [`a73`](devices/a73.md) | 1.0.92 | 10092 | 2024-04-17 | RAM | 1585 | RU,US | `18ad0dc9` | 209 | 19 | 8 |
| [`a74`](devices/a74.md) | 1.0.96 | 10096 | 2024-08-01 | RAM | 1588 | CN,DE,IN,RU,SG,US | `0da0d8ed` | 202 | 21 | 8 |
| [`a75`](devices/a75.md) | 1.0.89 | 10089 | 2023-12-12 | RAM | 1588 | DE | `66becc3a` | 202 | 21 | 8 |
| [`a76`](devices/a76.md) | 1.0.77 | 10077 | 2023-01-05 | RAM (minified) | 1959 | CN,DE,IN,RU,SG,US | `b49b68a2` | 194 | 20 | 8 |
| [`c1`](devices/c1.md) | 1.0.48 | 10048 | 2020-12-30 | plain JS | 1023 | DE,IN,RU,SG,US | `42c531ce` | 73 | 8 | 11 |
| [`e2`](devices/e2.md) | 1.0.48 | 10048 | 2020-12-30 | plain JS | 1023 | IN,RU,SG,US | `42c531ce` | 73 | 8 | 11 |
| [`m1s`](devices/m1s.md) | 1.0.34 | 10034 | 2020-04-14 | plain JS | 678 | CN | `63599f00` | 79 | 7 | 10 |
| [`p5`](devices/p5.md) | 1.0.34 | 10034 | 2020-03-17 | plain JS | 819 | CN | `1e129e82` | 100 | 6 | 10 |
| [`s4`](devices/s4.md) | 1.0.47 | 10047 | 2020-12-04 | plain JS | 1417 | US | `2cae915f` | 114 | 9 | 10 |
| [`s5`](devices/s5.md) | 1.0.47 | 10047 | 2020-12-08 | plain JS | 1018 | IN,RU,SG,US | `d3188909` | 91 | 6 | 8 |
| [`s5e`](devices/s5e.md) | 1.0.49 | 10049 | 2021-01-05 | plain JS | 1419 | IN,RU,SG,US | `80ef03cb` | 114 | 9 | 10 |
| [`s6`](devices/s6.md) | 1.0.47 | 10047 | 2020-12-04 | plain JS | 1417 | IN,RU,SG,US | `2c23ad58` | 114 | 9 | 10 |
| [`t4`](devices/t4.md) | 1.0.32 | 10032 | 2020-01-03 | plain JS | 506 | CN | `634b68fa` | 85 | 6 | 10 |
| [`t6`](devices/t6.md) | 1.0.32 | 10032 | 2020-01-03 | plain JS | 458 | CN | `b43ac478` | 84 | 6 | 10 |
| [`v1`](devices/v1.md) | 1.0.46 | 10046 | 2020-11-18 | plain JS | 1072 | IN,RU,SG | `97f09a55` | 76 | 6 | 6 |

## Regional builds

The same model can have several builds (different md5, region). Per model the newest build is used in the tables; the other builds were compared method by method and the differences are listed on the device page under "Regional builds". The following 15 models have more than one build; every other model has a single md5 in all regions where it was found (for the ten models a26 a29 a37 a46 a52 a64 a66 a69 a74 a76 this was checked explicitly across the six regions CN, DE, IN, RU, SG, US).

| Build | Regions | Plugin | SDK | Build date |
|---|---|---|---:|---|
| `a01@761267f4` | DE | 1.0.35 | 10035 | 2020-03-10 |
| `a01@da4f2797` | CN,RU | 1.0.47 | 10047 | 2020-11-30 |
| `a08@1e129e82` | DE | 1.0.34 | 10034 | 2020-03-17 |
| `a08@33224506` | CN | 1.0.34 | 10034 | 2020-08-17 |
| `a10@1af87cdf` | CN,DE | 1.0.34 | 10034 | 2020-06-13 |
| `a10@faa8dbc2` | RU | 1.0.48 | 10048 | 2020-12-25 |
| `a15@a1df84d4` | DE | 1.0.52 | 10052 | 2021-03-12 |
| `a65@01cc8681` | DE,IN,SG | 1.0.83 | 10083 | 2023-07-10 |
| `a72@7907121f` | DE,SG | 1.0.85 | 10085 | 2023-08-29 |
| `a73@1dd6af45` | DE,IN,SG | 1.0.83 | 10083 | 2023-07-11 |
| `a75@1f1f19e9` | IN,RU,SG,US | 1.0.82 | 10082 | 2023-06-20 |
| `c1@ea1df7b1` | CN | 1.0.34 | 10034 | 2020-03-31 |
| `e2@26e9c09e` | DE | 1.0.46 | 10046 | 2020-11-18 |
| `e2@ea1df7b1` | CN | 1.0.34 | 10034 | 2020-03-31 |
| `s4@634b68fa` | DE | 1.0.32 | 10032 | 2020-01-03 |
| `s5@330efc74` | DE | 1.0.46 | 10046 | 2020-11-18 |
| `s5@f6d4be23` | CN,DE | 1.0.35 | 10035 | 2020-02-28 |
| `s5e@c49a013c` | DE | 1.0.34 | 10034 | 2020-03-27 |
| `s6@b43ac478` | DE | 1.0.32 | 10032 | 2020-01-03 |
| `v1@f1819b44` | CN,DE | 1.0.32 | 10032 | 2020-01-03 |

<a id="metadata-quirks"></a>
## Metadata quirks

Package metadata is not reliable and is never used as evidence on its own.

- **`project.json` `models` field.** 26 of the 42 best bundles carry `"models": "roborock.vacuum.t4v2"` regardless of the model they were built for (a01, a26, a27, a29, a30, a34, a37, a38, a40, a46, a51, a52, a62, a64, a65, a66, a69, a70, a72, a73, a74, a75, a76, c1, e2, s5). 16 older bundles have no such field. Model attribution therefore comes from the catalog entry the plugin was requested for, i.e. from the download tool's file name.
- **Package path.** Every bundle reports the same package path (`com.roborock.tanos`) in its metadata; the plugins are builds of one code base.
- **Shared code.** Several models share a byte-identical `main.bundle` ([code families](devices/index.md#code-families)); their differences can only come from the model gates inside the code.
- **Names.** `a29` and `a30` carry the same marketing name in the catalog ("Roborock G10"); the catalog and openHAB occasionally disagree (see [corrections](appendix/corrections.md#bundle-vs-openhab-conflicts)).
- **Model ids with suffixes.** The plugin treats `a65v2` … `a65v5` (revision-suffixed ids) as the same model; they are not separate bundles. Whether they are hardware revisions is not stated by the bundles.

## Extraction method

Scripts live in [`tools/`](../tools/README.md); the pipeline `tools/run_pipeline.py` runs them in order.

| Step | Script | Result |
|---|---|---|
| unpack | `unpack_plugins.py` | one folder per model with `main.bundle` or per-module files (Metro RAM bundles are split into `modules/m<id>.js`), resources, `project.json` |
| RPC calls | `js/extract_rpc.mjs`, `build_commands.py` | AST scan: `Methods` tables, `RobotApi` / `RRMISDK` wrappers (also minified exports), call sites with parameter shapes and the reply fields read at the call site → `data/commands.json`, `data/bundles.json` |
| enumerations | `js/extract_enums.mjs`, `build_enums.py` | named constant tables and string tables → `data/enums.json` |
| consumables, cloud calls | `js/extract_consumables.mjs`, `js/extract_cloud_calls.mjs`, `build_consumables.py`, `build_cloud.py` | consumable keys and lives, cloud / smart-home calls → `data/consumables.json`, `data/cloud_calls.json` |
| status fields | `js/extract_status_fields.mjs`, `build_status.py` | fields read by the status parser → `data/status_fields.json` |
| feature gates | `js/extract_feature_defs.mjs`, `js/eval_features.mjs`, `build_models.py` | predicate definitions and their sandbox evaluation per model → `data/feature_gates.json`, `data/models.json` |
| maps | `js/extract_map_schema.mjs`, `build_map_blocks.py` | block table of the app's map parser → `data/map_blocks.json` |
| names | `catalog_names.py`, `openhab_models.py`, `legacy_models.py` | name sources → `data/catalog_names.json`, `data/openhab_models.json`, `data/legacy_models.json` |
| pages | `gen_docs.py` (+ `gen_reference.py`, `gen_devices.py`, `gen_maps.py`, `gen_concepts.py`) | the generated Markdown (including the legacy-capture appendix and the cloud-calls page); hand-written text lives in `tools/curated/` |

The curated text (parameter semantics, behaviour notes, legacy comparisons) was written by reading the call sites; claims name the module that was read (`model@version · m<id>`). Module ids are numeric and only meaningful inside one bundle; to look one up use the unpacked `modules/m<id>.js` of that bundle.

## Limits

- Dynamic behaviour (what firmware answers, what the host SDK does) is not observable from static code.
- Parameter shapes come from call sites; where several call sites differ, the page lists the variants. Example payloads are labelled **constructed from app code** (built from the code, values invented) or **legacy capture (unverified)**.
- Feature-gate evaluation uses a sandbox with stubs for runtime inputs; predicates that depend on them are classified `RT`/`N` and not interpreted ([feature flags](concepts/feature-flags.md#how-the-gates-were-evaluated)).
- Account-specific allow lists inside the plugin (Mi Home user ids) are deliberately not recorded.
- Models without a bundle (known only from the cloud catalog, openHAB or the plugins' model tables) appear only in the [unverified models](appendix/unverified-models.md) appendix.
- No proprietary source code is reproduced; short identifiers, method names, enumeration tables and one-line patterns are quoted.

## Regenerating

```
python tools/run_pipeline.py --plugins-root <folder with the downloaded plugin zips per region> --work <scratch folder> --node <path to node> \
       --catalog-dir <folder with the per-region device catalog JSON> --openhab <path to the openHAB miio binding>
python tools/gen_docs.py            # writes the generated Markdown
python tools/gen_docs.py --check    # fails if a generated file would change
python tools/check_links.py         # relative links and anchors in all Markdown files
```

Details and prerequisites are in [`tools/README.md`](../tools/README.md). The plugin downloads themselves are not part of this repository.

## Contributing

Corrections and captures are welcome. Please state the model, the firmware version and the exact request and reply. A new capture is added as ⚪ Legacy or as a labelled example until a bundle confirms it; if you have a plugin bundle for a model that is missing here, run the pipeline on it and open a pull request with the regenerated `data/` files.

## See also

- [README](../README.md)
- [Devices](devices/index.md)
- [Corrections](appendix/corrections.md)
- [Open questions](appendix/open-questions.md)
