#!/usr/bin/env python3
"""Build data/map_blocks.json from the output of js/extract_map_schema.mjs.

usage: python build_map_blocks.py --schema <map_schema.json> --out ../data/map_blocks.json
Records, for every block id the app's own map parser (`*_parser_workermapparser.jx`) knows, its code name, its block header
fields and in which models' plugin it is present; plus the set of block ids per model.
"""
import argparse
import collections
import json
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--schema', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    with open(a.schema, encoding='utf-8') as fh:
        d = json.load(fh)
    blocks = {}
    per_model = {}
    for model, rec in d.items():
        if 'schema' not in rec:
            continue
        ids = sorted(int(i) for i in rec['schema'])
        per_model[model] = dict(file=rec['file'], block_ids=ids, scale=rec.get('scale'), max_block_num=rec.get('maxBlockNum'))
        for i, e in rec['schema'].items():
            b = blocks.setdefault(int(i), dict(names=collections.OrderedDict(), headers=collections.OrderedDict(), models=[]))
            b['names'].setdefault(str(e['type']), []).append(model)
            b['headers'].setdefault(json.dumps(e['header']), []).append(model)
            b['models'].append(model)
    out = dict(meta=dict(generator='tools/build_map_blocks.py', parsers=len(per_model)),
               blocks={str(k): dict(code_names={n: sorted(m) for n, m in v['names'].items()},
                                    headers={h: sorted(m) for h, m in v['headers'].items()},
                                    models=sorted(v['models'])) for k, v in sorted(blocks.items())},
               parsers=per_model)
    with open(a.out, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1)
    print(len(blocks), 'block ids;', len(per_model), 'parsers')


if __name__ == '__main__':
    sys.exit(main())
