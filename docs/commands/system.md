# Network, time, firmware and logs

[Home](../../README.md) / [Commands](index.md) / Network, time, firmware and logs

Wi-Fi information, time zone, OTA and log upload.

Wi-Fi information, time zone, firmware update and log upload. The generic `miIO.*` methods that every Xiaomi device
understands (`miIO.info`, `miIO.config_router`, `miIO.get_ota_state`, …) are **not** called by these plugins, except for
`miIO.ota`; see [generic miIO methods](../concepts/miio-protocol.md#generic-methods).

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`get_network_info`](#get_network_info) | Returns SSID, signal strength, IP and MAC address. | ✅ Bundle |
| [`app_get_wifi_list`](#app_get_wifi_list) | Returns the networks stored on the robot. | ✅ Bundle |
| [`app_delete_wifi`](#app_delete_wifi) | Deletes a stored network. | ✅ Bundle |
| [`get_timezone`](#get_timezone) | Returns the robot's time zone name. | ✅ Bundle |
| [`set_timezone`](#set_timezone) | Sets the robot's time zone. | ✅ Bundle |
| [`set_app_timezone`](#set_app_timezone) | Sent at start-up so that the robot knows the phone's time zone and mobile country code. | ✅ Bundle |
| [`miIO.ota`](#miIO.ota) | Starts an OTA with an explicit URL; only used by a debug page. | ✅ Bundle |
| [`enable_log_upload`](#enable_log_upload) | Tells the robot how much logging it may upload; sent when the privacy agreement is accepted. | ✅ Bundle |
| [`get_log_upload_status`](#get_log_upload_status) | In every Methods table; no call site. | ✅ Bundle (declared only) |
| [`user_upload_log`](#user_upload_log) | Asks the robot to upload its logs (the "report a problem" button). | ✅ Bundle |
| [`upload_data_for_debug_mode`](#upload_data_for_debug_mode) | Starts a debug data upload from the debug page. | ✅ Bundle |
| [`set_fds_endpoint`](#set_fds_endpoint) | Tells the robot which file-storage host to use for uploads (maps, logs). | ✅ Bundle |

<a id="get_network_info"></a>
### `get_network_info` — Wi-Fi information

Returns SSID, signal strength, IP and MAC address.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result` (object): `ssid`, `rssi`, `ip`, `mac` (✅ Bundle · a65 m14105 and m14093); missing values are shown as "Unknown".

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_network_info", "params": []}
```

**Legacy documentation**

⚪ Legacy [network_info.md](../../network_info.md) — the README lists it as "s5e, s5, s7, s6"; the bundles call it in all of them.

**Related:** [`app_get_wifi_list`](system.md#app_get_wifi_list)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getNetworkInfo`); call sites m14123, m14135, m14306, m14405, m14570; table key `GetNetworkInfo` · anchor `"GetNetworkInfo"`
- `a65@1.0.95` · wrapper m10115 (`getNetworkInfo`); call sites m14093, m14105, m14276, m14375, m14516; table key `GetNetworkInfo` · anchor `"GetNetworkInfo"`
- `t4@1.0.32` · wrapper m10010 (`getNetworkInfo`); call sites m11369, m11474; table key `GetNetworkInfo` · anchor `"GetNetworkInfo"`

</details>

<a id="app_get_wifi_list"></a>
### `app_get_wifi_list` — Saved Wi-Fi networks

Returns the networks stored on the robot.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

`result` is an array of objects with `ssid` and `id`; the app hides the currently connected SSID.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_get_wifi_list", "params": {}}
```

**Related:** [`app_delete_wifi`](system.md#app_delete_wifi)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getWifiList`); call sites m14591 · anchor `"app_get_wifi_list"`
- `a65@1.0.95` · wrapper m10115 (`getWifiList`); call sites m14537 · anchor `"app_get_wifi_list"`
- `a29@1.0.75` · wrapper m10112 (`getWifiList`); call sites m14267 · anchor `"app_get_wifi_list"`

</details>

<a id="app_delete_wifi"></a>
### `app_delete_wifi` — Forget a Wi-Fi network

Deletes a stored network.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"id": <int>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_delete_wifi", "params": {"id": 1}}
```

**Related:** [`app_get_wifi_list`](system.md#app_get_wifi_list)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`deleteWifi`); call sites m14591 · anchor `"app_delete_wifi"`
- `a65@1.0.95` · wrapper m10115 (`deleteWifi`); call sites m14537 · anchor `"app_delete_wifi"`
- `a29@1.0.75` · wrapper m10112 (`deleteWifi`); call sites m14267 · anchor `"app_delete_wifi"`

</details>

<a id="get_timezone"></a>
### `get_timezone` — Robot time zone (read)

Returns the robot's time zone name.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` is a tz database name (e.g. `Europe/Amsterdam`); the app compares it with the phone zone and shows a red dot if they differ.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_timezone", "params": []}
```

**Legacy documentation**

⚪ Legacy [timezone.md](../../timezone.md) — confirmed.

**Related:** [`set_timezone`](system.md#set_timezone), [`set_app_timezone`](system.md#set_app_timezone)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getTimeZone`); call sites m13985, m14561, m14570; table key `GetTimezone` · anchor `"GetTimezone"`
- `a65@1.0.95` · wrapper m10115 (`getTimeZone`); call sites m13970, m14507, m14516; table key `GetTimezone` · anchor `"GetTimezone"`
- `t4@1.0.32` · wrapper m10010 (`getTimeZone`); call sites m11204, m11369, m11453; table key `GetTimezone` · anchor `"GetTimezone"`

</details>

<a id="set_timezone"></a>
### `set_timezone` — Robot time zone (write)

Sets the robot's time zone.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `["<tz name>"]` in most bundles; the a01 family sends the object `{"olson": "<tz name>", "posix": "<POSIX tz string>"}`
(✅ Bundle · a01 wrapper `setTimezone(timeZone, posix)`; a65 m14135 `setTimezone(timeZone)`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_timezone", "params": ["Europe/Berlin"]}
```

**Related:** [`get_timezone`](system.md#get_timezone)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setTimezone`); call sites m14165; table key `SetTimezone` · anchor `"SetTimezone"`
- `a65@1.0.95` · wrapper m10115 (`setTimezone`); call sites m14135; table key `SetTimezone` · anchor `"SetTimezone"`
- `t4@1.0.32` · wrapper m10010 (`setTimezone`); call sites m11450; table key `SetTimezone` · anchor `"SetTimezone"`

</details>

<a id="set_app_timezone"></a>
### `set_app_timezone` — Tell the robot the app's zone and country

Sent at start-up so that the robot knows the phone's time zone and mobile country code.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<tz name>, <mcc>]` (the phone zone and the MCC, `0` when unknown; a65 m10007).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_app_timezone", "params": ["Europe/Berlin", 0]}
```

**Behaviour in the app**

After the call the plugin re-reads the location (`app_get_init_status`).

**Related:** [`app_get_init_status`](status.md#app_get_init_status), [`get_timezone`](system.md#get_timezone)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setAppTimezone`); call sites m10007; table key `SetAppTimezone` · anchor `"SetAppTimezone"`
- `a65@1.0.95` · wrapper m10115 (`setAppTimezone`); call sites m10007; table key `SetAppTimezone` · anchor `"SetAppTimezone"`
- `t4@1.0.32` · wrapper m10010 (`setAppTimezone`); call sites m10628; table key `SetAppTimezone` · anchor `"SetAppTimezone"`

</details>

<a id="miIO.ota"></a>
### `miIO.ota` — Firmware update (test page)

Starts an OTA with an explicit URL; only used by a debug page.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 3: a14 a15 a23 model(s) |
| Other bundles | wrapper only: 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"app_url": "<url>", "file_md5": "<md5>", "proc": <v>, "mode": <v>, "install": <v>}` (a14 wrapper `otaMiIot`).

**Response**

The debug page shows the raw reply as text.

**Legacy documentation**

⚪ Legacy [miIO-ota.md](../../miIO-ota.md): `{"mode": "normal", "install": "1", "app_url": …, "file_md5": …, "proc": "dnld install"}` — same keys.

<details><summary>Sources</summary>

- `a23@1.0.53` · wrapper m10142 (`otaMiIot`); call sites m13298 · anchor `"miIO.ota"`
- `a15@1.0.53` · wrapper m10142 (`otaMiIot`); call sites m13298 · anchor `"miIO.ota"`
- `a14@1.0.53` · wrapper m10142 (`otaMiIot`); call sites m13298 · anchor `"miIO.ota"`

</details>

<a id="enable_log_upload"></a>
### `enable_log_upload` — Log-upload consent level

Tells the robot how much logging it may upload; sent when the privacy agreement is accepted.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<level>, <privacy name>]`, or `[<level>]` in older bundles. `level` is `0` when the user disagrees and
the product's *agree level* otherwise (3 for the `Rubys` product, 9 for all others; a65 m10139 `agreeProtocolLevel`).
The named levels of the plugin are `LogLevel` None 0, BlackBox 1, Pickup 2, Full 4; `privacyName` codes: `PN_NONE` 0,
`PN_CN` 1, `PN_GENERAL` 2, `PN_EU` 3 ([enums](../reference/other-enums.md)). The app retries up to 4 times.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Legacy documentation**

⚪ Legacy [log_upload.md](../../log_upload.md).

**Related:** [`get_log_upload_status`](system.md#get_log_upload_status), [`set_fds_endpoint`](system.md#set_fds_endpoint)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setLogLevel`); call sites m10007; table key `EnableLogUpload` · anchor `"EnableLogUpload"`
- `a65@1.0.95` · wrapper m10115 (`setLogLevel`); call sites m10007; table key `EnableLogUpload` · anchor `"EnableLogUpload"`
- `t4@1.0.32` · wrapper m10010 (`setLogLevel`); call sites m10628; table key `EnableLogUpload` · anchor `"EnableLogUpload"`

</details>

<a id="get_log_upload_status"></a>
### `get_log_upload_status` — Log-upload status (declared only)

In every Methods table; no call site.

| | |
|---|---|
| Evidence | ✅ Bundle (declared only) — no call site found in the bundles |
| Other bundles | declared only: all 42 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

❓ Unknown.

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Related:** [`enable_log_upload`](system.md#enable_log_upload)

<details><summary>Sources</summary>

- `a74@1.0.96` · table key `GetLogUploadStatus` · anchor `"GetLogUploadStatus"`
- `a65@1.0.95` · table key `GetLogUploadStatus` · anchor `"GetLogUploadStatus"`
- `t4@1.0.32` · table key `GetLogUploadStatus` · anchor `"GetLogUploadStatus"`

</details>

<a id="user_upload_log"></a>
### `user_upload_log` — Upload logs now

Asks the robot to upload its logs (the "report a problem" button).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 38: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5 s5e s6 t4 t6 model(s) |
| Other bundles | declared only: 4: a01 c1 e2 v1 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "user_upload_log", "params": []}
```

**Related:** [`enable_log_upload`](system.md#enable_log_upload)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`userUploadLog`); call sites m14117, m14306, m14570; table key `UserUploadLog` · anchor `"UserUploadLog"`
- `a65@1.0.95` · wrapper m10115 (`userUploadLog`); call sites m14087, m14276, m14516; table key `UserUploadLog` · anchor `"UserUploadLog"`
- `t4@1.0.32` · call sites m11363; table key `UserUploadLog` · anchor `"UserUploadLog"`

</details>

<a id="upload_data_for_debug_mode"></a>
### `upload_data_for_debug_mode` — Debug-data upload

Starts a debug data upload from the debug page.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "upload_data_for_debug_mode", "params": []}
```

**Related:** [`user_upload_log`](system.md#user_upload_log)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`uploadDataDebugMode`); call sites m14420 · anchor `"upload_data_for_debug_mode"`
- `a65@1.0.95` · wrapper m10115 (`uploadDataDebugMode`); call sites m14390 · anchor `"upload_data_for_debug_mode"`
- `a14@1.0.53` · wrapper m10142 (`uploadDataDebugMode`); call sites m13301 · anchor `"upload_data_for_debug_mode"`

</details>

<a id="set_fds_endpoint"></a>
### `set_fds_endpoint` — Set the file-service endpoint

Tells the robot which file-storage host to use for uploads (maps, logs).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<host>]` — chosen from the account region; sent at plugin start together with the log level.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_fds_endpoint", "params": ["host.example.invalid"]}
```

**Behaviour in the app**

Supported when fw feature code 111 (`isSupportFDSEndPoint`) is present.

**Legacy documentation**

⚪ Legacy fw_features.md: "Supports FSEndPoint" for code 111 — consistent.

**Related:** [`enable_log_upload`](system.md#enable_log_upload)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setFDSEndpoint`); call sites m10007; table key `SetFdsEndpoint` · anchor `"SetFdsEndpoint"`
- `a65@1.0.95` · wrapper m10115 (`setFDSEndpoint`); call sites m10007; table key `SetFdsEndpoint` · anchor `"SetFdsEndpoint"`
- `t4@1.0.32` · wrapper m10010 (`setFDSEndpoint`); call sites m10628; table key `SetFdsEndpoint` · anchor `"SetFdsEndpoint"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
