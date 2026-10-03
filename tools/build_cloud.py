#!/usr/bin/env python3
"""Build data/cloud_calls.json: cloud / smart-home calls of the plugins (calls that are not miIO RPCs).

usage: python build_cloud.py --cloud <dir of js/extract_cloud_calls.mjs output> --corpus <corpus> --out ../data/cloud_calls.json
Only the best bundle of every model is counted. Per call: kind, the models whose plugin contains it, up to three
(module, enclosing function) call sites.
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
    ap.add_argument('--cloud', required=True)
    ap.add_argument('--corpus', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    calls = collections.OrderedDict()
    for model in sorted(B.load_index(a.corpus)):
        p = os.path.join(a.cloud, model + '.json')
        if not os.path.exists(p):
            continue
        for r in json.load(open(p, encoding='utf-8')):
            k = (r['kind'], r['name'])
            rec = calls.setdefault(k, dict(kind=r['kind'], name=r['name'], models=[], sites=[]))
            if model not in rec['models']:
                rec['models'].append(model)
            if len(rec['sites']) < 3 and not any(s['model'] == model for s in rec['sites']):
                rec['sites'].append(dict(model=model, module=r['module'], enclosing=r['enclosing']))
    out = dict(meta=dict(generator='tools/build_cloud.py'), calls=sorted(calls.values(), key=lambda r: (r['kind'], r['name'])))
    with open(a.out, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(len(calls), 'cloud call kinds')


if __name__ == '__main__':
    main()
