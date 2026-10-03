# Maps overview

[Home](../../README.md) / Concepts / Maps overview

A Roborock map is not returned by an RPC: the RPC names a file, the plugin downloads and decodes it. This page explains the fetch flow, the coordinate system that every map-related call shares, and the exact parameter layout the plugin uses to send virtual walls and forbidden zones back to the robot. The file format itself is in [RR map file format](../../RRMapFile/RRFileFormat.md). Primary source: a65 (plugin 1.0.95): `RRMISDK` m10046, map downloader m10109, `MapValidator` m10052, map editor m12218 / m14318; other bundles checked by script where stated.

## Pieces

| Piece | Where documented |
|---|---|
| RPCs that return map file names or data | [maps commands](../commands/maps.md) (`get_map_v1`, `get_map`, `get_multi_map`, `get_recover_map`, `get_photo`, …) |
| RPCs that edit maps | [maps commands](../commands/maps.md), [rooms and map objects](../commands/rooms-and-areas.md), [carpet](../commands/carpet.md) |
| The binary map file | [RR map file format](../../RRMapFile/RRFileFormat.md), [maps index](../maps/index.md) |
| State fields that describe the loaded map | [status fields](../reference/status-fields.md#maps) |

<a id="how-a-map-reaches-the-app"></a>
## How a map reaches the app

Inside Mi Home (`RRMISDK.isMiApp`) the plugin runs `downloadMap(method, params)` (✅ Bundle · a65 m10109):

1. Send the RPC (`get_map_v1`, `get_multi_map` or `get_recover_map`; `get_clean_record_map` uses the same route).
2. Read the object name: classic reply `result[0]` (the plugin replaces `%2F` by `/`); with incremental maps (below) the reply is an object `{"result": "ok"|"retry", "nonce", "file", "snapshot"}` and the name is `file`.
3. If the name is `locating` or empty, the attempt ends **without calling back** (the robot is relocating; the UI keeps its loading state).
4. If the name is `retry`: wait 1 s and send the request again (for incremental maps with the nonce from the previous reply). The counter allows at most 8 retries; afterwards the call fails with "retry times exceeded the max retry count".
5. Otherwise ask the Mi Home cloud service for a download address (`smarthome.getMapfileUrl({model, obj_name})`), download the file to `map.gz` (for `get_multi_map`: `map<NN>.gz` where `NN` are the last two characters of the object name), un-gzip it with the host file API and validate it ([file validation](../../RRMapFile/RRFileFormat.md#file-header-and-validation)).
6. Any exception retries the whole request after 2 s while the retry counter allows, then fails with "mi download map data failed".

So a third party that talks to the robot directly (local miIO) receives only the object name and needs its own way to fetch the file; the bundles show the cloud route only. The file arrives gzip-compressed.

The Roborock app (not Mi Home) uses a different native path (`RRPluginSDK.getMapData`) with the same validation; its branches are visible in the code but not analysed here.

### The newer encrypted path (`get_map`, `get_photo`)

The map (`get_map`, newer generation-B plugins) and the obstacle photos (`get_photo`; also present in the generation-A plugins of a08 a09 a10 a11 a19 s4 s5e s6) are requested through `getRobotData` / `getAndDecBase64Data` (a65 m12806 `downloadFile`, m10046). The request carries a freshly generated public key and a cipher-suite number; the robot's reply is again the object name in `result[0]` (with the same `retry` handling), the plugin downloads that object, reads it as base64, decrypts it and decompresses it (`get_map`: LZ4; `get_photo`: gzip). The key handling is part of the plugin's worker code and is deliberately not documented here. [`get_random_pkey`](../commands/maps.md#get_random_pkey) returns a key used by the record viewer. Which models answer `get_map` is not shown by the bundles; the app calls it in the 22 generation-B bundles listed in the [`get_map` entry](../commands/maps.md#get_map).

<a id="incremental-maps"></a>
## Incremental maps

If the robot announces the feature (`isSupportIncrementalMap`: bit 13 of the low 8 hex digits of `new_feature_info_str` in Mi Home, [feature flags](feature-flags.md#feature-word-new_feature_info_str)), `get_map_v1` is sent with `{"nonce": <n>}` (`-1` for the first request) and the plugin keeps the nonce of the last accepted map. A `retry` reply carries a `snapshot` that the plugin parses and a new nonce. Once per plugin session, when the retry counter exceeds 2, the plugin resets the nonce to `-1`. [`get_dynamic_map_diff`](../commands/maps.md#get_dynamic_map_diff) and [`get_dynamic_data`](../commands/maps.md#get_dynamic_data) are the per-layer variants.

## Map state in `get_status`

`map_status` packs two values: `map_status % 4` is the status (0 none, 1 map without rooms, 3 map with rooms) and `map_status >> 2` is the id of the loaded saved map (63 means "none", shown as -1). `lab_status` is 1 while map saving is on and 3 with multi-floor. The robot state `LOCKED` (103, "saving map") makes some calls wait: the plugin polls once a second, at most 5 times, for it to clear (for example before a go-to). See [states](../reference/states.md), [status fields](../reference/status-fields.md#maps).

## Multi-floor maps

With multi-floor support (firmware feature code 120, [feature flags](feature-flags.md#feature-codes)) the robot keeps several saved maps. The plugin lists them with [`get_multi_maps_list`](../commands/maps.md#get_multi_maps_list) (`max_multi_map`, `map_info[]` with `mapFlag`), shows one with [`get_multi_map`](../commands/maps.md#get_multi_map), switches with [`load_multi_map`](../commands/maps.md#load_multi_map), renames with [`name_multi_map`](../commands/maps.md#name_multi_map) and backs up or restores with the `recover` calls. Where firmware reports it, backup copies of a map are addressed with an extra flag (`isSupportBackupMap`). `load_multi_map` is one of the calls covered by the [retry protocol](transports.md#retry-protocol).

<a id="coordinates"></a>
## Coordinates

All map-related requests and the map file use one frame:

- Map file positions are millimetres; the plugin divides by `50` to get pixels (one pixel = 50 mm).
- The file's y axis points up, image rows count down. For an element placed at pixel offset `(px, py)` inside the image of a map with `left`, `top`, `height` (all from the image block header) the plugin sends
  `x = (left + px) × 50` and `y = (top + height − py) × 50` (✅ Bundle · a65 m12218 `getGotoTarget`, `getZoneParams`, `_mapOffsetToSlam`).
- Zones are sent as `[x1, y1, x2, y2]` with `x1 < x2` and `y1 < y2` in that frame (the lower-left corner first), in millimetres rounded to whole pixels × 50.
- Obstacle positions in map blocks 13-16 are already in millimetres and are not divided; the plugin hides obstacles within 300 mm of the charger and obstacles that are in the ignore list.

See also [zoned clean](../commands/cleaning-control.md#app_zoned_clean) and [go-to](../commands/cleaning-control.md#app_goto_target).

<a id="virtual-walls-and-forbidden-zones"></a>
## Virtual walls and forbidden zones

The map editor sends walls and zones with [`save_map`](../commands/maps.md#save_map). `params` is an array of arrays built as `walls.concat(zones)`; in a multi-floor setup two marker rows follow (`[100, <map id>]`, and `[200, 0]` when the home map is saved). Each row (✅ Bundle · a65 m12218 `getWallsParams`, `getFBZParams`, `_getSingleFBZoneParams`; all values millimetres as above):

| Row | Layout | Meaning |
|---|---|---|
| virtual wall | `[1, x1, y1, x2, y2]` | wall between two end points |
| no-go zone | `[0, x1, y1, x2, y2, x3, y3, x4, y4]` | `FBZ_TYPE_REGULAR`; the four corners of the (possibly rotated) rectangle, order: upper left, upper right, lower right, lower left in the editor's frame |
| no-mop zone | `[2, x1, y1, …, x4, y4]` | `FBZ_TYPE_MOPPING` |
| "cleaning" forbidden zone | `[3, x1, y1, …, x4, y4]` | `FBZ_TYPE_CLEANING`; the editor shows it only for the product line the plugin calls `Garnet` (`isGarnet`) |
| AI-edit point | `[4, x, y]` | one point |
| cliff zone, editable | `[0, x1, y1, …, x4, y4]` | appended after the AI points (same type value as a no-go zone); non-editable cliff zones come from a separate function (`getCliffZones`) with type value `1` |

Other editor actions use separate calls: carpet ignore zones ([`set_ignore_carpet_zone`](../commands/carpet.md), object `{"map_index", "zone_data"}`), door sills, stuck points and cliff zones ([rooms and map objects](../commands/rooms-and-areas.md)). The block ids under which the robot reports these elements in the map file are in [RR map file format](../../RRMapFile/RRFileFormat.md#block-types).

How many walls or zones the editor allows is decided by `isFBZsReachMaxNum` in the plugin; the limits were not extracted. The set of zone kinds a particular robot offers is gated per product ([feature matrix](../devices/matrix-features.md)).

## Rooms (segments)

The map image carries room ids in the upper five bits of every pixel (0 = none, up to 31). [`get_room_mapping`](../commands/rooms-and-areas.md#get_room_mapping) maps those ids to the robot's room numbers, [`app_segment_clean`](../commands/cleaning-control.md#app_segment_clean) cleans them by id, and [`merge_segment`](../commands/rooms-and-areas.md#merge_segment), [`split_segment`](../commands/rooms-and-areas.md#split_segment), [`name_segment`](../commands/rooms-and-areas.md#name_segment) edit them (these three are in the retry list).

## Map editing session

A map edit is bracketed by [`start_edit_map`](../commands/maps.md#start_edit_map) and [`end_edit_map`](../commands/maps.md#end_edit_map). Map operations report failures with the codes of `mapOpErrorCode` ([errors](../reference/errors.md#map-operation-errors-mapoperrorcode)), for example `-10005` parameter error and `-105` "exceed room max count" for room edits.

## See also

- [RR map file format](../../RRMapFile/RRFileFormat.md)
- [Maps commands](../commands/maps.md)
- [Transports and dispatch](transports.md)
- [Feature flags](feature-flags.md)
