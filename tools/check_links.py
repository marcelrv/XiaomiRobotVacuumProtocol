#!/usr/bin/env python3
"""Link checker for all Markdown files of the repository: relative links, images and #anchors.

usage: python tools/check_links.py [--root <repo>]
Anchors are collected from Markdown headings (GitHub slug rules) and from <a id=".."> / <a name=".."> tags.
External links (http/https/mailto) are not fetched. Exit status 1 when something is broken.
"""
import argparse
import os
import re
import sys
import urllib.parse

LINK = re.compile(r'(!?)\[(?:[^\]\\]|\\.)*\]\(\s*(<[^>]*>|[^)\s]*)(?:\s+"[^"]*")?\s*\)')
HEAD = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
ANCH = re.compile(r'<a\s+(?:id|name)="([^"]+)"', re.I)
SKIP_DIRS = {'.git', 'node_modules'}


def slug(text):
    t = re.sub(r'`', '', text)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
    t = t.strip().lower()
    t = re.sub(r'[^\w\- ]', '', t, flags=re.UNICODE)
    return t.replace(' ', '-')


def anchors_of(path, cache={}):
    if path in cache:
        return cache[path]
    seen = {}
    out = set()
    fence = False
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            if line.lstrip().startswith('```'):
                fence = not fence
                continue
            if fence:
                continue
            m = HEAD.match(line)
            if m:
                s = slug(m.group(2))
                n = seen.get(s, 0)
                seen[s] = n + 1
                out.add(s if n == 0 else '%s-%d' % (s, n))
            for a in ANCH.findall(line):
                out.add(a)
    cache[path] = out
    return out


def md_files(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if f.lower().endswith('.md'):
                yield os.path.join(d, f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    root = a.root
    bad = []
    n_links = 0
    n_files = 0
    for f in md_files(root):
        n_files += 1
        fence = False
        with open(f, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
        for ln, line in enumerate(lines, 1):
            if line.lstrip().startswith('```'):
                fence = not fence
                continue
            if fence:
                continue
            clean = re.sub(r'`[^`]*`', '', line)
            for m in LINK.finditer(clean):
                target = m.group(2).strip('<>')
                if re.match(r'^[a-z][a-z0-9+.-]*:', target, re.I) or target.startswith('//'):
                    continue
                n_links += 1
                path, _, frag = target.partition('#')
                path = urllib.parse.unquote(path)
                frag = urllib.parse.unquote(frag)
                dest = f if not path else os.path.normpath(os.path.join(os.path.dirname(f), path))
                rel = os.path.relpath(f, root).replace('\\', '/')
                if not os.path.exists(dest):
                    bad.append('%s:%d: missing file %s' % (rel, ln, target))
                    continue
                if frag and dest.lower().endswith('.md') and os.path.isfile(dest):
                    if frag not in anchors_of(dest):
                        bad.append('%s:%d: missing anchor %s' % (rel, ln, target))
    print('%d markdown files, %d relative links checked, %d problems' % (n_files, n_links, len(bad)))
    for b in bad:
        print(b)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
