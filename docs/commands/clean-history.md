# Cleaning history

[Home](../../README.md) / [Commands](index.md) / Cleaning history

Cleaning summary, per-run records and the map of a past run.

History is a two-level query: [`get_clean_summary`](#get_clean_summary) returns totals and the list of record ids, then
[`get_clean_record`](#get_clean_record) is called **once per id**. A record id is the **start time** of the run as a Unix
timestamp; the plugin ignores ids ≤ 1451577600 (1 Jan 2016) as invalid (✅ Bundle · a65 m14012). Two data layouts exist:
an array layout (older firmware) and an object layout (new-feature bits `isNewDataForCleanHistory` / `…Detail`,
low word bits 22 and 23). See also [clean record fields](../reference/clean-record.md).

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`get_clean_summary`](#get_clean_summary) | Returns the lifetime totals and the ids of the stored records. | ✅ Bundle |
| [`get_clean_record`](#get_clean_record) | Returns the details of the run that started at the given time. | ✅ Bundle |
| [`get_clean_record_map`](#get_clean_record_map) | Downloads the map and path of a record (same file mechanism as the live map). | ✅ Bundle |
| [`get_clean_record_map_v2`](#get_clean_record_map_v2) | Declared in every Methods table; never called. | ✅ Bundle (declared only) |
| [`del_clean_record`](#del_clean_record) | Deletes the record with the given start time. | ✅ Bundle |
| [`clear_clean_records`](#clear_clean_records) | Deletes the whole history; only the a01-family bundles (a01, c1, e2) call it. | ✅ Bundle |
| [`app_get_clean_estimate_info`](#app_get_clean_estimate_info) | Polled every 5 s by the "clean estimate" page. | ✅ Bundle |

<a id="get_clean_summary"></a>
### `get_clean_summary` — Totals and record ids

Returns the lifetime totals and the ids of the stored records.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

Array layout: `result` = `[total_time, total_area, total_count, [record id, …]]`.
Object layout: `result` = `{"clean_time", "clean_area", "clean_count", "records": [id, …], "dust_collection_count", "mop_count", "wash_count"}`
(the last three only on dock models).

**Example** — constructed from app code (element order; values invented)

```json
{"result": [174145, 2410215000, 82, [1488240000, 1488153600]], "id": 1}
```

**Legacy documentation**

⚪ Legacy [clean_summary+record.md](../../clean_summary+record.md) documents both layouts — confirmed (array and object with `clean_time`, `clean_area`,
`clean_count`, `dust_collection_count`, `records`). **Correction:** the legacy text gives the area in cm²; the app divides it by 1 000 000 to show
square metres, so the unit is mm² ([units](../reference/units.md)). A legacy capture of the object layout also shows a top-level `exe_time` next to `result`;
the plugin does not read it.

**Related:** [`get_clean_record`](clean-history.md#get_clean_record)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCleanSummary`); call sites m14042; table key `GetCleanSummary` · anchor `"GetCleanSummary"`
- `a65@1.0.95` · wrapper m10115 (`getCleanSummary`); call sites m14012; table key `GetCleanSummary` · anchor `"GetCleanSummary"`
- `t4@1.0.32` · wrapper m10010 (`getCleanSummary`); call sites m11300; table key `GetCleanSummary` · anchor `"GetCleanSummary"`

</details>

<a id="get_clean_record"></a>
### `get_clean_record` — One cleaning record

Returns the details of the run that started at the given time.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<record id>]` (the start timestamp).

**Response**

`result[0]`, array layout (9 elements): `[start, end, duration, area, error, complete, start_type, clean_type, finish_reason]`.
Object layout: `{"begin", "end", "duration", "area", "error", "complete", "start_type", "clean_type", "finish_reason",
"dust_collection_status", "avoid_count", "clean_mop", "wash_count", "wash_time", "map_flag"}`; `map_flag` is `-2` when absent.
Units and enumerations: [clean record fields](../reference/clean-record.md).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_clean_record", "params": [1700000000]}
```

**Related:** [`get_clean_summary`](clean-history.md#get_clean_summary), [`get_clean_record_map`](clean-history.md#get_clean_record_map), [`del_clean_record`](clean-history.md#del_clean_record)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCleanRecord`); call sites m14042; table key `GetCleanRecord` · anchor `"GetCleanRecord"`
- `a65@1.0.95` · wrapper m10115 (`getCleanRecord`); call sites m14012; table key `GetCleanRecord` · anchor `"GetCleanRecord"`
- `t4@1.0.32` · wrapper m10010 (`getCleanRecord`); call sites m11300; table key `GetCleanRecord` · anchor `"GetCleanRecord"`

</details>

<a id="get_clean_record_map"></a>
### `get_clean_record_map` — Map of a past run

Downloads the map and path of a record (same file mechanism as the live map).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`); map download (`getMapData` -> RPC returning a file name, then HTTPS download; see [maps](../concepts/maps-overview.md)) |

**Request**

Mi Home: `[<start>]`; Roborock app: `{"start_time": <start>}` (✅ Bundle · a65 m14042 `fetchRemoteMap`), through `getMapData`.

**Response**

`result[0]` is the **object name** of the map file (the plugin replaces `%2F` by `/`), or the string `retry` (ask again after 1 s, at most 8 times) or `locating` (the robot is relocating; the attempt ends without a callback). The app then asks the cloud for a download address of that object, downloads it, un-gzips it and validates it ([maps overview](../concepts/maps-overview.md#how-a-map-reaches-the-app)). ✅ Bundle · a65 m10109 `downloadMap`. The downloaded file is a map file with a `PATH` block of the cleaning run ([map file format](../../RRMapFile/RRFileFormat.md)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_clean_record_map", "params": [1700000000]}
```

**Legacy documentation**

⚪ Legacy [clean_summary+record.md](../../clean_summary+record.md).

**Related:** [`get_clean_record_map_v2`](clean-history.md#get_clean_record_map_v2), [`get_clean_record`](clean-history.md#get_clean_record)

<details><summary>Sources</summary>

- `a74@1.0.96` · call sites m14072; table key `GetCleanRecordMap` · anchor `"GetCleanRecordMap"`
- `a65@1.0.95` · call sites m14042; table key `GetCleanRecordMap` · anchor `"GetCleanRecordMap"`
- `t4@1.0.32` · call sites m11324; table key `GetCleanRecordMap` · anchor `"GetCleanRecordMap"`

</details>

<a id="get_clean_record_map_v2"></a>
### `get_clean_record_map_v2` — Record map v2 (declared only)

Declared in every Methods table; never called.

| | |
|---|---|
| Evidence | ✅ Bundle (declared only) — no call site found in the bundles |
| Other bundles | declared only: all 42 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

❓ Unknown — no call site.

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Related:** [`get_clean_record_map`](clean-history.md#get_clean_record_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · table key `GetCleanRecordMapV2` · anchor `"GetCleanRecordMapV2"`
- `a65@1.0.95` · table key `GetCleanRecordMapV2` · anchor `"GetCleanRecordMapV2"`
- `t4@1.0.32` · table key `GetCleanRecordMapV2` · anchor `"GetCleanRecordMapV2"`

</details>

<a id="del_clean_record"></a>
### `del_clean_record` — Delete one record

Deletes the record with the given start time.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<start>]` (the plugin passes `rowData.start`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "del_clean_record", "params": [1700000000]}
```

**Related:** [`get_clean_record`](clean-history.md#get_clean_record), [`clear_clean_records`](clean-history.md#clear_clean_records)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`deleteCleanRecord`); call sites m14042; table key `DelCleanRecord` · anchor `"DelCleanRecord"`
- `a65@1.0.95` · wrapper m10115 (`deleteCleanRecord`); call sites m14012; table key `DelCleanRecord` · anchor `"DelCleanRecord"`
- `t4@1.0.32` · wrapper m10010 (`deleteCleanRecord`); call sites m11300; table key `DelCleanRecord` · anchor `"DelCleanRecord"`

</details>

<a id="clear_clean_records"></a>
### `clear_clean_records` — Delete all records

Deletes the whole history; only the a01-family bundles (a01, c1, e2) call it.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 3: a01 c1 e2 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result.length` (3), `result[0]` (3). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "clear_clean_records", "params": []}
```

**Related:** [`del_clean_record`](clean-history.md#del_clean_record)

<details><summary>Sources</summary>

- `a01@1.0.51` · call sites m11369; table key `ClearCleanRecord` · anchor `"ClearCleanRecord"`
- `e2@1.0.48` · call sites m11366; table key `ClearCleanRecord` · anchor `"ClearCleanRecord"`
- `c1@1.0.48` · call sites m11366; table key `ClearCleanRecord` · anchor `"ClearCleanRecord"`

</details>

<a id="app_get_clean_estimate_info"></a>
### `app_get_clean_estimate_info` — Clean estimate (debug page)

Polled every 5 s by the "clean estimate" page.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result.clean_estimate` (21). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_get_clean_estimate_info", "params": {}}
```

**Related:** [`get_clean_summary`](clean-history.md#get_clean_summary)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCleanEstimateInfo`); call sites m14582 · anchor `"app_get_clean_estimate_info"`
- `a65@1.0.95` · wrapper m10115 (`getCleanEstimateInfo`); call sites m14528 · anchor `"app_get_clean_estimate_info"`
- `a34@1.0.70` · wrapper m10109 (`getCleanEstimateInfo`); call sites m14105 · anchor `"app_get_clean_estimate_info"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
