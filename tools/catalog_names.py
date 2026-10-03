#!/usr/bin/env python3
"""Extract Roborock/Rockrobo marketing names from the Mi Home cloud device catalog (one JSON document per region).

The catalog lists the products Mi Home can pair in a region (model id, display name, status). It is NOT a plugin
list; it is used here only as a *tagged name source* ("Mi Home cloud device catalog").

Expected input: a folder with one JSON document per region. Each document is a JSON object with a `list` array of
device entries; every entry holds at least `model` (string) and `name` (string) and may hold `status`, `pd_id`,
`min_app_version`, `localizations` ({"en": {"name": ...}}). Optional top-level key: `last_modify`.
The region is taken from the file name: --catalog-glob is a pattern in which {region} stands for the region label
(default "*_{region}.json", for example `devices_de.json`).

usage: python catalog_names.py --catalog-dir <folder> [--catalog-glob "*_{region}.json"] [--regions cn,de,in,ru,sg,us]
                               [--exclude-model <model id>]... --out ../data/catalog_names.json
"""
import argparse
import glob
import json
import os
import re

KEEP = ('model', 'name', 'status', 'pd_id', 'min_app_version')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--catalog-dir', required=True, help='folder with one catalog JSON document per region')
    ap.add_argument('--catalog-glob', default='*_{region}.json', help='file name pattern, {region} = region label')
    ap.add_argument('--regions', default='cn,de,in,ru,sg,us', help='comma separated region labels to read')
    ap.add_argument('--exclude-model', action='append', default=[], help='model id to leave out of the output (repeatable)')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    models = {}
    meta = {}
    for region in [r.strip() for r in args.regions.split(',') if r.strip()]:
        for f in sorted(glob.glob(os.path.join(args.catalog_dir, args.catalog_glob.replace('{region}', region)))):
            with open(f, encoding='utf-8') as fh:
                d = json.load(fh)
            R = region.upper()
            meta[R] = dict(last_modify=d.get('last_modify'), entries=len(d['list']))
            for x in d['list']:
                m = str(x.get('model', ''))
                if not m.startswith(('roborock.', 'rockrobo.')) or m in args.exclude_model:
                    continue
                rec = models.setdefault(m, {})
                rec[R] = {k: x.get(k) for k in KEEP if k in x}
                loc = x.get('localizations')
                if isinstance(loc, dict) and 'en' in loc:
                    rec[R]['name_en_localization'] = loc['en'].get('name') if isinstance(loc['en'], dict) else loc['en']
    out = dict(source='Mi Home cloud device catalog (per region)', catalogs=meta,
               models={k: models[k] for k in sorted(models)})
    with open(args.out, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(len(models), 'roborock/rockrobo models in the catalog')


if __name__ == '__main__':
    main()
