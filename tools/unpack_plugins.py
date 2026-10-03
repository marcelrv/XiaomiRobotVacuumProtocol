#!/usr/bin/env python3
"""Unpack Roborock/Rockrobo Mi Home plugin bundles into a greppable plain-JS corpus.

Input : a folder with the downloaded plugin zips per region: one sub-folder per Mi Home region, named
        <region-dir-prefix><REGION> (default: no prefix, every sub-folder is a region and its name the label, e.g. CN, DE; see --region-dir-prefix).
        Two file name forms are accepted:
          * the name the Mi Home cloud serves (last URL path segment):
              signed_<sdk>_<n>_<n>_ANDROID_bundle_<md5>.zip
            This name does not contain the model id, so the zip must lie in a sub-folder that is named after the model
            (<region folder>/<model>/signed_...zip);
          * the same name with a local "<model>-v2-" prefix (the convention of some download tools), anywhere below the
            region folder:
              roborock.vacuum.a15-v2-signed_10042_1004367_27_ANDROID_bundle_<md5>.zip
            (a "-v1-" prefix marks an old native-Android plugin; these are listed but not unpacked).
Output: <out>/<model>/android/{project.json, main.bundle, raw/*, [modules/m<id>.js, _startup.js]}
        <out>/<model>/variants/<first 8 hex of hash>/android/...   (only with --variants: every other distinct bundle hash)
        <out>/INDEX.json   (inventory: every zip seen, hashes, regions, project.json of each variant)

By default only the bundle with the highest (SDK level, build) is unpacked per model ("best").
Binary assets (png/jpg/mp3/...) are skipped; only code and JSON/text resources are kept.

Metro "indexed RAM bundles" (magic 0xFB0BD1E5) are split into modules/m<id>.js.
Plain bundles are left as one main.bundle (see bundlelib.py for module splitting).

No proprietary code is meant to be committed to the repository: point --out at a scratch folder.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import sys
import zipfile

MODEL_PAT = r'(?:roborock|rockrobo)\.[a-z]+\.[a-z0-9_]+'
NAME_RX = re.compile(r'^(' + MODEL_PAT + r')-(v\d)-(.+)\.zip$', re.I)      # <model>-v2-<cloud name>.zip
CLOUD_RX = re.compile(r'^(signed_.+)\.zip$', re.I)                          # <cloud name>.zip (model = parent folder)
MODEL_RX = re.compile(r'^' + MODEL_PAT + r'$', re.I)
META_RX = re.compile(r'signed_(\d+)_(\d+)_(\d+)_ANDROID_bundle_([0-9a-f]{32})')
SKIP_EXT = ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.html', '.ttf', '.otf', '.mp3', '.wav', '.ogg')
RAM_MAGIC = 0xFB0BD1E5


def scan(root, model_rx, region_prefix=''):
    """Return {model: [record,...]} for every plugin zip below root/<region_prefix><REGION>/ ."""
    cands = {}
    for region in sorted(os.listdir(root)):
        if not region.lower().startswith(region_prefix.lower()) or not os.path.isdir(os.path.join(root, region)):
            continue
        for dp, _dn, fn in os.walk(os.path.join(root, region)):
            for f in fn:
                m = NAME_RX.match(f)
                if m:
                    model, ver, rest = m.groups()
                else:
                    m = CLOUD_RX.match(f)
                    parent = os.path.basename(dp)
                    if not m or not MODEL_RX.match(parent):
                        if f.lower().endswith('.zip') and f.startswith('signed_'):
                            print('skipped (model unknown, put the zip in a <model>/ folder): %s' % os.path.join(dp, f))
                        continue
                    model, ver, rest = parent, 'v2', m.group(1)
                if not model_rx.search(model):
                    continue
                mm = META_RX.match(rest)
                if mm:
                    sdk, dev, build, h = mm.groups()
                    key = (int(sdk), int(build))
                else:
                    sdk = dev = build = None
                    h = rest
                    key = (0, 0)
                cands.setdefault(model, []).append(dict(
                    model=model, ver=ver, path=os.path.join(dp, f), region=region[len(region_prefix):],
                    hash=h, key=key, sdk=sdk, dev=dev, build=build, file=f))
    return cands


def longpath(p):
    """Windows: add the extended-length prefix so paths beyond MAX_PATH (260 chars) work."""
    if os.name == 'nt':
        p = os.path.abspath(p)
        prefix = '\\\\?\\'
        if not p.startswith(prefix):
            return prefix + p
    return p


def extract_zip(zpath, dest):
    with zipfile.ZipFile(zpath) as zf:
        for n in zf.namelist():
            if n.endswith('/') or n.lower().endswith(SKIP_EXT):
                continue
            target = longpath(os.path.join(dest, *n.split('/')))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with zf.open(n) as src, open(target, 'wb') as dst:
                shutil.copyfileobj(src, dst)


def split_ram_bundle(bundle_path):
    """Split a Metro indexed RAM bundle into modules/m<id>.js and _startup.js. Returns module count."""
    with open(bundle_path, 'rb') as fh:
        b = fh.read()
    if struct.unpack('<I', b[:4])[0] != RAM_MAGIC:
        return None
    cnt, sup = struct.unpack('<II', b[4:12])
    tbl = struct.unpack('<%dI' % (cnt * 2), b[12:12 + cnt * 8])
    base = 12 + cnt * 8
    outdir = os.path.join(os.path.dirname(bundle_path), 'modules')
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for i in range(cnt):
        off, ln = tbl[2 * i], tbl[2 * i + 1]
        if not ln:
            continue
        with open(os.path.join(outdir, 'm%d.js' % i), 'wb') as fh:
            fh.write(b[base + off:base + off + ln].rstrip(b'\0'))
        n += 1
    with open(os.path.join(os.path.dirname(bundle_path), '_startup.js'), 'wb') as fh:
        fh.write(b[base:base + sup].rstrip(b'\0'))
    return n


def unpack_variant(rec, dest):
    dest = longpath(dest)
    extract_zip(rec['path'], dest)
    info = dict(file=rec['file'], hash=rec['hash'], sdk_in_name=rec['sdk'], build_in_name=rec['build'],
                regions=None, project=None, format=None, modules=None, main_bundle_md5=None)
    for dp, _dn, fn in os.walk(dest):
        if 'project.json' in fn and info['project'] is None:
            try:
                with open(os.path.join(dp, 'project.json'), encoding='utf-8-sig') as fh:
                    info['project'] = json.load(fh)
            except Exception as exc:  # noqa: BLE001
                info['project'] = {'_error': str(exc)}
        if 'main.bundle' in fn:
            mb = os.path.join(dp, 'main.bundle')
            n = split_ram_bundle(mb)
            info['format'] = 'indexed-ram' if n is not None else 'plain-js'
            info['modules'] = n
            with open(mb, 'rb') as fh:
                info['main_bundle_md5'] = hashlib.md5(fh.read()).hexdigest()
    return info


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--plugins-root', required=True, help='folder with the downloaded plugin zips, one sub-folder per region')
    ap.add_argument('--region-dir-prefix', default='', help='only sub-folders whose name starts with this prefix are regions; the rest of the name is the region label (default: empty = every sub-folder)')
    ap.add_argument('--out', required=True, help='output corpus folder (created)')
    ap.add_argument('--models', default=r'.', help='regex filter on model id (default: all)')
    ap.add_argument('--variants', action='store_true',
                    help='also unpack every other distinct bundle hash into <model>/variants/<hash>/')
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    cands = scan(args.plugins_root, re.compile(args.models), args.region_dir_prefix)
    index = {}
    for model, recs in sorted(cands.items()):
        v2 = [r for r in recs if r['ver'] == 'v2']
        by_hash = {}
        for r in v2:
            by_hash.setdefault(r['hash'], []).append(r)
        regions = {}
        for r in recs:
            regions.setdefault(r['hash'], set()).add(r['region'])
        entry = dict(best=None, variants=[],
                     all=[dict(hash=h, regions=sorted(s)) for h, s in regions.items()],
                     legacy_v1_files=sorted({r['file'] for r in recs if r['ver'] == 'v1'}),
                     all_files=sorted({r['file'] for r in recs}))
        if v2:
            info = best = None
            bad = entry.setdefault('unreadable_zips', [])
            for cand in sorted(v2, key=lambda r: r['key'], reverse=True):   # newest first; skip corrupt / partial downloads
                try:
                    info = unpack_variant(cand, os.path.join(args.out, model))
                    best = cand
                    break
                except zipfile.BadZipFile:
                    bad.append(cand['file'])
                    shutil.rmtree(longpath(os.path.join(args.out, model)), ignore_errors=True)
            if best is None:
                index[model] = entry
                print('%-24s no readable v2 zip: %s' % (model, bad))
                continue
            info['regions'] = sorted(regions[best['hash']])
            entry['best'] = info
            if args.variants:
                for h, rs in by_hash.items():
                    if h == best['hash']:
                        continue
                    r = sorted(rs, key=lambda x: x['key'])[-1]
                    try:
                        vi = unpack_variant(r, os.path.join(args.out, model, 'variants', h[:8]))
                    except zipfile.BadZipFile:
                        bad.append(r['file'])
                        continue
                    vi['regions'] = sorted(regions[h])
                    entry['variants'].append(vi)
        index[model] = entry
        b = entry['best'] or {}
        print('%-24s %-12s modules=%-5s version=%s hashes=%d' % (
            model, b.get('format'), b.get('modules'), (b.get('project') or {}).get('version'), len(entry['all'])))
    with open(os.path.join(args.out, 'INDEX.json'), 'w', encoding='utf-8') as fh:
        json.dump(index, fh, indent=1, default=str)


if __name__ == '__main__':
    sys.exit(main())
