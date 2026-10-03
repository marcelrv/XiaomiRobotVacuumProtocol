# Status, properties and capabilities

[Home](../../README.md) / [Commands](index.md) / Status, properties and capabilities

Reading the robot state, the capability lists reported by the firmware and basic identity information.

The plugin polls **one** call for the robot state: [`get_prop`](#get_prop) with the parameter `"get_status"`. Capabilities
come from [`app_get_init_status`](#app_get_init_status) (and, in the bundles of a01, c1, e2, s5 and v1, from
[`get_fw_features`](#get_fw_features)). The status fields are described in
[status fields](../reference/status-fields.md); state and error codes in [states](../reference/states.md) and
[errors](../reference/errors.md).

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`get_prop`](#get_prop) | The plugin calls it only as `get_prop ["get_status"]`; the reply's first array element is the status object. | ✅ Bundle |
| [`get_status`](#get_status) | Listed in the Methods tables; in the plugin it is the *argument* of `get_prop`, never a method. | ✅ Bundle (parameter value only) |
| [`app_get_status`](#app_get_status) | The `GetStatus` entry of the alternate (`saphire`) table; not active for any shipped bundle. | ✅ Bundle (alternate table only) |
| [`app_get_init_status`](#app_get_init_status) | Called once when the plugin starts; delivers the robot location and the capability lists. | ✅ Bundle |
| [`get_fw_features`](#get_fw_features) | Returns the array of firmware feature codes; called only by the a01, c1, e2, s5 and v1 bundles. | ✅ Bundle |
| [`get_serial_number`](#get_serial_number) | Returns the robot serial number. | ✅ Bundle |
| [`app_get_locale`](#app_get_locale) | Returns the location, language, time zone and related profile fields. | ✅ Bundle |
| [`get_testid`](#get_testid) | Debug-page query returning `testid` and `vnid`. | ✅ Bundle |
| [`app_stat`](#app_stat) | Sends batches of UI-usage counters to the robot. | ✅ Bundle |
| [`get_dock_info`](#get_dock_info) | Reads dock details; used on debug and settings pages for dock type O4. | ✅ Bundle |

<a id="get_prop"></a>
### `get_prop` — Read properties (used for the status poll)

The plugin calls it only as `get_prop ["get_status"]`; the reply's first array element is the status object.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`); map download (`getMapData` -> RPC returning a file name, then HTTPS download; see [maps](../concepts/maps-overview.md)) |

**Request**

`params`: `["get_status"]` (the string is the Methods-table value of key `GetStatus`).
Seen in every bundle: `RobotApi.getStatus` / direct `callMethod(Methods.GetProp, [Methods.GetStatus])`.
One older bundle (a01 family map manager) also calls `get_prop` with the object `{"params": "app_get_map"}` through its
map-download helper (✅ Bundle · a01 m10010).

**Response**

`result` is an array whose first element is the status object (`res.result[0]`), see
[status fields](../reference/status-fields.md). Other property names are not requested by any bundle
(❓ Unknown whether the firmware supports other `get_prop` arguments).

**Example** — constructed from app code

```json
{"id": 1, "method": "get_prop", "params": ["get_status"]}
```

**Behaviour in the app**

- Poll interval `LoopDelay` = 2000 ms (a65 m10010). The loop starts when the main page opens.
- On failure with error code `-10002` (access denied) the app marks the connection as invalid and shows the
  "error 10002" dialog once; other failures only log.
- The app derives *computed states* from the reply (e.g. 6301–6310, 202, 103, 100); see [states](../reference/states.md).

**Legacy documentation**

⚪ Legacy [status.md](../../status.md) documents `get_status` as a method. **Correction:** no bundle sends
`get_status` as the *method*; the string only appears as the parameter of `get_prop`. (The reply shape is the same.)

**Related:** [`get_status`](status.md#get_status), [`app_get_init_status`](status.md#app_get_init_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getStatus`); call sites m10010; table key `GetProp` · anchor `"GetProp"`
- `a65@1.0.95` · wrapper m10115 (`getStatus`); call sites m10010; table key `GetProp` · anchor `"GetProp"`
- `t4@1.0.32` · wrapper m10010 (`getStatus`); call sites m10007, m10649, m11459; table key `GetProp` · anchor `"GetProp"`

</details>

<a id="get_status"></a>
### `get_status` — Status (parameter value of get_prop)

Listed in the Methods tables; in the plugin it is the *argument* of `get_prop`, never a method.

| | |
|---|---|
| Evidence | ✅ Bundle (parameter value only) — no call site found in the bundles |
| Other bundles | parameter value of another call only: all 42 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

See [`get_prop`](#get_prop).

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Legacy documentation**

⚪ Legacy documents `get_status` as a direct method (python-miio and openHAB also use `get_status`). The bundles do not
show a direct call, so whether firmware answers `get_status` as a method is ❓ Unknown from the bundles.

**Related:** [`get_prop`](status.md#get_prop)

<details><summary>Sources</summary>


</details>

<a id="app_get_status"></a>
### `app_get_status` — Status (alternate-table name)

The `GetStatus` entry of the alternate (`saphire`) table; not active for any shipped bundle.

| | |
|---|---|
| Evidence | ✅ Bundle (alternate table only) — no call site found in the bundles |
| Other bundles | alternate table only: all 42 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

❓ Unknown — never called.

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Related:** [`get_status`](status.md#get_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · Methods table · anchor `"app_get_status"`
- `a65@1.0.95` · Methods table · anchor `"app_get_status"`
- `t4@1.0.32` · Methods table · anchor `"app_get_status"`

</details>

<a id="app_get_init_status"></a>
### `app_get_init_status` — Initial status: location, firmware feature lists

Called once when the plugin starts; delivers the robot location and the capability lists.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 38: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5 s5e s6 t4 t6 model(s) |
| Other bundles | wrapper only: 4: a01 c1 e2 v1 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` fields read by the plugin (✅ Bundle · a65 m10007 `fetchDeviceLocation`):

| Field | Type | Use |
|---|---|---|
| `local_info.location` | string | robot location (`prc` is rewritten to `cn`); drives region gating (`cn`, `us`, `de`, …) |
| `local_info.featureset` | int | bit 0 = "FCC state" (`& 0x01`) |
| `feature_info` | int array | firmware feature codes (101…130), see [feature flags](../concepts/feature-flags.md) |
| `new_feature_info` | int (up to 64 bit) | firmware feature bit mask |
| `new_feature_info_str` | string (hex digits, length a multiple of 8) | second, wider feature word read by the newer `FeatureManager`: the last 8 hex digits and the three digits before them are tested bit by bit (see [feature flags](../concepts/feature-flags.md#feature-word-new_feature_info_str)) |

**Example** — constructed from field names read by the app

```json
{"result": [{"local_info": {"location": "de", "featureset": 1}, "feature_info": [111, 112, 114, 116],
             "new_feature_info": 1073741825, "new_feature_info_str": "…"}], "id": 2}
```

**Behaviour in the app**

On failure the app retries after 1 s. After success it also fetches the serial number and syncs the time zone.

**Legacy documentation**

⚪ Legacy [init_status.md](../../init_status.md) lists the reply keys `local_info`, `feature_info` and `status_info` (a status object); the plugin reads the first two and
the two `new_feature_*` keys, and does not read `status_info` from this reply (no bundle contains the key). README lists it as "s5e only". The bundles of 38 models call it; a01, c1, e2 and v1 only wrap it.

**Related:** [`get_fw_features`](status.md#get_fw_features), [`app_get_locale`](status.md#app_get_locale), [`get_serial_number`](status.md#get_serial_number)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getInitStatus`); call sites m10007; table key `GetInitStatus` · anchor `"GetInitStatus"`
- `a65@1.0.95` · wrapper m10115 (`getInitStatus`); call sites m10007; table key `GetInitStatus` · anchor `"GetInitStatus"`
- `t4@1.0.32` · wrapper m10010 (`getInitStatus`); call sites m10628; table key `GetInitStatus` · anchor `"GetInitStatus"`

</details>

<a id="get_fw_features"></a>
### `get_fw_features` — Firmware feature list

Returns the array of firmware feature codes; called only by the a01, c1, e2, s5 and v1 bundles.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 5: a01 c1 e2 s5 v1 model(s) |
| Other bundles | wrapper only: 37: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5e s6 t4 t6 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result` is the plain array of codes (a01: `robotFeatures = resFeature.result`). Newer bundles take the same list from
`feature_info` of [`app_get_init_status`](#app_get_init_status) and never call this method (the wrapper exists).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_fw_features", "params": []}
```

**Behaviour in the app**

Called by the bundles of a01, c1, e2, s5 and v1 (a01: unless the model is `isSapphireCC`; v1: as part of start-up).

**Legacy documentation**

⚪ Legacy [fw_features.md](../../fw_features.md). The code meanings listed there are cross-checked in
[feature flags](../concepts/feature-flags.md).

**Related:** [`app_get_init_status`](status.md#app_get_init_status)

<details><summary>Sources</summary>

- `a01@1.0.51` · wrapper m10013 (`getFWFeatures`); call sites m10502, m11582; table key `GetFWFeatures` · anchor `"GetFWFeatures"`
- `e2@1.0.48` · wrapper m10013 (`getFWFeatures`); call sites m10499, m11579; table key `GetFWFeatures` · anchor `"GetFWFeatures"`
- `v1@1.0.46` · wrapper m10010 (`getFWFeatures`); call sites m10445; table key `GetFWFeatures` · anchor `"GetFWFeatures"`

</details>

<a id="get_serial_number"></a>
### `get_serial_number` — Serial number

Returns the robot serial number.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0].serial_number` (string) is read (a65 m13964 `getSn`); the number is then used to look up a privacy code.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_serial_number", "params": []}
```

**Legacy documentation**

⚪ Legacy [serial_number.md](../../serial_number.md).

**Related:** [`app_get_init_status`](status.md#app_get_init_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getSerialNumber`); call sites m10007, m13979, m14117, m14123, m14147; table key `GetSerialNumber` · anchor `"GetSerialNumber"`
- `a65@1.0.95` · wrapper m10115 (`getSerialNumber`); call sites m10007, m13964, m14087, m14093, m14117; table key `GetSerialNumber` · anchor `"GetSerialNumber"`
- `t4@1.0.32` · wrapper m10010 (`getSerialNumber`); call sites m10562, m11249, m11363, m11369, m11492; table key `GetSerialNumber` · anchor `"GetSerialNumber"`

</details>

<a id="app_get_locale"></a>
### `app_get_locale` — Locale information

Returns the location, language, time zone and related profile fields.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

Fields displayed on the "robot information" page (✅ Bundle · a65 m14156): `location`, `language`, `wifiplan`,
`logserver`, `timezone`, `bom`, `name` (profile) and `featureset`.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_get_locale", "params": []}
```

**Legacy documentation**

⚪ Legacy [locale.md](../../locale.md) lists the same field names — confirmed; `wifiplan`, `name` and `featureset`
meanings remain unexplained by the bundles (the app only shows the strings).

**Related:** [`app_get_init_status`](status.md#app_get_init_status), [`get_timezone`](system.md#get_timezone)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getLocale`); call sites m14186; table key `GetRobotLocale` · anchor `"GetRobotLocale"`
- `a65@1.0.95` · wrapper m10115 (`getLocale`); call sites m14156; table key `GetRobotLocale` · anchor `"GetRobotLocale"`
- `t4@1.0.32` · wrapper m10010 (`getLocale`); call sites m11492; table key `GetRobotLocale` · anchor `"GetRobotLocale"`

</details>

<a id="get_testid"></a>
### `get_testid` — Anonymous test id

Debug-page query returning `testid` and `vnid`.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 36: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5 s5e s6 t4 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0].testid`, `result[0].vnid` (strings); the debug page shows the list item only when `testid` is non-empty.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_testid", "params": []}
```

**Related:** [`get_dock_info`](status.md#get_dock_info)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getAnonymousID`); call sites m14405 · anchor `"get_testid"`
- `a65@1.0.95` · wrapper m10115 (`getAnonymousID`); call sites m14375 · anchor `"get_testid"`
- `t4@1.0.32` · wrapper m10010 (`getAnonymousID`); call sites m11363 · anchor `"get_testid"`

</details>

<a id="app_stat"></a>
### `app_stat` — Usage statistics upload

Sends batches of UI-usage counters to the robot.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 41: a01 a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 c1 e2 m1s p5 s4 s5 s5e s6 t4 t6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[{"ver": <int>, "data": [ {…item…}, … ]}]`; the app packs items into batches limited by a byte budget
(a65 m10031 `Stat`). The item layout is internal to the statistics module and not documented here (❓ Unknown).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`appStat`); call sites m10031; table key `AppStat` · anchor `"AppStat"`
- `a65@1.0.95` · wrapper m10115 (`appStat`); call sites m10031; table key `AppStat` · anchor `"AppStat"`
- `t4@1.0.32` · call sites m10595; table key `AppStat` · anchor `"AppStat"`

</details>

<a id="get_dock_info"></a>
### `get_dock_info` — Dock information

Reads dock details; used on debug and settings pages for dock type O4.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`{}` in the wrapper).

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result[0]` (3). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_dock_info", "params": {}}
```

**Behaviour in the app**

Called only when `RSM.isO4Dock()` is true (a65 m14375, m14516).

**Related:** [`update_dock`](dock.md#update_dock)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getDockInfo`); call sites m14405, m14570 · anchor `"get_dock_info"`
- `a65@1.0.95` · wrapper m10115 (`getDockInfo`); call sites m14375, m14516 · anchor `"get_dock_info"`
- `a29@1.0.75` · wrapper m10112 (`getDockInfo`); call sites m14105 · anchor `"get_dock_info"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
