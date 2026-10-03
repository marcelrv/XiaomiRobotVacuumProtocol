#!/usr/bin/env python3
"""Extract what the *pre-existing* repo text said about models (prior art, tagged "legacy", unverified).

usage: python legacy_models.py --ref be636c7 --out ../data/legacy_models.json
Parses README.md (supported-devices table) and fw_features.md (model / name / firmware / feature-flag matrix) from a git
revision, so that the data stays reproducible after those files have been rewritten.
"""
import argparse
import json
import subprocess
import sys

ROW = '|'


def git_show(ref, path):
    return subprocess.run(['git', 'show', f'{ref}:{path}'], capture_output=True, text=True, encoding='utf-8', check=True).stdout


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    models = {}
    for line in git_show(args.ref, 'README.md').splitlines():
        if line.startswith('| ') and ('roborock.' in line or 'rockrobo.' in line):
            c = cells(line)
            if len(c) >= 2 and (c[0].startswith('roborock.') or c[0].startswith('rockrobo.')):
                models.setdefault(c[0], {})['readme_name'] = c[1]
    fw_codes = []
    for line in git_show(args.ref, 'fw_features.md').splitlines():
        if line.startswith('| Model'):
            fw_codes = [x for x in cells(line)[3:-1]]
        elif line.startswith('| ') and (line[2:].startswith('roborock.') or line[2:].startswith('rockrobo.')):
            c = cells(line)
            rec = models.setdefault(c[0], {})
            rec['fw_features_name'] = c[1]
            rec['fw_features_firmware'] = c[2] or None
            flags = c[3:3 + len(fw_codes)]
            rec['fw_features_codes_marked'] = [int(code) for code, f in zip(fw_codes, flags) if f.upper() == 'X' and code.isdigit()]
    out = dict(source=f'pre-existing README.md and fw_features.md at git revision {args.ref}', status='legacy, unverified',
               models=dict(sorted(models.items())))
    with open(args.out, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(len(models), 'models')


if __name__ == '__main__':
    sys.exit(main())
