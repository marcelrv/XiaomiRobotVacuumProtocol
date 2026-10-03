# Maps and multi-floor maps

[Home](../../README.md) / [Commands](index.md) / Maps and multi-floor maps

Map download, map editing sessions, multi-floor map management and map backups.

**The map is not returned by the RPC.** In Mi Home the map methods (`get_map_v1`, `get_multi_map`, `get_recover_map`, …)
are sent through `getMapData` → `MiMapDownloader.downloadMap`. The robot answers with a *file name* (or `retry` /
`locating`); the plugin then asks the Mi smart-home service for a download URL of that object, downloads a gzip file,
un-gzips it and validates it. The resulting bytes are the map file described in
[map formats](../maps/index.md). Details: [maps overview](../concepts/maps-overview.md).

Maps use a plugin-side retry loop: up to 8 retries, 1 s after a `retry` reply and 2 s after a failure
(✅ Bundle · a65 m10109 `downloadMap`).

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`get_map`](#get_map) | Raw map request used by the newest plugin generation through an encrypted/compressed path. | ✅ Bundle |
| [`get_map_v1`](#get_map_v1) | The standard map request; the reply names the file to download. | ✅ Bundle |
| [`get_map_v2`](#get_map_v2) | Listed in every Methods table; never called. | ✅ Bundle (declared only) |
| [`app_get_map`](#app_get_map) | The `GetMap` entry of the `saphire`/`tanos` table; no call site. | ✅ Bundle (declared only) |
| [`get_fresh_map`](#get_fresh_map) | Declared in 41 bundles; never called (the s5 bundle calls the `_v1` variant). | ✅ Bundle (declared only) |
| [`get_fresh_map_v1`](#get_fresh_map_v1) | Map request for the "new map" candidate; only the s5 bundle contains the call. | ✅ Bundle |
| [`get_persist_map`](#get_persist_map) | Declared in 41 bundles; never called. | ✅ Bundle (declared only) |
| [`get_persist_map_v1`](#get_persist_map_v1) | Saved-map request; only the s5 bundle contains the call. | ✅ Bundle |
| [`get_photo`](#get_photo) | Fetches a photo taken by the robot (obstacle recognition). | ✅ Bundle |
| [`get_random_pkey`](#get_random_pkey) | Returns a public key used for encrypted record data. | ✅ Bundle |
| [`get_multi_map`](#get_multi_map) | Downloads one saved map of a multi-floor setup. | ✅ Bundle |
| [`get_multi_maps_list`](#get_multi_maps_list) | Returns the saved maps and the maximum number of floors. | ✅ Bundle |
| [`load_multi_map`](#load_multi_map) | Makes a saved map the active one. | ✅ Bundle |
| [`name_multi_map`](#name_multi_map) | Sets the name of a saved map. | ✅ Bundle |
| [`recover_multi_map`](#recover_multi_map) | Restores a saved floor map from its backup copy. | ✅ Bundle |
| [`save_map`](#save_map) | Writes map edits: virtual walls, forbidden zones and, with multi-floor, the target map. | ✅ Bundle |
| [`reset_map`](#reset_map) | Deletes the current map on the robot. | ✅ Bundle |
| [`start_edit_map`](#start_edit_map) | Tells the robot that the app edits the map. | ✅ Bundle |
| [`end_edit_map`](#end_edit_map) | Ends the session (also called when leaving without saving). | ✅ Bundle |
| [`use_new_map`](#use_new_map) | s5-generation "new map / old map" choice: keep the new map. | ✅ Bundle |
| [`use_old_map`](#use_old_map) | Counterpart of `use_new_map`. | ✅ Bundle |
| [`get_recover_map`](#get_recover_map) | Downloads the map of a backup entry for preview. | ✅ Bundle |
| [`get_recover_maps`](#get_recover_maps) | Returns the restorable map versions. | ✅ Bundle |
| [`recover_map`](#recover_map) | Restores the chosen backup entry. | ✅ Bundle |
| [`del_map`](#del_map) | Deletes a saved floor map. | ✅ Bundle |
| [`get_map_status`](#get_map_status) | Wrapped in every newer bundle; no call site. The map status is taken from the status field `map_status`. | ✅ Bundle (wrapper only) |
| [`set_switch_map_mode`](#set_switch_map_mode) | Turns automatic switching between saved maps on or off. | ✅ Bundle |
| [`manual_bak_map`](#manual_bak_map) | Creates a manual backup of a saved floor map. | ✅ Bundle |
| [`app_update_unsave_map`](#app_update_unsave_map) | Tells the robot what to do with a map it did not save. | ✅ Bundle |
| [`get_dynamic_map_diff`](#get_dynamic_map_diff) | Asks which map layers changed since a nonce. | ✅ Bundle |
| [`get_dynamic_data`](#get_dynamic_data) | Fetches the changed data of one map layer. | ✅ Bundle |
| [`get_offline_map_status`](#get_offline_map_status) | Wrapped; no call site (the app keeps the state locally). | ✅ Bundle (wrapper only) |
| [`set_offline_map_status`](#set_offline_map_status) | Enables or disables offline map storage. | ✅ Bundle |
| [`set_lab_status`](#set_lab_status) | Turns map saving (and multi-floor maps) on or off. | ✅ Bundle |
| [`set_map_beautification_status`](#set_map_beautification_status) | Writes a bit mask of experimental map-display options. | ✅ Bundle |
| [`get_map_beautification_status`](#get_map_beautification_status) | Reads the mask. | ✅ Bundle |

<a id="get_map"></a>
### `get_map` — Get the map (newer raw request)

Raw map request used by the newest plugin generation through an encrypted/compressed path.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Other bundles | declared only: 17: a08 a09 a10 a11 a14 a15 a19 a23 m1s p5 s4 s5 s5e s6 t4 t6 v1; alternate table only: 3: a01 c1 e2 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`); map download (`getMapData` -> RPC returning a file name, then HTTPS download; see [maps](../concepts/maps-overview.md)) |

**Request**

`params`: `{}`; called through `getAndDecBase64Data("get_map", {}, Lz4)` (a65 m10046).

**Response**

Through the encrypted path of generation-B plugins: the request carries a freshly generated public key and a cipher suite (`endpoint`, `security`); `result[0]` is again the object name (`retry` is handled as above). The downloaded file is read as base64, decrypted by the plugin (`Decryptor`) and LZ4-decompressed; the result is a map file ([maps overview](../concepts/maps-overview.md#the-newer-encrypted-path-get_map-get_photo)). ✅ Bundle · a65 m12806 `downloadFile`, m10046 `getAndDecBase64Data`.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_map", "params": {}}
```

**Behaviour in the app**

In the plugin the data is returned base64-encoded and decompressed with LZ4; the transport details of that path are not part of the miIO request (❓ Unknown beyond the method name).

**Related:** [`get_map_v1`](maps.md#get_map_v1), [`get_photo`](maps.md#get_photo), [`get_random_pkey`](maps.md#get_random_pkey)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getMapBase64Data`); call sites m10112; table key `GetMap` · anchor `"GetMap"`
- `a65@1.0.95` · wrapper m10115 (`getMapBase64Data`); call sites m10112; table key `GetMap` · anchor `"GetMap"`
- `a62@1.0.69` · wrapper m10109 (`getMapBase64Data`); call sites m12038; table key `GetMap` · anchor `"GetMap"`

</details>

<a id="get_map_v1"></a>
### `get_map_v1` — Get the current map

The standard map request; the reply names the file to download.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 39: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5 s5e s6 t4 t6 v1 model(s) |
| Other bundles | declared only: 3: a01 c1 e2 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`); map download (`getMapData` -> RPC returning a file name, then HTTPS download; see [maps](../concepts/maps-overview.md)) |

**Request**

`params` depends on the bundle: `{}` or `[]` (older); `{"nonce": <int>}` when the firmware supports incremental maps
(`isSupportIncrementalMap`, a65 m10112: `-1` for the first request).

**Response**

Classic: `result[0]` = object name (the plugin replaces `%2F` by `/`), or the strings `retry` / `locating`
(`locating` ends the attempt). Incremental maps: `result` is an object `{"result": "ok"|"retry", "nonce", "file", "snapshot"}`;
`retry` carries a `snapshot` that the plugin parses and a new `nonce` to ask with.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_map_v1", "params": {}}
```

**Legacy documentation**

⚪ Legacy [map_v1.md](../../map_v1.md) and [map.md](../../map.md): same file-name reply; the incremental form is new.

**Related:** [`get_map`](maps.md#get_map), [`get_multi_map`](maps.md#get_multi_map), [`get_dynamic_map_diff`](maps.md#get_dynamic_map_diff)

<details><summary>Sources</summary>

- `a74@1.0.96` · call sites m10112; table key `GetMapAndroid` · anchor `"GetMapAndroid"`
- `a65@1.0.95` · call sites m10112; table key `GetMapAndroid` · anchor `"GetMapAndroid"`
- `t4@1.0.32` · call sites m10553; table key `GetMapAndroid` · anchor `"GetMapAndroid"`

</details>

<a id="get_map_v2"></a>
### `get_map_v2` — Map v2 (declared only)

Listed in every Methods table; never called.

| | |
|---|---|
| Evidence | ✅ Bundle (declared only) — no call site found in the bundles |
| Other bundles | declared only: all 42 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

❓ Unknown — no call site.

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Related:** [`get_map_v1`](maps.md#get_map_v1)

<details><summary>Sources</summary>

- `a74@1.0.96` · table key `GetMapV2` · anchor `"GetMapV2"`
- `a65@1.0.95` · table key `GetMapV2` · anchor `"GetMapV2"`
- `t4@1.0.32` · table key `GetMapV2` · anchor `"GetMapV2"`

</details>

<a id="app_get_map"></a>
### `app_get_map` — Map (alternate-table name)

The `GetMap` entry of the `saphire`/`tanos` table; no call site.

| | |
|---|---|
| Evidence | ✅ Bundle (declared only) — no call site found in the bundles |
| Other bundles | declared only: 3: a01 c1 e2 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

❓ Unknown.

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Related:** [`get_map`](maps.md#get_map)

<details><summary>Sources</summary>

- `a01@1.0.51` · table key `GetMap` · anchor `"GetMap"`
- `e2@1.0.48` · table key `GetMap` · anchor `"GetMap"`
- `c1@1.0.48` · table key `GetMap` · anchor `"GetMap"`

</details>

<a id="get_fresh_map"></a>
### `get_fresh_map` — Fresh map (declared only)

Declared in 41 bundles; never called (the s5 bundle calls the `_v1` variant).

| | |
|---|---|
| Evidence | ✅ Bundle (declared only) — no call site found in the bundles |
| Other bundles | declared only: 41: a01 a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 c1 e2 m1s p5 s4 s5 s5e s6 t4 t6 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

❓ Unknown.

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Related:** [`get_fresh_map_v1`](maps.md#get_fresh_map_v1)

<details><summary>Sources</summary>

- `a74@1.0.96` · table key `GetFreshMap` · anchor `"GetFreshMap"`
- `a65@1.0.95` · table key `GetFreshMap` · anchor `"GetFreshMap"`
- `t4@1.0.32` · table key `GetFreshMap` · anchor `"GetFreshMap"`

</details>

<a id="get_fresh_map_v1"></a>
### `get_fresh_map_v1` — Fresh map (s5)

Map request for the "new map" candidate; only the s5 bundle contains the call.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 2: s5 v1 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`); map download (`getMapData` -> RPC returning a file name, then HTTPS download; see [maps](../concepts/maps-overview.md)) |

**Request**

`params`: `{}` via `getMapData`.

**Response**

`result[0]` is the **object name** of the map file (the plugin replaces `%2F` by `/`), or the string `retry` (ask again after 1 s, at most 8 times) or `locating` (the robot is relocating; the attempt ends without a callback). The app then asks the cloud for a download address of that object, downloads it, un-gzips it and validates it ([maps overview](../concepts/maps-overview.md#how-a-map-reaches-the-app)). ✅ Bundle · a65 m10109 `downloadMap`.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_fresh_map_v1", "params": {}}
```

**Related:** [`use_new_map`](maps.md#use_new_map), [`get_persist_map_v1`](maps.md#get_persist_map_v1)

<details><summary>Sources</summary>

- `s5@1.0.47` · call sites m10331 · anchor `"get_fresh_map_v1"`
- `v1@1.0.46` · call sites m10340; table key `GetFreshMap` · anchor `"GetFreshMap"`

</details>

<a id="get_persist_map"></a>
### `get_persist_map` — Persisted map (declared only)

Declared in 41 bundles; never called.

| | |
|---|---|
| Evidence | ✅ Bundle (declared only) — no call site found in the bundles |
| Other bundles | declared only: 41: a01 a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 c1 e2 m1s p5 s4 s5 s5e s6 t4 t6 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

❓ Unknown.

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Related:** [`get_persist_map_v1`](maps.md#get_persist_map_v1)

<details><summary>Sources</summary>

- `a74@1.0.96` · table key `GetPersistMap` · anchor `"GetPersistMap"`
- `a65@1.0.95` · table key `GetPersistMap` · anchor `"GetPersistMap"`
- `t4@1.0.32` · table key `GetPersistMap` · anchor `"GetPersistMap"`

</details>

<a id="get_persist_map_v1"></a>
### `get_persist_map_v1` — Persisted map (s5)

Saved-map request; only the s5 bundle contains the call.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 2: s5 v1 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`); map download (`getMapData` -> RPC returning a file name, then HTTPS download; see [maps](../concepts/maps-overview.md)) |

**Request**

`params`: `{}` via `getMapData`.

**Response**

`result[0]` is the **object name** of the map file (the plugin replaces `%2F` by `/`), or the string `retry` (ask again after 1 s, at most 8 times) or `locating` (the robot is relocating; the attempt ends without a callback). The app then asks the cloud for a download address of that object, downloads it, un-gzips it and validates it ([maps overview](../concepts/maps-overview.md#how-a-map-reaches-the-app)). ✅ Bundle · a65 m10109 `downloadMap`.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_persist_map_v1", "params": {}}
```

**Related:** [`use_old_map`](maps.md#use_old_map), [`get_fresh_map_v1`](maps.md#get_fresh_map_v1)

<details><summary>Sources</summary>

- `s5@1.0.47` · call sites m10331 · anchor `"get_persist_map_v1"`
- `v1@1.0.46` · call sites m10340; table key `GetPersistMap` · anchor `"GetPersistMap"`

</details>

<a id="get_photo"></a>
### `get_photo` — Get an obstacle photo

Fetches a photo taken by the robot (obstacle recognition).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`); map download (`getMapData` -> RPC returning a file name, then HTTPS download; see [maps](../concepts/maps-overview.md)) |
| Call-site gate | the call sits behind `isFwFilterObstacleSupported` (tests found in the enclosing code of the call sites; [feature flags](../concepts/feature-flags.md)) |

**Request**

`params`: `{"data_filter": {"img_id": <id>, "type": <int>}}`, through `getAndDecBase64Data("get_photo", …, gzip)` (a65 m10046).

**Response**

Same flow as `get_map`: `result[0]` is the object name, the file is downloaded and decrypted, then gunzipped and parsed by `Decryptor.parsePhotoData` (a65 m12806, m10046 `getPhotoBase64Data`). The request names the photo with `data_filter` (`img_id`, `type`).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_photo", "params": {"data_filter": {"img_id": 1, "type": 1}}}
```

**Behaviour in the app**

Needs the camera/obstacle features; see [camera](camera.md).

**Related:** [`get_random_pkey`](maps.md#get_random_pkey), [`upload_photo`](camera.md#upload_photo)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getPhotoBase64Data`); call sites m12611, m14261, m14330, m14339 · anchor `"get_photo"`
- `a65@1.0.95` · wrapper m10115 (`getPhotoBase64Data`); call sites m12599, m14231, m14300, m14309 · anchor `"get_photo"`
- `a11@1.0.34` · wrapper m10010 (`getPhotoBase64Data`); call sites m10553, m11888 · anchor `"get_photo"`

</details>

<a id="get_random_pkey"></a>
### `get_random_pkey` — Random public key

Returns a public key used for encrypted record data.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.pub_key` (string) is read (a65 m14657 and m14660); the value is then used by the record viewer. The key is not recorded here.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_random_pkey", "params": []}
```

**Related:** [`get_photo`](maps.md#get_photo)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getRandomPubKey`); call sites m14711, m14714 · anchor `"get_random_pkey"`
- `a65@1.0.95` · wrapper m10115 (`getRandomPubKey`); call sites m14657, m14660 · anchor `"get_random_pkey"`
- `a08@1.0.47` · wrapper m10013 (`getRandomPubKey`); call sites m12671, m12674 · anchor `"get_random_pkey"`

</details>

<a id="get_multi_map"></a>
### `get_multi_map` — Get a saved floor map

Downloads one saved map of a multi-floor setup.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 38: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5 s5e s6 t4 t6 model(s) |
| Other bundles | alternate table only: 3: a01 c1 e2 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`); map download (`getMapData` -> RPC returning a file name, then HTTPS download; see [maps](../concepts/maps-overview.md)) |

**Request**

Mi Home: `[<map id>]`, or `[<map id>, 1]` for the backup copy when `isSupportBackupMap` (new-feature high bit 17).
Roborock app (not Mi Home): `{"map_index": <id>, "is_bak": 1}` (✅ Bundle · a65 m12527 `getMapData`).

**Response**

`result[0]` is the **object name** of the map file (the plugin replaces `%2F` by `/`), or the string `retry` (ask again after 1 s, at most 8 times) or `locating` (the robot is relocating; the attempt ends without a callback). The app then asks the cloud for a download address of that object, downloads it, un-gzips it and validates it ([maps overview](../concepts/maps-overview.md#how-a-map-reaches-the-app)). ✅ Bundle · a65 m10109 `downloadMap`. For this call the downloaded file is stored as `map<NN>.gz` (`NN` = last two characters of the object name).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_multi_map", "params": [0]}
```

**Related:** [`get_multi_maps_list`](maps.md#get_multi_maps_list), [`load_multi_map`](maps.md#load_multi_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · call sites m12539; table key `GetMultiMap` · anchor `"GetMultiMap"`
- `a65@1.0.95` · call sites m12527; table key `GetMultiMap` · anchor `"GetMultiMap"`
- `t4@1.0.32` · call sites m11504; table key `GetMultiMap` · anchor `"GetMultiMap"`

</details>

<a id="get_multi_maps_list"></a>
### `get_multi_maps_list` — List saved floor maps

Returns the saved maps and the maximum number of floors.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 38: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5 s5e s6 t4 t6 model(s) |
| Other bundles | alternate table only: 3: a01 c1 e2 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` = `{"max_multi_map": <int>, "map_info": [ {"mapFlag", "add_time", "name", "length"}, … ]}` (✅ Bundle · a65 m12527).
The list UI uses `mapFlag` as the map id, `add_time` as the creation time, `name` (an empty name is replaced by the app's default
floor name plus `mapFlag + 1`) and `length`; the current map is sorted first, the others newest first.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_multi_maps_list", "params": []}
```

**Legacy documentation**

⚪ Legacy [multimap.md](../../multimap.md) documents the same keys and adds `max_bak_map` (maximum backup maps), `multi_map_count`
(number of stored maps) and a per-map `bak_maps` array (backup maps); the plugin reads none of these three. A legacy capture shows
`{"max_multi_map": 4, "max_bak_map": 0, "multi_map_count": 3, "map_info": [{"mapFlag": 0, "add_time": …, "length": 11, "name": …, "bak_maps": []}, …]}`
(legacy capture, unverified); the meaning of `length` is not given.

**Related:** [`load_multi_map`](maps.md#load_multi_map), [`name_multi_map`](maps.md#name_multi_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getMultiMaps, getMultiMapsList`); call sites m10112, m12539; table key `GetMultiMapsList` · anchor `"GetMultiMapsList"`
- `a65@1.0.95` · wrapper m10115 (`getMultiMaps, getMultiMapsList`); call sites m10112, m12527; table key `GetMultiMapsList` · anchor `"GetMultiMapsList"`
- `t4@1.0.32` · wrapper m10010 (`getMultiMaps`); call sites m10553, m11504; table key `GetMultiMapsList` · anchor `"GetMultiMapsList"`

</details>

<a id="load_multi_map"></a>
### `load_multi_map` — Switch to a saved floor map

Makes a saved map the active one.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 38: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5 s5e s6 t4 t6 model(s) |
| Other bundles | alternate table only: 3: a01 c1 e2 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<map id>]`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "load_multi_map", "params": [0]}
```

**Behaviour in the app**

In the retry-capable list ([transports](../concepts/transports.md#retry-protocol)). The app does not call it while the robot is cleaning on another map.

**Related:** [`get_multi_maps_list`](maps.md#get_multi_maps_list), [`recover_multi_map`](maps.md#recover_multi_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`loadMultiMap`); call sites m12539, m14003, m14021, m14027; table key `LoadMultiMap` · anchor `"LoadMultiMap"`
- `a65@1.0.95` · wrapper m10115 (`loadMultiMap`); call sites m12527, m13988, m13991, m13997; table key `LoadMultiMap` · anchor `"LoadMultiMap"`
- `t4@1.0.32` · call sites m11504; table key `LoadMultiMap` · anchor `"LoadMultiMap"`

</details>

<a id="name_multi_map"></a>
### `name_multi_map` — Rename a saved floor map

Sets the name of a saved map.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 38: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5 s5e s6 t4 t6 model(s) |
| Other bundles | alternate table only: 3: a01 c1 e2 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[{"multi_map": <map id>, "name": "<name>", "length": <int>}]` (`length` = byte/char length passed by the editor).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "name_multi_map", "params": [{"multi_map": 0, "name": "name", "length": 4}]}
```

**Related:** [`get_multi_maps_list`](maps.md#get_multi_maps_list)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`nameMultiMap`); call sites m12539; table key `NameMultiMap` · anchor `"NameMultiMap"`
- `a65@1.0.95` · wrapper m10115 (`nameMultiMap`); call sites m12527; table key `NameMultiMap` · anchor `"NameMultiMap"`
- `t4@1.0.32` · call sites m11504; table key `NameMultiMap` · anchor `"NameMultiMap"`

</details>

<a id="recover_multi_map"></a>
### `recover_multi_map` — Restore a saved map from backup

Restores a saved floor map from its backup copy.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Other bundles | declared only: 16: a08 a09 a10 a11 a14 a15 a19 a23 m1s p5 s4 s5 s5e s6 t4 t6; alternate table only: 3: a01 c1 e2 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"map_flag": <map id>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "recover_multi_map", "params": {"map_flag": 0}}
```

**Related:** [`manual_bak_map`](maps.md#manual_bak_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`recoverMultiMap`); call sites m12539; table key `RecoverMultiMap` · anchor `"RecoverMultiMap"`
- `a65@1.0.95` · wrapper m10115 (`recoverMultiMap`); call sites m12527; table key `RecoverMultiMap` · anchor `"RecoverMultiMap"`
- `a62@1.0.69` · wrapper m10109 (`recoverMultiMap`); call sites m13418; table key `RecoverMultiMap` · anchor `"RecoverMultiMap"`

</details>

<a id="save_map"></a>
### `save_map` — Save the edited map (walls, no-go zones, floor id)

Writes map edits: virtual walls, forbidden zones and, with multi-floor, the target map.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params` is an **array of arrays** built by the map editor: the wall entries and forbidden-zone entries concatenated
(`wallsPara.concat(fbzsPara)`); with multi-floor support (fw feature 120) two marker entries are appended:
`[100, <replace map id>]` and, when saving the home map, `[200, 0]` (✅ Bundle · a65 m10112 `saveMap`). The element
layout of wall/zone entries is described in [maps overview](../concepts/maps-overview.md#virtual-walls-and-forbidden-zones).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Behaviour in the app**

In the retry-capable list. The editing session is bracketed by [`start_edit_map`](#start_edit_map) and [`end_edit_map`](#end_edit_map).

**Legacy documentation**

⚪ Legacy [map.md](../../map.md) documents the same row layouts: a zone `[0, x1, y1, x2, y2, x3, y3, x4, y4]` (type 0 plus eight integers for the
rectangle) and a barrier (virtual wall) `[1, x1, y1, x2, y2]` — confirmed. The legacy page states that the call requires an activated
[lab status](#set_lab_status) (map saving); the plugin enables saving before it edits maps. README lists `save_map` as "s5, s6, s5e".

**Related:** [`start_edit_map`](maps.md#start_edit_map), [`end_edit_map`](maps.md#end_edit_map), [`set_lab_status`](maps.md#set_lab_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`saveMap`); call sites m10112; table key `SaveMap` · anchor `"SaveMap"`
- `a65@1.0.95` · wrapper m10115 (`saveMap`); call sites m10112; table key `SaveMap` · anchor `"SaveMap"`
- `t4@1.0.32` · wrapper m10010 (`saveMap`); call sites m10553; table key `SaveMap` · anchor `"SaveMap"`

</details>

<a id="reset_map"></a>
### `reset_map` — Reset (clear) the map

Deletes the current map on the robot.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result.length` (10), `result[0]` (10). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "reset_map", "params": []}
```

**Related:** [`recover_map`](maps.md#recover_map), [`del_map`](maps.md#del_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`resetMap`); call sites m12539; table key `ResetMap` · anchor `"ResetMap"`
- `a65@1.0.95` · wrapper m10115 (`resetMap`); call sites m12527; table key `ResetMap` · anchor `"ResetMap"`
- `t4@1.0.32` · call sites m10649, m10982; table key `ResetMap` · anchor `"ResetMap"`

</details>

<a id="start_edit_map"></a>
### `start_edit_map` — Begin a map edit session

Tells the robot that the app edits the map.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |
| Call-site gate | the call sits behind `isFBZReachMaxNum`, `isMoppingFBZReachMaxNum`, `isWallReachMaxNum` (tests found in the enclosing code of the call sites; [feature flags](../concepts/feature-flags.md)) |

**Request**

`params`: none (`[]`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "start_edit_map", "params": []}
```

**Related:** [`end_edit_map`](maps.md#end_edit_map), [`save_map`](maps.md#save_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`startEditMap`); call sites m12545, m14348, m14354, m14375; table key `StartEditMap` · anchor `"StartEditMap"`
- `a65@1.0.95` · wrapper m10115 (`startEditMap`); call sites m12533, m14318, m14324, m14345; table key `StartEditMap` · anchor `"StartEditMap"`
- `t4@1.0.32` · call sites m10649, m10886; table key `StartEditMap` · anchor `"StartEditMap"`

</details>

<a id="end_edit_map"></a>
### `end_edit_map` — End a map edit session

Ends the session (also called when leaving without saving).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "end_edit_map", "params": []}
```

**Related:** [`start_edit_map`](maps.md#start_edit_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`endEditMap`); call sites m12545; table key `EndEditMap` · anchor `"EndEditMap"`
- `a65@1.0.95` · wrapper m10115 (`endEditMap`); call sites m12533; table key `EndEditMap` · anchor `"EndEditMap"`
- `t4@1.0.32` · call sites m10886; table key `EndEditMap` · anchor `"EndEditMap"`

</details>

<a id="use_new_map"></a>
### `use_new_map` — Accept the freshly built map

s5-generation "new map / old map" choice: keep the new map.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 2: s5 v1 model(s) |
| Other bundles | declared only: 40: a01 a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 c1 e2 m1s p5 s4 s5e s6 t4 t6 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`); only the s5 bundle contains call sites.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "use_new_map", "params": []}
```

**Related:** [`use_old_map`](maps.md#use_old_map)

<details><summary>Sources</summary>

- `s5@1.0.47` · wrapper m10010,11444 (`useNewMap`); call sites m11477; table key `UseNewMap` · anchor `"UseNewMap"`
- `v1@1.0.46` · wrapper m10010 (`useNewMap`); call sites m11396; table key `UseNewMap` · anchor `"UseNewMap"`

</details>

<a id="use_old_map"></a>
### `use_old_map` — Keep the previous map

Counterpart of `use_new_map`.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 2: s5 v1 model(s) |
| Other bundles | declared only: 40: a01 a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 c1 e2 m1s p5 s4 s5e s6 t4 t6 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`); only the s5 bundle contains call sites.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "use_old_map", "params": []}
```

**Related:** [`use_new_map`](maps.md#use_new_map)

<details><summary>Sources</summary>

- `s5@1.0.47` · wrapper m10010,11444 (`useOldMap`); call sites m11477; table key `UseOldMap` · anchor `"UseOldMap"`
- `v1@1.0.46` · wrapper m10010 (`useOldMap`); call sites m11396; table key `UseOldMap` · anchor `"UseOldMap"`

</details>

<a id="get_recover_map"></a>
### `get_recover_map` — Download a restorable map

Downloads the map of a backup entry for preview.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`); map download (`getMapData` -> RPC returning a file name, then HTTPS download; see [maps](../concepts/maps-overview.md)) |

**Request**

`params`: `{"map_index": <id>}`, plus `"is_bak": 0|1` when `isSupportBackupMap`; some bundles pass `[<id>]`.

**Response**

`result[0]` is the **object name** of the map file (the plugin replaces `%2F` by `/`), or the string `retry` (ask again after 1 s, at most 8 times) or `locating` (the robot is relocating; the attempt ends without a callback). The app then asks the cloud for a download address of that object, downloads it, un-gzips it and validates it ([maps overview](../concepts/maps-overview.md#how-a-map-reaches-the-app)). ✅ Bundle · a65 m10109 `downloadMap`. The string `unknown_method` makes the plugin report "plugin needs update" (a65 m12527).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_recover_map", "params": {"map_index": 0}}
```

**Related:** [`get_recover_maps`](maps.md#get_recover_maps), [`recover_map`](maps.md#recover_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getRecoverMap`); call sites m12539; table key `GetRecoverMap` · anchor `"GetRecoverMap"`
- `a65@1.0.95` · wrapper m10115 (`getRecoverMap`); call sites m12527; table key `GetRecoverMap` · anchor `"GetRecoverMap"`
- `t4@1.0.32` · call sites m10982, m11504; table key `GetRecoverMap` · anchor `"GetRecoverMap"`

</details>

<a id="get_recover_maps"></a>
### `get_recover_maps` — List map backups

Returns the restorable map versions.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result` is an array of `[<map id>, <time>]` pairs (a65 m12527).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_recover_maps", "params": []}
```

**Related:** [`get_recover_map`](maps.md#get_recover_map), [`recover_map`](maps.md#recover_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getRecoverMaps`); call sites m12539; table key `GetRecoverMaps` · anchor `"GetRecoverMaps"`
- `a65@1.0.95` · wrapper m10115 (`getRecoverMaps`); call sites m12527; table key `GetRecoverMaps` · anchor `"GetRecoverMaps"`
- `t4@1.0.32` · call sites m10982; table key `GetRecoverMaps` · anchor `"GetRecoverMaps"`

</details>

<a id="recover_map"></a>
### `recover_map` — Restore a map version

Restores the chosen backup entry.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<map id>]`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "recover_map", "params": [0]}
```

**Related:** [`get_recover_maps`](maps.md#get_recover_maps)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`recoverMap`); call sites m12539; table key `RecoverMap` · anchor `"RecoverMap"`
- `a65@1.0.95` · wrapper m10115 (`recoverMap`); call sites m12527; table key `RecoverMap` · anchor `"RecoverMap"`
- `t4@1.0.32` · call sites m10982; table key `RecoverMap` · anchor `"RecoverMap"`

</details>

<a id="del_map"></a>
### `del_map` — Delete a saved map

Deletes a saved floor map.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<map id>]`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "del_map", "params": [0]}
```

**Behaviour in the app**

If it is the current map the app also clears its cached map data and removes stored AR-map data for that id.

**Related:** [`get_multi_maps_list`](maps.md#get_multi_maps_list)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`deleteSelectMap`); call sites m12539; table key `DeleteSelectMap` · anchor `"DeleteSelectMap"`
- `a65@1.0.95` · wrapper m10115 (`deleteSelectMap`); call sites m12527; table key `DeleteSelectMap` · anchor `"DeleteSelectMap"`
- `t4@1.0.32` · call sites m10982, m11504; table key `DeleteSelectMap` · anchor `"DeleteSelectMap"`

</details>

<a id="get_map_status"></a>
### `get_map_status` — Map status (wrapped, unused)

Wrapped in every newer bundle; no call site. The map status is taken from the status field `map_status`.

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
{"id": 1, "method": "get_map_status", "params": []}
```

**Related:** [`get_prop`](status.md#get_prop)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getMapStatus`); table key `GetMapStatus` · anchor `"GetMapStatus"`
- `a65@1.0.95` · wrapper m10115 (`getMapStatus`); table key `GetMapStatus` · anchor `"GetMapStatus"`
- `t4@1.0.32` · wrapper m10010 (`getMapStatus`); table key `GetMapStatus` · anchor `"GetMapStatus"`

</details>

<a id="set_switch_map_mode"></a>
### `set_switch_map_mode` — Smart map switching

Turns automatic switching between saved maps on or off.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"mode": 0|1}` (the app sends `0` when the switch was on, `1` otherwise; a27 m14258). The current value is the status field `switch_map_mode`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_switch_map_mode", "params": {"mode": 1}}
```

**Behaviour in the app**

Offered with new-feature bit `isSupportSetSwitchMapMode` (low word bit 28).

**Related:** [`set_lab_status`](maps.md#set_lab_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setSwitchMapMode`); call sites m14288; table key `SetSwitchMapMode` · anchor `"SetSwitchMapMode"`
- `a65@1.0.95` · wrapper m10115 (`setSwitchMapMode`); call sites m14258; table key `SetSwitchMapMode` · anchor `"SetSwitchMapMode"`
- `a62@1.0.69` · wrapper m10109 (`setSwitchMapMode`); call sites m13823; table key `SetSwitchMapMode` · anchor `"SetSwitchMapMode"`

</details>

<a id="manual_bak_map"></a>
### `manual_bak_map` — Back up a saved map

Creates a manual backup of a saved floor map.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"map_flag": <map id>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "manual_bak_map", "params": {"map_flag": 0}}
```

**Related:** [`recover_multi_map`](maps.md#recover_multi_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`manualBackupMap`); call sites m12539 · anchor `"manual_bak_map"`
- `a65@1.0.95` · wrapper m10115 (`manualBackupMap`); call sites m12527 · anchor `"manual_bak_map"`
- `a62@1.0.69` · wrapper m10109 (`manualBackupMap`); call sites m13418 · anchor `"manual_bak_map"`

</details>

<a id="app_update_unsave_map"></a>
### `app_update_unsave_map` — Handle an unsaved map

Tells the robot what to do with a map it did not save.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"update": <code>}` with the codes of `UnsaveMapHandle`: Ignore 0, Update 1, Load 2, Done 3 ([enums](../reference/other-enums.md)).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_update_unsave_map", "params": {"update": 1}}
```

**Behaviour in the app**

The reason is the status field `unsave_map_reason` (`UnsaveMapReason`: Saved 0 … MapMess 8).

**Related:** [`set_lab_status`](maps.md#set_lab_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`updateUnsaveMap`); call sites m13031 · anchor `"app_update_unsave_map"`
- `a65@1.0.95` · wrapper m10115 (`updateUnsaveMap`); call sites m13019 · anchor `"app_update_unsave_map"`
- `a62@1.0.69` · wrapper m10109 (`updateUnsaveMap`); call sites m12587 · anchor `"app_update_unsave_map"`

</details>

<a id="get_dynamic_map_diff"></a>
### `get_dynamic_map_diff` — Incremental map diff

Asks which map layers changed since a nonce.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"nonce": <mapNonce>, "round": <ms timestamp>}`.

**Response**

`result` lists per-layer diffs; the plugin decides per layer whether to fetch data, reset or reload the map.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_dynamic_map_diff", "params": {"nonce": -1, "round": 1700000000000}}
```

**Related:** [`get_dynamic_data`](maps.md#get_dynamic_data), [`get_map_v1`](maps.md#get_map_v1)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getMapDiffDynamic`); call sites m10112 · anchor `"get_dynamic_map_diff"`
- `a65@1.0.95` · wrapper m10115 (`getMapDiffDynamic`); call sites m10112 · anchor `"get_dynamic_map_diff"`
- `a29@1.0.75` · wrapper m10112 (`getMapDiffDynamic`); call sites m10109 · anchor `"get_dynamic_map_diff"`

</details>

<a id="get_dynamic_data"></a>
### `get_dynamic_data` — Incremental map layer data

Fetches the changed data of one map layer.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: an object `params` built from the layer description (`dataInst.toJSONString`).

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result.nonce` (16). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Related:** [`get_dynamic_map_diff`](maps.md#get_dynamic_map_diff)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getMapDataDynamic`); call sites m10112 · anchor `"get_dynamic_data"`
- `a65@1.0.95` · wrapper m10115 (`getMapDataDynamic`); call sites m10112 · anchor `"get_dynamic_data"`
- `a29@1.0.75` · wrapper m10112 (`getMapDataDynamic`); call sites m10109 · anchor `"get_dynamic_data"`

</details>

<a id="get_offline_map_status"></a>
### `get_offline_map_status` — Offline map switch (read)

Wrapped; no call site (the app keeps the state locally).

| | |
|---|---|
| Evidence | ✅ Bundle (wrapper only) — no call site found in the bundles |
| Other bundles | wrapper only: 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_offline_map_status", "params": {}}
```

**Related:** [`set_offline_map_status`](maps.md#set_offline_map_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getOfflineMapStatus`) · anchor `"get_offline_map_status"`
- `a65@1.0.95` · wrapper m10115 (`getOfflineMapStatus`) · anchor `"get_offline_map_status"`
- `a29@1.0.75` · wrapper m10112 (`getOfflineMapStatus`) · anchor `"get_offline_map_status"`

</details>

<a id="set_offline_map_status"></a>
### `set_offline_map_status` — Offline map switch

Enables or disables offline map storage.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"status": 0|1}`; the status field `switch_status` bit 0 reports it.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_offline_map_status", "params": {"status": 1}}
```

**Related:** [`get_offline_map_status`](maps.md#get_offline_map_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setOfflineMapStatus`); call sites m13031, m14168 · anchor `"set_offline_map_status"`
- `a65@1.0.95` · wrapper m10115 (`setOfflineMapStatus`); call sites m13019, m14138 · anchor `"set_offline_map_status"`
- `a29@1.0.75` · wrapper m10112 (`setOfflineMapStatus`); call sites m12773, m13886 · anchor `"set_offline_map_status"`

</details>

<a id="set_lab_status"></a>
### `set_lab_status` — Map saving / multi-floor switch

Turns map saving (and multi-floor maps) on or off.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[0|1]` on firmware without multi-floor; with multi-floor `{"lab_status": 0|1|3}`; `{"lab_status": 1, "reserve_map": <id>}`
keeps a map when switching (✅ Bundle · a08, a65 m12527 `mapSaveSwitch`). Reported back as the status field
`lab_status` (1 = map saving, 3 = multi-floor).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_lab_status", "params": [1]}
```

**Legacy documentation**

⚪ Legacy [lab_status.md](../../lab_status.md); README lists it as "s5, s6, s5e".

**Related:** [`load_multi_map`](maps.md#load_multi_map), [`app_update_unsave_map`](maps.md#app_update_unsave_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setLabStatus`); call sites m12539, m14168, m14288, m14348; table key `SetLabStatus` · anchor `"SetLabStatus"`
- `a65@1.0.95` · wrapper m10115 (`setLabStatus`); call sites m12527, m14138, m14258, m14318; table key `SetLabStatus` · anchor `"SetLabStatus"`
- `t4@1.0.32` · wrapper m10010 (`setLabStatus`); call sites m11453; table key `SetLabStatus` · anchor `"SetLabStatus"`

</details>

<a id="set_map_beautification_status"></a>
### `set_map_beautification_status` — Map beautification bits (debug)

Writes a bit mask of experimental map-display options.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"status": <bit mask>}`; bits: 1 partition map, 2 carpet, 4 mop floor, plus further debug switches (a65 m14375). Debug page only.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_map_beautification_status", "params": {"status": 1}}
```

**Related:** [`get_map_beautification_status`](maps.md#get_map_beautification_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setMapBeautificationStatus`); call sites m14405 · anchor `"set_map_beautification_status"`
- `a65@1.0.95` · wrapper m10115 (`setMapBeautificationStatus`); call sites m14375 · anchor `"set_map_beautification_status"`
- `a14@1.0.53` · wrapper m10142 (`setMapBeautificationStatus`); call sites m13286 · anchor `"set_map_beautification_status"`

</details>

<a id="get_map_beautification_status"></a>
### `get_map_beautification_status` — Map beautification bits (read)

Reads the mask.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.status` (integer bit mask).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_map_beautification_status", "params": []}
```

**Related:** [`set_map_beautification_status`](maps.md#set_map_beautification_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getMapBeautificationStatus`); call sites m14405 · anchor `"get_map_beautification_status"`
- `a65@1.0.95` · wrapper m10115 (`getMapBeautificationStatus`); call sites m14375 · anchor `"get_map_beautification_status"`
- `a14@1.0.53` · wrapper m10142 (`getMapBeautificationStatus`); call sites m13286 · anchor `"get_map_beautification_status"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
