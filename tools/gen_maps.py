"""Generate RRMapFile/RRFileFormat.md (the map file format) and docs/maps/index.md.
Called from gen_docs.py (`run(ctx, G)`). Block availability comes from data/map_blocks.json (the app's own parser),
layouts from tools/curated/map_blocks.yaml."""
import collections
import json
import os

import yaml


def run(ctx, G):
    mb = G.load_json('map_blocks.json')
    cur = yaml.safe_load(open(os.path.join(G.CUR, 'map_blocks.yaml'), encoding='utf-8'))['blocks']
    parsers = mb['parsers']
    total = len(parsers)
    # parser generations: models grouped by their block id set
    gens = collections.defaultdict(list)
    for m, p in parsers.items():
        gens[tuple(p['block_ids'])].append(m)
    gen_rows = sorted(gens.items(), key=lambda kv: len(kv[0]))

    L = ['# Roborock map file format (RR map)', '',
         '[Home](../README.md) / [Maps](../docs/maps/index.md) / RR map file format', '',
         'The map the robot produces is a **gzip-compressed** binary file ("RR file") consisting of a header and a sequence of typed blocks. '
         'In Mi Home the file is not returned by the RPC: the RPC returns a file name, the plugin downloads the object and un-gzips it '
         '([how](../docs/concepts/maps-overview.md#how-a-map-reaches-the-app)).', '',
         'This page was verified against the **app\'s own map parser** shipped in every plugin bundle '
         '(`raw/*_parser_workermapparser.jx`, `Schema` table, %d parsers; method: [methodology](../docs/methodology.md)). '
         'Layouts marked *confirmed* agree with the legacy text, *extended* means the legacy text was incomplete, *new* means the block was not documented before. '
         'The machine-readable block table is [`data/map_blocks.json`](../data/map_blocks.json); a Kaitai description is [`roborock_map_file.ksy`](roborock_map_file.ksy) '
         '(it covers block types ≤ 19 only and is unchanged).' % total, '',
         '## Conventions', '',
         '- All integers are little-endian.', '',
         '<a id="coordinates"></a>',
         '- **Coordinates** stored in the file are millimetres; the app divides them by `Scale = 50` to get map pixels (one pixel = 50 mm). '
         'Zones and points sent *to* the robot ([`app_zoned_clean`](../docs/commands/cleaning-control.md#app_zoned_clean), '
         '[`app_goto_target`](../docs/commands/cleaning-control.md#app_goto_target)) use the same millimetre frame.',
         '- "scaled" below means the app divides the value by 50. Obstacle coordinates are **not** scaled in the app.',
         '- The y axis of the file points up while image rows count downwards: for a position at image row `r` the app uses `y = top + height − r` '
         '(pixel units; ✅ Bundle · a65 m12218 `getZoneParams`, `getGotoTarget`).', '',
         '## Framing', '',
         'The parser reads blocks sequentially. Every block starts with a prefix:', '',
         '| Offset | Size | Field |', '|---:|---:|---|',
         '| 0 | 2 | block type |', '| 2 | 2 | header length (bytes from the start of the block to the payload) |', '| 4 | 4 | payload length |', '',
         'The next block starts at `start + header length + payload length`. Block fields listed as *header* below follow the prefix inside the header; '
         'the *record* layout describes the payload. Unknown block types are skipped by length.', '',
         '<a id="file-header"></a>', '### File header and validation', '',
         'The file begins with a block of type `0x7272` (the ASCII characters `rr`) whose header carries:', '',
         '| Field | Size |', '|---|---:|', '| major version | 2 |', '| minor version | 2 |', '| map index | 4 |', '| map sequence | 4 |', '',
         'so the file header is 20 bytes long (header length field = 0x14 in the samples of the legacy text). '
         'Before decoding, the app checks the downloaded file (✅ Bundle · a65@1.0.95 · m10052 `MapValidator`; the validator, recognised by its SHA-1 routine and function names, is present in all 42 bundles; a65 is quoted):', '',
         '1. the first two bytes are the ASCII text `rr`;',
         '2. `header length + payload length` (u16 at offset 2, u32 at offset 4) equals the length of the whole file, i.e. the payload length of the file header is the length of **everything after the file header**, not an offset to a footer as the legacy text said;',
         '3. the last 20 bytes of the file equal the SHA-1 of all bytes in front of them (the digest table of the validator lists map version 1.0 in all readable bundles and 1.1 in all of them except a11, m1s, p5, t4, t6 and v1; the digest-table lines of the minified bundles were not read);',
         '4. the lengths of all following blocks add up to the payload length.', '',
         '⚪ Legacy documented the same header fields ("0x00 `RR`, 0x02 header length, 0x04 data length, 0x08 major, 0x0A minor, 0x0C map index, 0x10 sequence").', '',
         '## Block types', '',
         'Parsers = how many of the %d analysed parsers know the block.' % total, '',
         '| Id | Name used by the app | Legacy name | Title | Header fields | Record layout | Parsers | Status |', '|---:|---|---|---|---|---|---:|---|']
    for i_s, b in mb['blocks'].items():
        i = int(i_s)
        if i == 29298:
            continue
        c = cur.get(i, {})
        names = '/'.join('`%s`' % n for n in b['code_names'])
        L.append('| %d | %s | `%s` | %s | %s | %s | %d | %s |' % (i, names, c.get('legacy_id', ''), c.get('title', ''), c.get('header', ''), c.get('record', ''), len(b['models']), c.get('status', '❓')))
    L += ['', '### Notes per block', '']
    for i, c in sorted(cur.items()):
        if c.get('note'):
            L.append('- **%d %s**: %s' % (i, c['title'], c['note']))
    L += ['', '## Pixel values of the image block (type 2)', '',
          '| Bits | Meaning |', '|---|---|',
          '| 0–2 (`pixel & 7`) | pixel type: `0` outside/unknown, `1` obstacle/wall, any other non-zero value = floor |',
          '| 3–7 (`pixel >> 3`) | room (segment) id, 0–31; `0` = no room |', '',
          '✅ Bundle · `convertMap` of the app parser; the .ksy declares the same split (`segment_id` b5, `type` b3). '
          'The legacy table "00 outside, 01 wall, FF inside" is the special case type 7 / room 31.', '',
          '## Obstacle types', '',
          'The `type` field of blocks 13–16 is mapped to a display name by the app; the table is in [other enumerations](../docs/reference/other-enums.md#obstaclenames) '
          '(the bundles that carry the table are listed there).', '',
          '## Parser generations', '',
          'Models whose plugin parser knows the same set of block ids (extra ids relative to the first row):', '',
          '| Block ids known | Count | Models |', '|---|---:|---|']
    base = None
    for ids, ms in gen_rows:
        label = ('%d block ids + file header 0x7272: ' % len([x for x in ids if x != 29298])) + (', '.join(str(x) for x in ids if x not in (base or ()) and x != 29298) or 'base set')
        L.append('| %s | %d | %s |' % (label, len(ms), ' '.join(G.short(m) for m in sorted(ms, key=G.natkey))))
        base = ids
    L += ['', 'Which of these ids a *firmware* writes is not determinable from the bundles; the table shows what the app can decode. '
          'The legacy note "map v1.1 / blocks 9–12 only with newer firmware" matches the generation split above (blocks 11 and 12 appear in every parser except the first one).', '',
          '## Files in this folder', '',
          '| File | What it is |', '|---|---|',
          '| [`roborock_map_file.ksy`](roborock_map_file.ksy) | Kaitai Struct description (block types 1–19 and 1024) |',
          '| [`RRDraw.java`](RRDraw.java) | proof-of-concept drawing code (legacy) |',
          '| [`roboMapViewer2.5.7.zip`](roboMapViewer2.5.7.zip), [`roboMapViewer2.5.9-1.zip`](roboMapViewer2.5.9-1.zip) | offline viewers (legacy; the newer one also decodes identified obstacles) |',
          '| `roboroommap%252F55512646%252F6.rrmap` (this folder), [`../roboroommap-with-objects.rrmap`](../roboroommap-with-objects.rrmap) (repository root) | sample map files (the first file name contains a literal `%252F`, so it is not linked) |',
          '| `DecodedSample.png`, `decodedRegion.png`, `rrmap-v11.jpg`, `robomapobjects.png` | decoded examples |', '',
          'Source of the offline viewer (openHAB binding): <https://github.com/openhab/openhab-addons/tree/main/bundles/org.openhab.binding.miio>. '
          'Latest viewer: [openHAB forum thread](https://community.openhab.org/t/xiaomi-vacuum-map-viewer-to-find-coordinates-for-zone-cleaning/103500).', '',
          '![decoded sample](DecodedSample.png "Decoded with concept reader with goto")',
          '![decoded regions](decodedRegion.png "Decoded with concept reader with regions")',
          '![map v1.1](rrmap-v11.jpg "Decoded with concept reader for map v1.1")',
          '![map objects](robomapobjects.png "Decoded map with objects")', '',
          '## See also', '', '- [Maps overview](../docs/concepts/maps-overview.md)', '- [Map commands](../docs/commands/maps.md)', '- [README of this folder](README.md)', '']
    G.OUT['RRMapFile/RRFileFormat.md'] = '\n'.join(L)

    I = ['# Maps', '', '[Home](../../README.md) / Maps', '',
         'Map data has two parts: **how the map is fetched** (RPC + download, [maps overview](../concepts/maps-overview.md)) and **the file format**. '
         'The binary assets (samples, viewers, `.ksy`) live in [`RRMapFile/`](../../RRMapFile/) so that existing external links keep working.', '',
         '| Page | Content |', '|---|---|',
         '| [RR map file format](../../RRMapFile/RRFileFormat.md) | block table verified against the app parser (%d parsers), pixel encoding, coordinates |' % total,
         '| [Maps overview](../concepts/maps-overview.md) | fetching, retry loop, incremental maps, multi-floor, coordinates |',
         '| [Map commands](../commands/maps.md) | `get_map_v1`, `get_multi_map`, `save_map`, … |',
         '| [RRMapFile/README.md](../../RRMapFile/README.md) | folder overview and viewer notes |',
         '| [Kaitai description](../../RRMapFile/roborock_map_file.ksy) | `.ksy` (types ≤ 19) |', '',
         '## See also', '', '- [Rooms and map objects](../commands/rooms-and-areas.md)', '- [Methodology](../methodology.md)', '']
    G.OUT['docs/maps/index.md'] = '\n'.join(I)

    R = ['# RR map file: format description and proof-of-concept reader', '',
         '[Home](../README.md) / [Maps](../docs/maps/index.md) / RRMapFile', '',
         'This folder keeps the binary assets (sample maps, viewers, Kaitai description) at their original paths. '
         'The format description is [RRFileFormat.md](RRFileFormat.md) (verified against the app parser, see [methodology](../docs/methodology.md)).', '',
         '- [roborock_map_file.ksy](roborock_map_file.ksy) is a [Kaitai](https://kaitai.io) struct for the map format that can be used to generate parsing code or to inspect a file in the [web IDE](https://ide.kaitai.io/). '
         'It covers block types up to 19 and 1024; types 20-34 and 36 are described in [RRFileFormat.md](RRFileFormat.md) only.',
         '- Offline viewer [roboMapViewer2.5.7.zip](roboMapViewer2.5.7.zip): `java -jar RoboMapviewer2.5.7.jar` (java in the path, viewer in the current directory, otherwise add the paths).',
         '- [roboMapViewer2.5.9-1.zip](roboMapViewer2.5.9-1.zip): updated version that also decodes the identified obstacles. '
         'The latest viewer is on the [openHAB forum](https://community.openhab.org/t/xiaomi-vacuum-map-viewer-to-find-coordinates-for-zone-cleaning/103500).',
         '- Source of the offline viewer (included in the openHAB miio binding): <https://github.com/openhab/openhab-addons/blob/2.5.x/bundles/org.openhab.binding.miio/src/test/java/org/openhab/binding/miio/internal/RoboMapViewer.java>', '',
         '![example picture](DecodedSample.png "Decoded with concept reader with goto")',
         '![example picture](decodedRegion.png "Decoded with concept reader with regions")', '',
         'Decoded with concept reader for map v1.1', '',
         '![example picture](rrmap-v11.jpg "Decoded with concept reader for map v1.1")',
         '![example picture](robomapobjects.png "Decoded map with objects")', '',
         '## See also', '', '- [Maps overview](../docs/concepts/maps-overview.md)', '- [Map commands](../docs/commands/maps.md)', '']
    G.OUT['RRMapFile/README.md'] = '\n'.join(R)
