#!/usr/bin/env python3
"""Build data/consumables.json from js/extract_consumables.mjs output.

usage: python build_consumables.py --cons <dir> --corpus <corpus> --out ../data/consumables.json
Per consumable key: nominal life as written in the plugin, whether the life is a time (hours) or a count, the English
display name (from the bundle's string table) and the models (best bundles) whose plugin defines it.
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bundlelib as B  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cons', required=True)
    ap.add_argument('--corpus', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    index = B.load_index(a.corpus)
    items = collections.OrderedDict()
    for model in sorted(index):
        p = os.path.join(a.cons, model + '.json')
        if not os.path.exists(p):
            continue
        rows = json.load(open(p, encoding='utf-8'))
        if not rows:
            continue
        en = B.load_strings(B.android_dir(a.corpus, model, None), 'en')
        for r in rows:
            rec = items.setdefault(r['key'], dict(key=r['key'], variants=collections.OrderedDict()))
            v = (r['total'], r['unitsTime'], en.get(r['nameKey'] or '', ''))
            rec['variants'].setdefault(json.dumps(v), []).append(model)
    consumables = []
    for k, rec in items.items():
        vs = []
        for v, ms in rec['variants'].items():
            total, units_time, name = json.loads(v)
            vs.append(dict(total=total, units_time=units_time, name=name, models=ms))
        consumables.append(dict(key=k, variants=vs))
    out = dict(meta=dict(generator='tools/build_consumables.py', note='bundles whose plugin has a consumables page definition (generation B); older plugins use a different page that was not extracted'),
               consumables=consumables)
    with open(a.out, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(len(items), 'consumable keys')


if __name__ == '__main__':
    main()
