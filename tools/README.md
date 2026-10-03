# Tools: regenerating the datasets and the documentation

[Home](../README.md) / Tools

Everything in `data/` and every generated page in `docs/` (plus `RRMapFile/RRFileFormat.md` and `README.md`) is produced by the scripts here from **plugin bundles you download yourself**. No bundle code is part of this repository: the unpacked corpus goes into a scratch folder.

## Prerequisites

- Python 3.10+ with `PyYAML` (`pip install pyyaml`).
- Node.js 20+; run `npm install` once in `tools/js` (installs `acorn`, `acorn-walk`, `prettier`).
- Git (the legacy comparison reads the old pages from a git commit).

## Inputs

| Input | What it is | Option |
|---|---|---|
| Plugin zips | A folder with the downloaded Mi Home plugin zips **per region**: one sub-folder per region, named `<prefix><REGION>` (default: no prefix, so the sub-folder names are the region labels, for example `CN`, `DE`; use `--region-dir-prefix` if your folders carry a common prefix and the root also holds other folders). Two file name forms are accepted: the cloud's own name `signed_<sdk>_<n>_<n>_ANDROID_bundle_<md5>.zip` placed in a sub-folder named after the model (`<region folder>/<model>/signed_....zip`), or the same name with a local `<model>-v2-` prefix anywhere below the region folder. See [methodology](../docs/methodology.md#how-the-bundles-were-obtained). | `--plugins-root`, `--region-dir-prefix` |
| Device catalog (optional, for marketing names) | A folder with one JSON document per region. Each document is a JSON object with a `list` array of device entries; every entry has at least `model` and `name` (optional: `status`, `pd_id`, `min_app_version`, `localizations.en.name`); optional top-level `last_modify`. The region label is taken from the file name through the pattern `--catalog-glob` (default `*_{region}.json`). | `--catalog-dir`, `--catalog-glob`, `--exclude-model` |
| openHAB binding (optional) | A checkout of the openHAB add-ons repository, path of `org.openhab.binding.miio`. The files are read from git (`git show <ref>:<path>`, default ref `main`), so the checked-out branch does not matter; the commit hash and date are recorded in `data/openhab_models.json`. | `--openhab`, `--openhab-ref` |
| Legacy text | Read from git: commit `be636c7` holds the pages as they were before the rewrite | `--legacy-ref` |

## Run everything

```
python tools/run_pipeline.py --plugins-root <folder with plugin zips per region> --work <scratch folder> \
       --node <path to the node executable> --catalog-dir <folder with the device catalog JSON> --data-out <folder> \
       --openhab <path to org.openhab.binding.miio>
python tools/gen_docs.py             # writes README.md, docs/**, RRMapFile/RRFileFormat.md from data/ and tools/curated/
python tools/make_stubs.py           # writes the pointer pages that replace the old root-level pages
python tools/check_links.py          # relative links and anchors in all Markdown files
python tools/check_coverage.py --corpus <unpacked corpus>   # every method string is documented and vice versa; regression tests of the call-site detection (wrapper-only and called pairs, RAM and plain bundles), of the gate evaluation and a lint of the examples
python tools/gen_docs.py --check     # fails if a generated file differs from what the data would produce
```

`--data-out <folder>` writes the generated JSON to a scratch folder instead of `data/` (the name-source files are copied over if missing) so that a run can be diffed against the committed data. `run_pipeline.py --steps unpack,rpc,...` runs a subset (`unpack`, `catalog`, `openhab`, `legacy`, `rpc`, `enums`, `status`, `cons`, `cloud`, `fdefs`, `feat`, `maps`, `build`); `--corpus <folder>` reuses an existing unpacked corpus.

## Scripts

| Script | Purpose |
|---|---|
| `unpack_plugins.py` | unpack zips; best build per model plus (with `--variants`) every other distinct md5; splits Metro RAM bundles into `modules/m<id>.js` |
| `bundlelib.py`, `enumlib.py` | shared helpers (module loading, string tables, enumeration queries) |
| `js/extract_rpc.mjs`, `build_commands.py` | method tables, wrappers, call sites with parameter shapes → `data/commands.json`, `data/bundles.json` |
| `js/extract_enums.mjs`, `build_enums.py` | enumeration and string tables → `data/enums.json` |
| `js/extract_consumables.mjs`, `build_consumables.py` | consumable keys and nominal lives → `data/consumables.json` |
| `js/extract_cloud_calls.mjs`, `build_cloud.py` | cloud / smart-home calls → `data/cloud_calls.json` |
| `js/extract_status_fields.mjs`, `build_status.py` | fields of the status parser → `data/status_fields.json` |
| `js/extract_feature_defs.mjs`, `js/eval_features.mjs`, `js/sandbox.mjs`, `build_models.py` | feature predicates and their evaluation per model → `data/feature_gates.json`, `data/models.json` |
| `js/extract_map_schema.mjs`, `build_map_blocks.py` | block table of the app's map parser → `data/map_blocks.json` |
| `catalog_names.py`, `openhab_models.py`, `legacy_models.py` | name sources → `data/catalog_names.json`, `data/openhab_models.json`, `data/legacy_models.json` |
| `gen_docs.py`, `gen_reference.py`, `gen_devices.py`, `gen_maps.py`, `gen_concepts.py` | Markdown generation (templates + `tools/curated/`) |
| `make_stubs.py` | replaces the old root pages by pointers (reads the old text from git) |
| `gen_legacy.py`, `gen_cloud.py`, `gen_openhab.py`, `examples.py` | generated appendix of legacy captures, the cloud-calls page, the openHAB comparison, and the example builder (typed sample values from the curated request text) used by `gen_docs.py` |
| `check_links.py`, `check_coverage.py` | quality checks |

## Curated text

Hand-written content that the generators merge with the data lives in `tools/curated/`: `categories.yaml` (category of each method), `commands/*.yaml` (per-command semantics, behaviour and legacy comparison), `status_fields.yaml`, `map_blocks.yaml`, `legacy_fw_features.yaml`. Edit these, not the generated pages.

## Data files

| File | Content |
|---|---|
| `data/bundles.json` | one record per bundle: version, SDK, build date, regions, md5, format, module ids |
| `data/commands.json` | one record per method string: evidence per bundle, call shapes, routes |
| `data/enums.json` | states, errors, simple enumerations, string tables |
| `data/consumables.json`, `data/cloud_calls.json` | consumable keys and lives; cloud / smart-home calls |
| `data/openhab_robot_enums.json` | the openHAB binding's robot enumerations (comparison only) |
| `data/status_fields.json` | status fields and which bundles read them |
| `data/feature_gates.json` | predicate definitions, per-model evaluation, feature code uses, feature bit table |
| `data/models.json` | per-model records, product code names, aliases, names |
| `data/map_blocks.json` | map block ids and parsers |
| `data/catalog_names.json`, `data/openhab_models.json`, `data/legacy_models.json` | name sources |

## Notes

- Windows: bundle paths can exceed 260 characters; the unpacker uses extended-length paths.
- Account-id allow lists found in the plugins are never written to the data files.
