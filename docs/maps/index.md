# Maps

[Home](../../README.md) / Maps

Map data has two parts: **how the map is fetched** (RPC + download, [maps overview](../concepts/maps-overview.md)) and **the file format**. The binary assets (samples, viewers, `.ksy`) live in [`RRMapFile/`](../../RRMapFile/) so that existing external links keep working.

| Page | Content |
|---|---|
| [RR map file format](../../RRMapFile/RRFileFormat.md) | block table verified against the app parser (42 parsers), pixel encoding, coordinates |
| [Maps overview](../concepts/maps-overview.md) | fetching, retry loop, incremental maps, multi-floor, coordinates |
| [Map commands](../commands/maps.md) | `get_map_v1`, `get_multi_map`, `save_map`, … |
| [RRMapFile/README.md](../../RRMapFile/README.md) | folder overview and viewer notes |
| [Kaitai description](../../RRMapFile/roborock_map_file.ksy) | `.ksy` (types ≤ 19) |

## See also

- [Rooms and map objects](../commands/rooms-and-areas.md)
- [Methodology](../methodology.md)
