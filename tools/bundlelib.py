"""Helpers to read an unpacked Mi Home (React-Native / Metro) plugin bundle as a set of modules.

Works on the layout produced by unpack_plugins.py:
    <corpus>/<model>/android/main.bundle            (plain bundle: all modules concatenated)
    <corpus>/<model>/android/modules/m<id>.js       (indexed RAM bundle: one file per module)

A module is the text of one  __d(function (...) {...}, <id>, [<dep ids>] [, "<source path>"]);  call.
Source paths are only present in the older plain bundles; RAM bundles carry numeric ids only.
"""
import json
import os
import re

_TAIL_RX = re.compile(r'^\},\s*(\d+)\s*,\s*\[([\d,\s]*)\](?:\s*,\s*"([^"]*)")?\s*\);?\s*$')
_DEP_RX = re.compile(r'_dependencyMap\[(\d+)\]')


class Module:
    __slots__ = ('id', 'deps', 'path', 'text')

    def __init__(self, mid, deps, path, text):
        self.id = mid
        self.deps = deps
        self.path = path
        self.text = text

    def resolved(self):
        """Module text with `_dependencyMap[n]` replaced by the numeric module id (`M<id>`) for readability."""
        deps = self.deps

        def sub(m):
            i = int(m.group(1))
            return 'M%d' % deps[i] if i < len(deps) else m.group(0)
        return _DEP_RX.sub(sub, self.text)


def _parse_tail(tail_line):
    m = _TAIL_RX.match(tail_line.strip())
    if not m:
        return None
    deps = [int(x) for x in m.group(2).replace(' ', '').split(',') if x]
    return int(m.group(1)), deps, m.group(3)


def _split_plain(text):
    mods = []
    cur = None
    for line in text.split('\n'):
        if cur is None:
            if line.startswith('__d(function'):
                cur = [line]
            continue
        cur.append(line)
        if line.startswith('},'):
            t = _parse_tail(line)
            if t:
                mid, deps, path = t
                mods.append(Module(mid, deps, path, '\n'.join(cur)))
                cur = None
    return mods


def load_modules(android_dir):
    """Return dict {module id: Module} for an unpacked bundle directory (the `android` folder)."""
    mods = {}
    mdir = os.path.join(android_dir, 'modules')
    if os.path.isdir(mdir):
        for fn in os.listdir(mdir):
            with open(os.path.join(mdir, fn), encoding='utf-8', errors='replace') as fh:
                text = fh.read()
            last = text.rstrip().rsplit('\n', 1)[-1]
            t = _parse_tail(last) if last.startswith('},') else None
            if t is None:
                m = re.search(r'\},\s*(\d+)\s*,\s*\[([\d,\s]*)\]\s*\);?\s*$', text)
                t = (int(m.group(1)), [int(x) for x in m.group(2).replace(' ', '').split(',') if x], None) if m else None
            if t is None:
                mid = int(re.match(r'm(\d+)\.js', fn).group(1))
                t = (mid, [], None)
            mods[t[0]] = Module(t[0], t[1], t[2], text)
    else:
        with open(os.path.join(android_dir, 'main.bundle'), encoding='utf-8', errors='replace') as fh:
            for m in _split_plain(fh.read()):
                mods[m.id] = m
    return mods


def load_index(corpus):
    with open(os.path.join(corpus, 'INDEX.json'), encoding='utf-8') as fh:
        return json.load(fh)


def models(corpus):
    return sorted(d for d in os.listdir(corpus) if os.path.isdir(os.path.join(corpus, d)))


def android_dir(corpus, model, variant=None):
    if variant:
        return os.path.join(corpus, model, 'variants', variant, 'android')
    return os.path.join(corpus, model, 'android')




_KV_RX = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')
_STRTABLE_RX = re.compile(r'__d\([^\n]*\n\s*module\.exports = \{\s*\n?\s*"')


def _embedded_strings(android, lang):
    """Oldest bundles (1.0.3x) embed every language table as `module.exports = {"key": "text", ...}` modules instead of
    shipping raw/*.json. Only English is supported here: pick the table with the highest share of pure-ASCII values."""
    if lang != 'en' or not os.path.exists(os.path.join(android, 'main.bundle')):
        return {}
    groups = {}   # string namespace (first sorted keys) -> (ascii share, table)
    for m in load_modules(android).values():
        if not _STRTABLE_RX.match(m.text):
            continue
        kv = {}
        for k, v in _KV_RX.findall(m.text):
            try:
                kv[json.loads('"%s"' % k)] = json.loads('"%s"' % v)
            except ValueError:
                pass
        if len(kv) < 200:
            continue
        sig = tuple(sorted(kv)[:3])
        share = sum(1 for v in kv.values() if all(ord(c) < 128 for c in v)) / len(kv)
        if sig not in groups or share > groups[sig][0]:
            groups[sig] = (share, kv)
    out = {}
    for share, kv in sorted(groups.values(), key=lambda g: g[0]):   # most ASCII-like (English) table wins per key
        if share >= 0.85:
            out.update(kv)
    return out


def load_strings(android, lang='en'):
    """Return the app's localisation table (key -> string) for a language, or {} if absent.
    Newer bundles ship raw/*_localizationstrings_<lang>_strings.json; the oldest embed the tables in JS (English only)."""
    out = {}
    raw = os.path.join(android, 'raw')
    if os.path.isdir(raw):
        for fn in os.listdir(raw):
            if fn.endswith('_localizationstrings_%s_strings.json' % lang) or                     re.search(r'_localizationstrings_[a-z]+_%s_strings\.json$' % lang, fn):
                with open(os.path.join(raw, fn), encoding='utf-8-sig') as fh:
                    out.update(json.loads(fh.read().replace(chr(0xa0), ' ')))   # some bundles use NBSP as JSON whitespace
    if not os.path.isdir(os.path.join(android, 'modules')):
        # plain bundles may additionally embed string tables in JS (e.g. the older "sapphire" strings): merge, raw wins
        for k, v in _embedded_strings(android, lang).items():
            out.setdefault(k, v)
    return out
