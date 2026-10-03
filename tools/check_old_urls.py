#!/usr/bin/env python3
"""URL-stability check: every path (and every named heading anchor) that exists at a base git ref must still resolve.

usage: python tools/check_old_urls.py [--base origin/master] [--root <repo>] [--show-generic]

External projects link to this repository's root-level pages and their anchors. For every file in the tree of
the base ref the script checks that the file still exists in the working tree and, for Markdown files, that every
heading anchor of the old version still exists in the new version (GitHub slug rules, plus <a id=".."> tags).
The anchors of the old per-command skeleton (`command`, `example`, `response` and their numbered variants,
`example-1`, `command-2`, ...) are generic and reported only as a count. Exit status 1 when a path or a named anchor is gone.
"""
import argparse
import collections
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_links as L  # noqa: E402

GENERIC = re.compile(r'^(command|example|response)(-\d+)*$')


def git(root, *args):
    return subprocess.run(['git', '-C', root] + list(args), capture_output=True, check=True).stdout


def old_anchors(text):
    out = set()
    seen = collections.Counter()
    fence = False
    for line in text.splitlines():
        if line.lstrip().startswith('```'):
            fence = not fence
            continue
        if fence:
            continue
        m = L.HEAD.match(line)
        if m:
            s = L.slug(m.group(2))
            n = seen[s]
            seen[s] += 1
            out.add(s if n == 0 else '%s-%d' % (s, n))
        out.update(L.ANCH.findall(line))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--base', default='origin/master', help='git ref holding the published layout (default origin/master)')
    ap.add_argument('--root', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--show-generic', action='store_true', help='also list the generic skeleton anchors that are gone')
    a = ap.parse_args()

    names = [n for n in git(a.root, 'ls-tree', '-r', '--name-only', a.base).decode('utf-8').splitlines() if n]
    missing, lost, generic = [], [], []
    anchors_total = 0
    for rel in names:
        path = os.path.join(a.root, rel)
        if not os.path.exists(path):
            missing.append(rel)
            continue
        if not rel.lower().endswith('.md'):
            continue
        old = old_anchors(git(a.root, 'show', '%s:%s' % (a.base, rel)).decode('utf-8', errors='replace'))
        new = L.anchors_of(path)
        for anchor in sorted(old):
            anchors_total += 1
            if anchor in new:
                continue
            (generic if GENERIC.match(anchor) else lost).append((rel, anchor))

    print('%d paths at %s, %d missing; %d heading anchors, %d named anchors lost, %d generic skeleton anchors gone'
          % (len(names), a.base, len(missing), anchors_total, len(lost), len(generic)))
    for rel in missing:
        print('MISSING PATH   ', rel)
    for rel, anchor in lost:
        print('LOST ANCHOR    %s#%s' % (rel, anchor))
    if a.show_generic:
        for rel, anchor in generic:
            print('generic anchor %s#%s' % (rel, anchor))
    return 1 if missing or lost else 0


if __name__ == '__main__':
    sys.exit(main())
