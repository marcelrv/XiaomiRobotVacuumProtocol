#!/usr/bin/env python3
"""Build data/status_fields.json: which fields of the status object each bundle's RobotStatusManager.parseStatus() reads.

usage: python build_status.py --status <dir of js/extract_status_fields.mjs output> --corpus <corpus> --out ../data/status_fields.json
Only the best bundle of every model is used. Each field lists the models that read it and the short assignment
expressions (<=120 chars) found in parseStatus (evidence of how the app interprets the value).
"""
import argparse
import collections
import glob
import json
import os
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--status', required=True)
    ap.add_argument('--corpus', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    with open(os.path.join(a.corpus, 'INDEX.json'), encoding='utf-8') as fh:
        models = sorted(json.load(fh))
    fields = collections.defaultdict(lambda: dict(models=[], uses={}))
    for m in models:
        p = os.path.join(a.status, m + '.json')
        if not os.path.exists(p):
            continue
        with open(p, encoding='utf-8') as fh:
            res = json.load(fh)
        for r in res:
            for f, uses in r['fields'].items():
                rec = fields[f]
                if m not in rec['models']:
                    rec['models'].append(m)
                for u in uses:
                    key = ('%s <- %s' % (u['target'], u['expr']) if u['target'] else u['expr'])[:60]
                    rec['uses'].setdefault(key, []).append(m)
    out = dict(meta=dict(generator='tools/build_status.py', models=len(models)),
               fields={f: dict(models=v['models'], uses=[dict(use=k, models=ms[:3] + (['…'] if len(ms) > 3 else [])) for k, ms in list(v['uses'].items())[:4]])
                       for f, v in sorted(fields.items())})
    with open(a.out, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(len(out['fields']), 'status fields')


if __name__ == '__main__':
    sys.exit(main())
