#!/usr/bin/env python3
"""Run the whole extraction pipeline: plugin zips -> corpus -> raw extractor output -> data/*.json.

usage:
  python tools/run_pipeline.py --plugins-root <folder with the downloaded plugin zips per region> --work <scratch dir>
         [--region-dir-prefix <prefix>] [--data-out <folder>] [--catalog-dir <folder with the per-region device catalog JSON>]
         [--catalog-glob "*_{region}.json"] [--exclude-model <model id>] [--node node] [--steps all]
         [--openhab <path to org.openhab.binding.miio>] [--legacy-ref be636c7]

Steps (in order; use --steps unpack,rpc to run a subset):
  unpack    tools/unpack_plugins.py --variants          -> <work>/corpus
  catalog   tools/catalog_names.py                       -> data/catalog_names.json
  openhab   tools/openhab_models.py (needs --openhab)    -> data/openhab_models.json
  legacy    tools/legacy_models.py                       -> data/legacy_models.json
  rpc       tools/js/extract_rpc.mjs                     -> <work>/rpc
  enums     tools/js/extract_enums.mjs                   -> <work>/enums
  status    tools/js/extract_status_fields.mjs           -> <work>/status
  cons      tools/js/extract_consumables.mjs             -> <work>/cons
  cloud     tools/js/extract_cloud_calls.mjs             -> <work>/cloud
  fdefs     tools/js/extract_feature_defs.mjs            -> <work>/fdefs
  feat      tools/js/eval_features.mjs (every bundle)    -> <work>/feat
  maps      tools/js/extract_map_schema.mjs + build_map_blocks.py -> data/map_blocks.json
  build     build_commands / build_enums / build_status / build_models -> data/
The JS steps need `npm install` once in tools/js. Nothing from the bundles is copied into the repository.
"""
import argparse
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, 'tools')
ALL = ['unpack', 'catalog', 'openhab', 'legacy', 'rpc', 'enums', 'status', 'cons', 'cloud', 'fdefs', 'feat', 'maps', 'build']


