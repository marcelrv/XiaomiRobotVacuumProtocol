# Rooms, zones and map objects

[Home](../../README.md) / [Commands](index.md) / Rooms, zones and map objects

Room (segment) tables and editing, furniture and floor-material recognition, carpet areas, door sills and smart scenes.

Rooms are called **segments** in the protocol. Segment ids come from the map file (see [maps](../maps/index.md)) and from
[`get_room_mapping`](#get_room_mapping). Newer bundles keep all map-object edits (carpet areas, door sills, furniture,
floor material, cliff, stuck points) as separate calls that carry the map id (`map_index` / `map_flag`) of the map being
edited (`replaceId` in the plugin code).

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`get_room_mapping`](#get_room_mapping) | Returns, per room, the segment number and the room id of the cloud/IoT room it is assigned to. | ✅ Bundle |
| [`merge_segment`](#merge_segment) | Merges the selected rooms into one. | ✅ Bundle |
| [`split_segment`](#split_segment) | Splits a room along a line drawn in the editor. | ✅ Bundle |
| [`name_segment`](#name_segment) | Writes the room names (via room tags) to the robot. | ✅ Bundle |
| [`manual_segment_map`](#manual_segment_map) | Turns the automatic room division of a map into a manual (editable) one. | ✅ Bundle |
| [`get_segment_status`](#get_segment_status) | Wrapped in every bundle; no call site. | ✅ Bundle (wrapper only) |
| [`set_scenes_segments`](#set_scenes_segments) | Registers a smart-scene task for rooms. | ✅ Bundle |
| [`set_scenes_zones`](#set_scenes_zones) | Registers a smart-scene task for rectangular zones. | ✅ Bundle |
| [`get_scenes_valid_tids`](#get_scenes_valid_tids) | Returns the task ids the robot knows. | ✅ Bundle |
| [`reunion_scenes`](#reunion_scenes) | Tells the robot which task ids are valid on the cloud side. | ✅ Bundle |
| [`save_furnitures`](#save_furnitures) | Writes the edited furniture list of a map. | ✅ Bundle |
| [`set_identify_furniture_status`](#set_identify_furniture_status) | Turns furniture recognition on or off. | ✅ Bundle |
| [`get_identify_furniture_status`](#get_identify_furniture_status) | Reads the switch. | ✅ Bundle |
| [`set_segment_ground_material`](#set_segment_ground_material) | Stores the floor type per room. | ✅ Bundle |
| [`set_identify_ground_material_status`](#set_identify_ground_material_status) | Turns floor-material recognition on or off. | ✅ Bundle |
| [`get_identify_ground_material_status`](#get_identify_ground_material_status) | Reads the switch. | ✅ Bundle |
| [`set_ignore_identify_area`](#set_ignore_identify_area) | Marks recognised obstacles as ignored. | ✅ Bundle |
| [`set_carpet_area`](#set_carpet_area) | Saves user-added carpet zones. | ✅ Bundle |
| [`set_ignore_carpet_zone`](#set_ignore_carpet_zone) | Saves zones where carpet detection is ignored. | ✅ Bundle |
| [`app_set_door_sill_blocks`](#app_set_door_sill_blocks) | Saves manual door-sill (threshold) blocks. | ✅ Bundle |
| [`app_set_smart_door_sill`](#app_set_smart_door_sill) | Saves the automatic door-sill areas. | ✅ Bundle |
| [`app_set_ignore_stuck_point`](#app_set_ignore_stuck_point) | Saves points where the robot's stuck detection is ignored. | ✅ Bundle |
| [`app_set_smart_cliff_forbidden`](#app_set_smart_cliff_forbidden) | Saves areas treated as cliff-forbidden. | ✅ Bundle |

<a id="get_room_mapping"></a>
### `get_room_mapping` — Room number to room name mapping

Returns, per room, the segment number and the room id of the cloud/IoT room it is assigned to.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`); a01 passes `{}`.

**Response**

`result` is an array of arrays. The first element of each is the segment number; the second is the id the plugin
uses as `iotRoomId` (Roborock app) or `miRoomId` (Mi Home) when naming rooms; newer firmware appends further columns
(the plugin indexes `roomMapping[i][1]` and `[i][2]` as the tag id, ✅ Bundle · a65 m10112).

**Example** — legacy capture (unverified)

```json
{"result": [[16, "<room id>"], [17, "<room id>"]], "id": 14837}
```

**Legacy documentation**

⚪ Legacy [room_mapping.md](../../room_mapping.md) — consistent; the README lists it as "s5e, m1s".

**Related:** [`name_segment`](rooms-and-areas.md#name_segment), [`app_segment_clean`](cleaning-control.md#app_segment_clean)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getRoomNameMappingInfo`); call sites m10112; table key `GetRoomMapping` · anchor `"GetRoomMapping"`
- `a65@1.0.95` · wrapper m10115 (`getRoomNameMappingInfo`); call sites m10112; table key `GetRoomMapping` · anchor `"GetRoomMapping"`
- `t4@1.0.32` · wrapper m10010 (`getRoomNameMappingInfo`); call sites m10553, m10886; table key `GetRoomMapping` · anchor `"GetRoomMapping"`

</details>

<a id="merge_segment"></a>
### `merge_segment` — Merge rooms

Merges the selected rooms into one.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: the array of selected segment ids (at least 2), `mergeList` of the map editor (a65 m14327).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Behaviour in the app**

In the retry list ([transports](../concepts/transports.md#retry-protocol)). After success the app re-downloads the map.

**Related:** [`split_segment`](rooms-and-areas.md#split_segment), [`name_segment`](rooms-and-areas.md#name_segment)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`mergeSegment`); call sites m14357; table key `MergeSegment` · anchor `"MergeSegment"`
- `a65@1.0.95` · wrapper m10115 (`mergeSegment`); call sites m14327; table key `MergeSegment` · anchor `"MergeSegment"`
- `t4@1.0.32` · call sites m10886; table key `MergeSegment` · anchor `"MergeSegment"`

</details>

<a id="split_segment"></a>
### `split_segment` — Split a room

Splits a room along a line drawn in the editor.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: the object `splitParams.info` produced by the editor (segment id and the two line end points; the layout is internal to the map editor, ❓ not decoded).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Behaviour in the app**

Retry-capable; app re-downloads the map afterwards.

**Related:** [`merge_segment`](rooms-and-areas.md#merge_segment)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`splitSegment`); call sites m14357; table key `SplitSegment` · anchor `"SplitSegment"`
- `a65@1.0.95` · wrapper m10115 (`splitSegment`); call sites m14327; table key `SplitSegment` · anchor `"SplitSegment"`
- `t4@1.0.32` · call sites m10886; table key `SplitSegment` · anchor `"SplitSegment"`

</details>

<a id="name_segment"></a>
### `name_segment` — Name rooms

Writes the room names (via room tags) to the robot.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: an array of objects `{"miRoomId" | "iotRoomId": <id>, "robotRoomId": <segment id>, "robotTagId": <tag id>}`
(`miRoomId` in Mi Home, `iotRoomId` in the Roborock app; ✅ Bundle · a65 m10112 `addZoneParams`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Behaviour in the app**

Retry-capable. The app then calls `get_room_mapping` again to refresh its cache. Room-name tags need new-feature bit `isRoomNameSupported` (low word bit 14).

**Related:** [`get_room_mapping`](rooms-and-areas.md#get_room_mapping)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`nameSegment`); call sites m10112, m14357; table key `NameSegment` · anchor `"NameSegment"`
- `a65@1.0.95` · wrapper m10115 (`nameSegment`); call sites m10112, m14327; table key `NameSegment` · anchor `"NameSegment"`
- `t4@1.0.32` · call sites m10886; table key `NameSegment` · anchor `"NameSegment"`

</details>

<a id="manual_segment_map"></a>
### `manual_segment_map` — Switch to manual room division

Turns the automatic room division of a map into a manual (editable) one.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 40: a01 a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 c1 e2 p5 s4 s5 s5e s6 t4 t6 model(s) |
| Other bundles | wrapper only: 2: m1s v1 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"map_flag": <map id>}` with multi-floor, otherwise `[]`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "manual_segment_map", "params": {"map_flag": 0}}
```

**Related:** [`merge_segment`](rooms-and-areas.md#merge_segment), [`split_segment`](rooms-and-areas.md#split_segment)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`manualSegmentMap`); call sites m12539, m14348, m14357; table key `ManualSegmentMap` · anchor `"ManualSegmentMap"`
- `a65@1.0.95` · wrapper m10115 (`manualSegmentMap`); call sites m12527, m14318, m14327; table key `ManualSegmentMap` · anchor `"ManualSegmentMap"`
- `t4@1.0.32` · wrapper m10010 (`manualSegmentMap`); call sites m10964; table key `ManualSegmentMap` · anchor `"ManualSegmentMap"`

</details>

<a id="get_segment_status"></a>
### `get_segment_status` — Segment status (wrapped, unused)

Wrapped in every bundle; no call site.

| | |
|---|---|
| Evidence | ✅ Bundle (wrapper only) — no call site found in the bundles |
| Other bundles | wrapper only: all 42 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_segment_status", "params": []}
```

**Related:** [`get_room_mapping`](rooms-and-areas.md#get_room_mapping)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getSegmentStatus`); table key `GetSegmentStatus` · anchor `"GetSegmentStatus"`
- `a65@1.0.95` · wrapper m10115 (`getSegmentStatus`); table key `GetSegmentStatus` · anchor `"GetSegmentStatus"`
- `t4@1.0.32` · wrapper m10010 (`getSegmentStatus`); table key `GetSegmentStatus` · anchor `"GetSegmentStatus"`

</details>

<a id="set_scenes_segments"></a>
### `set_scenes_segments` — Smart scene: rooms

Registers a smart-scene task for rooms.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[{"tid": <task id>, "segs": [{"sid": <segment id>}, …]}]`; the reply `result[0].tid` is the robot-side task id; the app then adds `fan_power` / `water_box_mode` to each returned segment.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_scenes_segments", "params": [{"tid": 1, "segs": [{"sid": 1}]}]}
```

**Behaviour in the app**

Smart scenes need new-feature bit `isSupportSmartScene` (high word bit 1).

**Related:** [`set_scenes_zones`](rooms-and-areas.md#set_scenes_zones), [`get_scenes_valid_tids`](rooms-and-areas.md#get_scenes_valid_tids), [`reunion_scenes`](rooms-and-areas.md#reunion_scenes)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setScenesSegment`); call sites m13997, m14003 · anchor `"set_scenes_segments"`
- `a65@1.0.95` · wrapper m10115 (`setScenesSegment`); call sites m13982, m13988 · anchor `"set_scenes_segments"`
- `a62@1.0.69` · wrapper m10109 (`setScenesSegment`); call sites m13952 · anchor `"set_scenes_segments"`

</details>

<a id="set_scenes_zones"></a>
### `set_scenes_zones` — Smart scene: zones

Registers a smart-scene task for rectangular zones.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[{"tid": <task id>, "zones": [{"range": <rect>, "zid": <id>}, …]}]`.

**Response**

`result[0] = {"tid", "zones": [ … ]}`.

**Related:** [`set_scenes_segments`](rooms-and-areas.md#set_scenes_segments)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setScenesZone`); call sites m13997, m14003 · anchor `"set_scenes_zones"`
- `a65@1.0.95` · wrapper m10115 (`setScenesZone`); call sites m13982, m13988 · anchor `"set_scenes_zones"`
- `a62@1.0.69` · wrapper m10109 (`setScenesZone`); call sites m13952 · anchor `"set_scenes_zones"`

</details>

<a id="get_scenes_valid_tids"></a>
### `get_scenes_valid_tids` — List valid scene task ids

Returns the task ids the robot knows.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`{}`).

**Response**

`result` is an array of objects with a `tid` field.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_scenes_valid_tids", "params": {}}
```

**Related:** [`reunion_scenes`](rooms-and-areas.md#reunion_scenes)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getScenes`); call sites m12539, m14507 · anchor `"get_scenes_valid_tids"`
- `a65@1.0.95` · wrapper m10115 (`getScenes`); call sites m12527, m14477 · anchor `"get_scenes_valid_tids"`
- `a62@1.0.69` · wrapper m10109 (`getScenes`); call sites m13418 · anchor `"get_scenes_valid_tids"`

</details>

<a id="reunion_scenes"></a>
### `reunion_scenes` — Re-sync scene tasks

Tells the robot which task ids are valid on the cloud side.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |
| Call-site gate | the call sits behind `isSupportSmartScene` (tests found in the enclosing code of the call sites; [feature flags](../concepts/feature-flags.md)) |

**Request**

`params`: `[{"tid": <id>}, …]` (the intersection of robot and cloud ids).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "reunion_scenes", "params": [{"tid": 1}]}
```

**Related:** [`get_scenes_valid_tids`](rooms-and-areas.md#get_scenes_valid_tids)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`reunionScenes`); call sites m13997, m14003 · anchor `"reunion_scenes"`
- `a65@1.0.95` · wrapper m10115 (`reunionScenes`); call sites m13982, m13988 · anchor `"reunion_scenes"`
- `a62@1.0.69` · wrapper m10109 (`reunionScenes`); call sites m13952 · anchor `"reunion_scenes"`

</details>

<a id="save_furnitures"></a>
### `save_furnitures` — Save furniture objects

Writes the edited furniture list of a map.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"map_flag": <map id>, "data": <furniture array>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Behaviour in the app**

Needs new-feature bit `isSupportFurniture` (high word bit 4).

**Related:** [`set_identify_furniture_status`](rooms-and-areas.md#set_identify_furniture_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`saveFurnitureEditZones`); call sites m10112 · anchor `"save_furnitures"`
- `a65@1.0.95` · wrapper m10115 (`saveFurnitureEditZones`); call sites m10112 · anchor `"save_furnitures"`
- `a62@1.0.69` · wrapper m10109 (`saveFurnitureEditZones`); call sites m12038 · anchor `"save_furnitures"`

</details>

<a id="set_identify_furniture_status"></a>
### `set_identify_furniture_status` — Furniture recognition switch

Turns furniture recognition on or off.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"status": 0|1}`. The app sets floor-material recognition first and furniture recognition second.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_identify_furniture_status", "params": {"status": 1}}
```

**Related:** [`get_identify_furniture_status`](rooms-and-areas.md#get_identify_furniture_status), [`set_identify_ground_material_status`](rooms-and-areas.md#set_identify_ground_material_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setFurnitureIdentifyStatus`); call sites m14285 · anchor `"set_identify_furniture_status"`
- `a65@1.0.95` · wrapper m10115 (`setFurnitureIdentifyStatus`); call sites m14255 · anchor `"set_identify_furniture_status"`
- `a62@1.0.69` · wrapper m10109 (`setFurnitureIdentifyStatus`); call sites m13820 · anchor `"set_identify_furniture_status"`

</details>

<a id="get_identify_furniture_status"></a>
### `get_identify_furniture_status` — Furniture recognition switch (read)

Reads the switch.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.status == 1` means on (an object, not an array).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_identify_furniture_status", "params": []}
```

**Related:** [`set_identify_furniture_status`](rooms-and-areas.md#set_identify_furniture_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getFurnitureIdentifyStatus`); call sites m14285 · anchor `"get_identify_furniture_status"`
- `a65@1.0.95` · wrapper m10115 (`getFurnitureIdentifyStatus`); call sites m14255 · anchor `"get_identify_furniture_status"`
- `a62@1.0.69` · wrapper m10109 (`getFurnitureIdentifyStatus`); call sites m13820 · anchor `"get_identify_furniture_status"`

</details>

<a id="set_segment_ground_material"></a>
### `set_segment_ground_material` — Set room floor material

Stores the floor type per room.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"data": <array of per-room floor entries>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`set_identify_ground_material_status`](rooms-and-areas.md#set_identify_ground_material_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`saveFloorMaterial`); call sites m14390 · anchor `"set_segment_ground_material"`
- `a65@1.0.95` · wrapper m10115 (`saveFloorMaterial`); call sites m14360 · anchor `"set_segment_ground_material"`
- `a62@1.0.69` · wrapper m10109 (`saveFloorMaterial`); call sites m13904 · anchor `"set_segment_ground_material"`

</details>

<a id="set_identify_ground_material_status"></a>
### `set_identify_ground_material_status` — Floor-material recognition switch

Turns floor-material recognition on or off.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"status": 0|1}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_identify_ground_material_status", "params": {"status": 1}}
```

**Related:** [`get_identify_ground_material_status`](rooms-and-areas.md#get_identify_ground_material_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setFloorIdentifyStatus`); call sites m14285 · anchor `"set_identify_ground_material_status"`
- `a65@1.0.95` · wrapper m10115 (`setFloorIdentifyStatus`); call sites m14255 · anchor `"set_identify_ground_material_status"`
- `a62@1.0.69` · wrapper m10109 (`setFloorIdentifyStatus`); call sites m13820 · anchor `"set_identify_ground_material_status"`

</details>

<a id="get_identify_ground_material_status"></a>
### `get_identify_ground_material_status` — Floor-material recognition switch (read)

Reads the switch.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.status == 1` means on.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_identify_ground_material_status", "params": []}
```

**Related:** [`set_identify_ground_material_status`](rooms-and-areas.md#set_identify_ground_material_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getFloorIdentifyStatus`); call sites m14285 · anchor `"get_identify_ground_material_status"`
- `a65@1.0.95` · wrapper m10115 (`getFloorIdentifyStatus`); call sites m14255 · anchor `"get_identify_ground_material_status"`
- `a62@1.0.69` · wrapper m10109 (`getFloorIdentifyStatus`); call sites m13820 · anchor `"get_identify_ground_material_status"`

</details>

<a id="set_ignore_identify_area"></a>
### `set_ignore_identify_area` — Ignore recognised objects

Marks recognised obstacles as ignored.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: an array of at most 49 entries `[2, <a>, <b>, <c>]` taken from the ignored-obstacle triplets of the map objects (a65 m14231).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`get_photo`](maps.md#get_photo)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setIgnoreIdentifyArea`); call sites m14261 · anchor `"set_ignore_identify_area"`
- `a65@1.0.95` · wrapper m10115 (`setIgnoreIdentifyArea`); call sites m14231 · anchor `"set_ignore_identify_area"`
- `a11@1.0.34` · call sites m10748, m11888 · anchor `"set_ignore_identify_area"`

</details>

<a id="set_carpet_area"></a>
### `set_carpet_area` — Add carpet areas

Saves user-added carpet zones.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"map_index": <map id>, "type": <int>, "zone_data": <zones>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Behaviour in the app**

Needs new-feature bit `isMapCarpetAddSupport` (low word bit 30).

**Related:** [`set_ignore_carpet_zone`](rooms-and-areas.md#set_ignore_carpet_zone)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`saveCarpetAddedZone`); call sites m10112 · anchor `"set_carpet_area"`
- `a65@1.0.95` · wrapper m10115 (`saveCarpetAddedZone`); call sites m10112 · anchor `"set_carpet_area"`
- `a62@1.0.69` · wrapper m10109 (`saveCarpetAddedZone`); call sites m12038 · anchor `"set_carpet_area"`

</details>

<a id="set_ignore_carpet_zone"></a>
### `set_ignore_carpet_zone` — Carpet-ignore zones

Saves zones where carpet detection is ignored.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"map_index": <map id>, "zone_data": <zones>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`set_carpet_area`](rooms-and-areas.md#set_carpet_area), [`set_carpet_mode`](carpet.md#set_carpet_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`saveCarpetIgnoreZone`); call sites m10112 · anchor `"set_ignore_carpet_zone"`
- `a65@1.0.95` · wrapper m10115 (`saveCarpetIgnoreZone`); call sites m10112 · anchor `"set_ignore_carpet_zone"`
- `a08@1.0.47` · wrapper m10013 (`saveCarpetIgnoreZone`); call sites m10322 · anchor `"set_ignore_carpet_zone"`

</details>

<a id="app_set_door_sill_blocks"></a>
### `app_set_door_sill_blocks` — Door-sill blocks

Saves manual door-sill (threshold) blocks.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"map_index": <map id>, "zone_data": <blocks>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`app_set_smart_door_sill`](rooms-and-areas.md#app_set_smart_door_sill)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`saveDoorSillBlocks`); call sites m10112 · anchor `"app_set_door_sill_blocks"`
- `a65@1.0.95` · wrapper m10115 (`saveDoorSillBlocks`); call sites m10112 · anchor `"app_set_door_sill_blocks"`
- `a29@1.0.75` · wrapper m10112 (`saveDoorSillBlocks`); call sites m10109 · anchor `"app_set_door_sill_blocks"`

</details>

<a id="app_set_smart_door_sill"></a>
### `app_set_smart_door_sill` — Smart door sills

Saves the automatic door-sill areas.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"map_index": <map id>, "zones": <zones>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`app_set_door_sill_blocks`](rooms-and-areas.md#app_set_door_sill_blocks)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`saveSmartDoorSills`); call sites m10112 · anchor `"app_set_smart_door_sill"`
- `a65@1.0.95` · wrapper m10115 (`saveSmartDoorSills`); call sites m10112 · anchor `"app_set_smart_door_sill"`
- `a29@1.0.75` · wrapper m10112 (`saveSmartDoorSills`); call sites m10109 · anchor `"app_set_smart_door_sill"`

</details>

<a id="app_set_ignore_stuck_point"></a>
### `app_set_ignore_stuck_point` — Ignore stuck points

Saves points where the robot's stuck detection is ignored.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"map_index": <map id>, "point_data": <points>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`app_set_smart_cliff_forbidden`](rooms-and-areas.md#app_set_smart_cliff_forbidden)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setIgnoreStuckPoint`); call sites m10112 · anchor `"app_set_ignore_stuck_point"`
- `a65@1.0.95` · wrapper m10115 (`setIgnoreStuckPoint`); call sites m10112 · anchor `"app_set_ignore_stuck_point"`
- `a29@1.0.75` · wrapper m10112 (`setIgnoreStuckPoint`); call sites m10109 · anchor `"app_set_ignore_stuck_point"`

</details>

<a id="app_set_smart_cliff_forbidden"></a>
### `app_set_smart_cliff_forbidden` — Cliff-forbidden areas

Saves areas treated as cliff-forbidden.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"map_index": <map id>, "zones": <zones>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`app_set_ignore_stuck_point`](rooms-and-areas.md#app_set_ignore_stuck_point)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCliffForbidden`); call sites m10112 · anchor `"app_set_smart_cliff_forbidden"`
- `a65@1.0.95` · wrapper m10115 (`setCliffForbidden`); call sites m10112 · anchor `"app_set_smart_cliff_forbidden"`
- `a29@1.0.75` · wrapper m10112 (`setCliffForbidden`); call sites m10109 · anchor `"app_set_smart_cliff_forbidden"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
