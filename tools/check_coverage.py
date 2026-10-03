#!/usr/bin/env python3
"""Coverage and regression checks.

1. every method string of data/commands.json appears in the command documentation and every command heading of the
   documentation exists in the data;
2. regression test for the call-site detection (classification called / wrapper-only):
   a. data-only: call sites known from reading the bundles must be classified "called" (see KNOWN_CALLED);
   b. with --corpus <unpacked corpus>: for every best bundle and every method classified "wrapper only", the wrapper
      function names must not be called from any module other than the wrapper modules (`<x>.<fn>(` member calls).

usage: python tools/check_coverage.py [--corpus <corpus folder>] [--data <data folder>]
Exit status 1 if anything fails.
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (model short id, method): a call site exists in that bundle (verified by reading the code; each was missed once by the extractor)
KNOWN_CALLED = [
    ('a27', 'set_timer'), ('a69', 'set_timer'), ('a76', 'set_server_timer'), ('a27', 'app_get_wifi_list'),
    ('t4', 'app_segment_clean'), ('t6', 'app_get_init_status'), ('t4', 'app_get_init_status'),
    ('a10', 'get_photo'), ('a27', 'get_photo'), ('a26', 'get_photo'), ('s6', 'get_photo'), ('a27', 'get_map'),
]


# (model short id, predicate, expected class set): the model-group helpers of the older plugins must be evaluated for the bundle's model
KNOWN_GATES = [('t4', 'isCameraSupported', {'N'}), ('t6', 'isCameraSupported', {'N'}), ('s5', 'isCameraSupported', {'N'}),
               ('a09', 'isCameraSupported', {'Y'}), ('a10', 'isCameraSupported', {'Y'}), ('a26', 'isCameraSupported', {'Y'}), ('a27', 'isCameraSupported', {'Y'}),
               ('a10', 'isVideoMonitorSupported', {'RA'})]


TAIL = re.compile(r'^\},\s*(\d+)\s*,\s*\[')


def module_texts(android):
    """(module id, text) of every module of an unpacked bundle: RAM bundles are one file per module; plain bundles are split at the
    Metro `__d(function ... },<id>,[deps])` boundaries."""
    md = os.path.join(android, 'modules')
    if os.path.isdir(md):
        for fn in os.listdir(md):
            m = re.match(r'm(\d+)\.js$', fn)
            if m:
                with open(os.path.join(md, fn), encoding='utf-8', errors='ignore') as fh:
                    yield int(m.group(1)), fh.read()
    else:
        cur = None
        with open(os.path.join(android, 'main.bundle'), encoding='utf-8', errors='ignore') as fh:
            for line in fh:
                if cur is None:
                    if line.startswith('__d(function'):
                        cur = [line]
                    continue
                cur.append(line)
                m = TAIL.match(line)
                if m:
                    yield int(m.group(1)), ''.join(cur)
                    cur = None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--corpus')
    ap.add_argument('--data', default=os.path.join(ROOT, 'data'))
    args = ap.parse_args()
    bad = False
    with open(os.path.join(args.data, 'commands.json'), encoding='utf-8') as fh:
        cmds = json.load(fh)['methods']
    methods = set(cmds)
    documented = set()
    headings = set()
    for f in glob.glob(os.path.join(ROOT, 'docs', 'commands', '*.md')):
        base = os.path.basename(f)
        if base == 'index.md':
            continue
        t = open(f, encoding='utf-8').read()
        documented |= set(re.findall(r'^### `([^`]+)`', t, re.M))
        documented |= set(re.findall(r'<a id="([^"]+)"></a>', t))
        documented |= set(re.findall(r'`(user\.[A-Za-z0-9_]+)`', t))
        if base != 'alternate-table.md':
            headings |= set(re.findall(r'^### `([^`]+)`', t, re.M))
    missing = sorted(methods - documented)
    unknown = sorted(headings - methods)
    print('%d methods in data, %d command headings in docs' % (len(methods), len(headings)))
    if missing:
        print('in data but not documented:', missing)
        bad = True
    if unknown:
        print('documented but not in data:', unknown)
        bad = True
    # 2a
    fails = [(m, x) for m, x in KNOWN_CALLED if cmds[x]['per_bundle'].get('roborock.vacuum.' + m, {}).get('status') != 'called']
    if fails:
        print('known call sites not classified as called:', fails)
        bad = True
    else:
        print('regression (data): %d known call sites classified as called' % len(KNOWN_CALLED))
    # example lint: no minified variable names or string placeholders in place of the parameters
    lint = []
    for f in glob.glob(os.path.join(ROOT, 'docs', 'commands', '*.md')):
        for ln, line in enumerate(open(f, encoding='utf-8').read().splitlines(), 1):
            if line.startswith('{"id": 1, "method"') and (re.search(r'"<[a-z]{1,2}>"', line) or '"params": "<' in line):
                lint.append('%s:%d' % (os.path.basename(f), ln))
    if lint:
        print('example lint failed (placeholder values):', lint[:10])
        bad = True
    else:
        print('lint (examples): no minified placeholders or string params')
    # gate evaluation regression (older plugins used to evaluate as 'always true')
    gp = os.path.join(args.data, 'feature_gates.json')
    if os.path.exists(gp):
        ev = json.load(open(gp, encoding='utf-8'))['evaluation']
        gfails = [(m, p, ev['roborock.vacuum.' + m]['predicates'].get(p, {}).get('cls')) for m, p, want in KNOWN_GATES
                  if ev['roborock.vacuum.' + m]['predicates'].get(p, {}).get('cls') not in want]
        if gfails:
            print('feature gate regression failed:', gfails)
            bad = True
        else:
            print('regression (gates): %d known gate classes as expected' % len(KNOWN_GATES))
    # 2b
    if args.corpus:
        n = rev = 0
        index = {}          # bundle -> (names called as <x>.default.<name>( / RobotApi.<name>( outside the wrapper modules, string literals outside them)
        call_rx = re.compile(r'(?:\.default|\bRobotApi)\.([A-Za-z_$][\w$]*)\(')
        lit_rx = re.compile(r"['\"]([a-z][a-z0-9_.]{3,})['\"]")
        for x, rec in cmds.items():
            for bid, row in rec['per_bundle'].items():
                if '@' in bid or row['status'] not in ('wrapper', 'called'):
                    continue
                android = os.path.join(args.corpus, bid, 'android')
                if not os.path.isdir(android):
                    continue
                mods = set(row.get('wrapper_modules') or [])
                if bid not in index:
                    names, lits = set(), set()
                    for mid, text in module_texts(android):
                        if mid in mods:
                            continue
                        names.update(call_rx.findall(text))
                        lits.update(lit_rx.findall(text))
                    index[bid] = (names, lits)
                names, lits = index[bid]
                outside_api = any(a in names for a in (row.get('api') or []))
                if row['status'] == 'wrapper':
                    if outside_api:
                        print('wrapper-only but called outside the wrapper module: %s %s' % (bid, x))
                        bad = True
                    n += 1
                else:
                    # reverse test: a "called" pair needs a wrapper call, a literal or a Methods-key use outside the wrapper modules
                    if not (outside_api or row.get('lit') or row.get('ref') or x in lits):
                        print('classified called but no evidence outside the wrapper module: %s %s' % (bid, x))
                        bad = True
                    rev += 1
        print('regression (corpus): %d wrapper-only pairs and %d called pairs checked (RAM and plain bundles)' % (n, rev))
    else:
        print('regression (corpus): skipped (pass --corpus to run it)')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