def run(cmd, **kw):
    print('+', ' '.join(cmd), flush=True)
    subprocess.run(cmd, check=True, **kw)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--plugins-root', help='folder with the downloaded plugin zips, one sub-folder per region (needed for the unpack step only)')
    ap.add_argument('--data-out', help='folder for the generated data/*.json (default: data/ of the repository); name-source files already present in data/ are copied there when missing')
    ap.add_argument('--region-dir-prefix', default='', help='prefix of the region sub-folders of --plugins-root')
    ap.add_argument('--catalog-dir', help='folder with one Mi Home cloud device catalog JSON per region (step catalog)')
    ap.add_argument('--catalog-glob', default='*_{region}.json', help='catalog file name pattern, {region} = region label')
    ap.add_argument('--exclude-model', action='append', default=[], help='model id to leave out of the catalog names (repeatable)')
    ap.add_argument('--work', required=True)
    ap.add_argument('--node', default='node')
    ap.add_argument('--corpus', help='corpus folder (default <work>/corpus)')
    ap.add_argument('--steps', default='all')
    ap.add_argument('--openhab')
    ap.add_argument('--openhab-ref', default='main', help='git ref of the openHAB checkout to compare with (default main)')
    ap.add_argument('--legacy-ref', default='be636c7')
    a = ap.parse_args()
    steps = ALL if a.steps == 'all' else a.steps.split(',')
    py = sys.executable
    corpus = a.corpus or os.path.join(a.work, 'corpus')
    data = a.data_out or os.path.join(ROOT, 'data')
    os.makedirs(data, exist_ok=True)
    if os.path.abspath(data) != os.path.join(ROOT, 'data'):
        import shutil
        for fn in ('catalog_names.json', 'openhab_models.json', 'legacy_models.json'):
            if not os.path.exists(os.path.join(data, fn)) and os.path.exists(os.path.join(ROOT, 'data', fn)):
                shutil.copy(os.path.join(ROOT, 'data', fn), os.path.join(data, fn))
    os.makedirs(a.work, exist_ok=True)
    js = os.path.join(T, 'js')
    env = dict(os.environ, PYTHONUTF8='1')
    if 'unpack' in steps:
        if not a.plugins_root:
            ap.error('--plugins-root is required for the unpack step (use --corpus with --steps rpc,... to reuse an unpacked corpus)')
        run([py, os.path.join(T, 'unpack_plugins.py'), '--plugins-root', a.plugins_root, '--region-dir-prefix', a.region_dir_prefix, '--out', corpus, '--variants'], env=env)
    if 'catalog' in steps and a.catalog_dir:
        cmd = [py, os.path.join(T, 'catalog_names.py'), '--catalog-dir', a.catalog_dir, '--catalog-glob', a.catalog_glob, '--out', os.path.join(data, 'catalog_names.json')]
        for m in a.exclude_model:
            cmd += ['--exclude-model', m]
        run(cmd, env=env)
    if 'openhab' in steps and a.openhab:
        run([py, os.path.join(T, 'openhab_models.py'), '--openhab', a.openhab, '--ref', a.openhab_ref, '--out', os.path.join(data, 'openhab_models.json')], env=env)
    if 'legacy' in steps:
        run([py, os.path.join(T, 'legacy_models.py'), '--ref', a.legacy_ref, '--out', os.path.join(data, 'legacy_models.json')], env=env, cwd=ROOT)
    for step, script, out in (('rpc', 'extract_rpc.mjs', 'rpc'), ('enums', 'extract_enums.mjs', 'enums'), ('status', 'extract_status_fields.mjs', 'status'), ('cons', 'extract_consumables.mjs', 'cons'), ('cloud', 'extract_cloud_calls.mjs', 'cloud')):
        if step in steps:
            run([a.node, script, corpus, os.path.join(a.work, out)], cwd=js)
    if 'fdefs' in steps:
        run([a.node, 'extract_feature_defs.mjs', corpus, os.path.join(a.work, 'rpc'), os.path.join(a.work, 'fdefs')], cwd=js)
    if 'feat' in steps:
        os.makedirs(os.path.join(a.work, 'feat'), exist_ok=True)
        for f in sorted(glob.glob(os.path.join(a.work, 'rpc', '*.json'))):
            bid = os.path.basename(f)[:-5]
            model = bid.split('@')[0]
            run([a.node, 'eval_features.mjs', corpus, os.path.join(a.work, 'rpc'), bid, os.path.join(a.work, 'feat', bid + '.json'), model], cwd=js)
    if 'maps' in steps:
        run([a.node, 'extract_map_schema.mjs', corpus, os.path.join(a.work, 'map_schema.json')], cwd=js)
        run([py, os.path.join(T, 'build_map_blocks.py'), '--schema', os.path.join(a.work, 'map_schema.json'), '--out', os.path.join(data, 'map_blocks.json')], env=env)
    if 'build' in steps:
        run([py, os.path.join(T, 'build_commands.py'), '--corpus', corpus, '--rpc', os.path.join(a.work, 'rpc'), '--out', data], env=env)
        run([py, os.path.join(T, 'build_enums.py'), '--corpus', corpus, '--enums', os.path.join(a.work, 'enums'), '--out', os.path.join(data, 'enums.json')], env=env)
        if os.path.exists(os.path.join(T, 'build_status.py')):
            run([py, os.path.join(T, 'build_status.py'), '--status', os.path.join(a.work, 'status'), '--corpus', corpus, '--out', os.path.join(data, 'status_fields.json')], env=env)
        if os.path.isdir(os.path.join(a.work, 'cons')):
            run([py, os.path.join(T, 'build_consumables.py'), '--cons', os.path.join(a.work, 'cons'), '--corpus', corpus, '--out', os.path.join(data, 'consumables.json')], env=env)
        if os.path.isdir(os.path.join(a.work, 'cloud')):
            run([py, os.path.join(T, 'build_cloud.py'), '--cloud', os.path.join(a.work, 'cloud'), '--corpus', corpus, '--out', os.path.join(data, 'cloud_calls.json')], env=env)
        run([py, os.path.join(T, 'build_models.py'), '--work', a.work, '--data', data], env=env)


if __name__ == '__main__':
    main()
