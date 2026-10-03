# Camera, live view and home security

[Home](../../README.md) / [Commands](index.md) / Camera, live view and home security

Camera switch, live-view negotiation (WebRTC-style signalling) and the home-security password.

Robots with a camera or structured-light sensor expose a switch word ([`get_camera_status`](#get_camera_status)), a
live-view signalling exchange (WebRTC-style: the app sends an SDP offer and ICE candidates, polls the robot's answer, and
asks for TURN server information) and a home-security password. Everything on this page is only reachable for products
with `isCameraSupported` or `isStructuredLightSupported` (see the [device pages](../devices/index.md)). Session
secrets, keys and endpoints seen in the code are intentionally not recorded.

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`get_camera_status`](#get_camera_status) | Returns a bit field with the camera-related switches. | ✅ Bundle |
| [`set_camera_status`](#set_camera_status) | Writes the whole bit field. | ✅ Bundle |
| [`start_camera_preview`](#start_camera_preview) | Starts the camera stream on the robot. | ✅ Bundle |
| [`stop_camera_preview`](#stop_camera_preview) | Stops the stream. | ✅ Bundle |
| [`get_turn_server`](#get_turn_server) | Returns relay information for the live view. | ✅ Bundle |
| [`send_sdp_to_robot`](#send_sdp_to_robot) | Sends the app side session description. | ✅ Bundle |
| [`send_ice_to_robot`](#send_ice_to_robot) | Sends one candidate. | ✅ Bundle |
| [`get_device_sdp`](#get_device_sdp) | Polled every 500 ms (default) until the robot has answered. | ✅ Bundle |
| [`get_device_ice`](#get_device_ice) | Polled every 500 ms (default). | ✅ Bundle |
| [`switch_video_quality`](#switch_video_quality) | Chooses the stream definition. | ✅ Bundle |
| [`switch_water_mark`](#switch_water_mark) | Turns the watermark on or off. | ✅ Bundle |
| [`set_homesec_password`](#set_homesec_password) | Enables, changes or disables the gesture password protecting the live view. | ✅ Bundle |
| [`reset_homesec_password`](#reset_homesec_password) | Removes the password. | ✅ Bundle |
| [`check_homesec_password`](#check_homesec_password) | Checks a password. | ✅ Bundle |
| [`get_homesec_connect_status`](#get_homesec_connect_status) | Returns the client id of the current monitoring session. | ✅ Bundle |
| [`upload_photo`](#upload_photo) | Sends the user's classification of a robot photo back to the robot/cloud. | ✅ Bundle |

<a id="get_camera_status"></a>
### `get_camera_status` — Camera switch word (read)

Returns a bit field with the camera-related switches.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 37: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5 s5e s6 t4 t6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` is an integer bit field (✅ Bundle · a65 m12998 `parseCameraStatus`):

| Bits | Meaning (app name) |
|---|---|
| 0 | camera enabled |
| 1 | pet mode |
| 2 | real-time monitor |
| 3–4 | LED setting (2 bits) |
| 5 | monitor privacy policy agreed |
| 6 | exploration enabled |
| 7 | "pet mode alert shown" |
| 8–9 | video setting (2 bits; only with new-feature bit `isVideoSettingSupported`) |
| 10 | map-object photo enabled |
| 11 | map-object photo privacy policy agreed |

The same word is also present in the status object as `camera_status`.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_camera_status", "params": []}
```

**Related:** [`set_camera_status`](camera.md#set_camera_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCameraStatus`); call sites m13010 · anchor `"get_camera_status"`
- `a65@1.0.95` · wrapper m10115 (`getCameraStatus`); call sites m12998 · anchor `"get_camera_status"`
- `t4@1.0.32` · wrapper m10010 (`getCameraStatus`); call sites m11453 · anchor `"get_camera_status"`

</details>

<a id="set_camera_status"></a>
### `set_camera_status` — Camera switch word (write)

Writes the whole bit field.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 37: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5 s5e s6 t4 t6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<int>]` — the OR of the bits above (a65 m12998 `setCameraStatus`: `cameraVal | pet<<1 | realtime<<2 | led<<3 | privacy<<5 | exploration<<6 | alertShown<<7 | video<<8 | photo<<10 | photoPrivacy<<11`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_camera_status", "params": [1]}
```

**Behaviour in the app**

Because the whole word is written, a client must read the current word first and change only its bit.

**Related:** [`get_camera_status`](camera.md#get_camera_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCameraStatus`); call sites m13010, m14168 · anchor `"set_camera_status"`
- `a65@1.0.95` · wrapper m10115 (`setCameraStatus`); call sites m12998, m14138 · anchor `"set_camera_status"`
- `t4@1.0.32` · wrapper m10010 (`setCameraStatus`); call sites m11453 · anchor `"set_camera_status"`

</details>

<a id="start_camera_preview"></a>
### `start_camera_preview` — Start the live view

Starts the camera stream on the robot.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: an object `para` assembled by the video module (client identification and quality; the layout is internal and not decoded).

**Response**

`result[0] == "ok"` is success.

**Behaviour in the app**

In the status the robot reports the live-view state in `camera_status` bit 2. The app refuses to start while the robot is charging or emptying (video error codes −101, −116; [errors](../reference/errors.md#app-side-codes)).

**Related:** [`stop_camera_preview`](camera.md#stop_camera_preview), [`get_turn_server`](camera.md#get_turn_server), [`send_sdp_to_robot`](camera.md#send_sdp_to_robot)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`startCameraPreview`); call sites m14750 · anchor `"start_camera_preview"`
- `a65@1.0.95` · wrapper m10115 (`startCameraPreview`); call sites m14696 · anchor `"start_camera_preview"`
- `a11@1.0.34` · wrapper m10010 (`startCameraPreview`); call sites m12002 · anchor `"start_camera_preview"`

</details>

<a id="stop_camera_preview"></a>
### `stop_camera_preview` — Stop the live view

Stops the stream.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[]` or an object `param` echoing the client identification.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "stop_camera_preview", "params": []}
```

**Related:** [`start_camera_preview`](camera.md#start_camera_preview)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`stopCameraPreview`); call sites m14750 · anchor `"stop_camera_preview"`
- `a65@1.0.95` · wrapper m10115 (`stopCameraPreview`); call sites m14696 · anchor `"stop_camera_preview"`
- `a11@1.0.34` · wrapper m10010 (`stopCameraPreview`); call sites m12002 · anchor `"stop_camera_preview"`

</details>

<a id="get_turn_server"></a>
### `get_turn_server` — TURN server information

Returns relay information for the live view.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.url`; the string `retry` makes the app ask again.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_turn_server", "params": []}
```

**Related:** [`send_sdp_to_robot`](camera.md#send_sdp_to_robot)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getTurnServerInfo`); call sites m14750 · anchor `"get_turn_server"`
- `a65@1.0.95` · wrapper m10115 (`getTurnServerInfo`); call sites m14696 · anchor `"get_turn_server"`
- `a11@1.0.34` · wrapper m10010 (`getTurnServerInfo`); call sites m12002 · anchor `"get_turn_server"`

</details>

<a id="send_sdp_to_robot"></a>
### `send_sdp_to_robot` — Send the SDP offer (cloud route)

Sends the app side session description.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`); cloud route (`callMethodFromCloud`; inside Mi Home this is the same call as `callMethod`) |

**Request**

`params`: `{"app_sdp": <string>}`; sent through `asyncCallMethodFromCloud` (✅ Bundle · a65 m10115).

**Response**

`result[0] == "ok"` on success.

**Related:** [`get_device_sdp`](camera.md#get_device_sdp), [`send_ice_to_robot`](camera.md#send_ice_to_robot)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`sendSdpInfo`); call sites m14744 · anchor `"send_sdp_to_robot"`
- `a65@1.0.95` · wrapper m10115 (`sendSdpInfo`); call sites m14690 · anchor `"send_sdp_to_robot"`
- `a11@1.0.34` · wrapper m10010 (`sendSdpInfo`); call sites m11996 · anchor `"send_sdp_to_robot"`

</details>

<a id="send_ice_to_robot"></a>
### `send_ice_to_robot` — Send an ICE candidate

Sends one candidate.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"app_ice": <string>}`.

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result[0]` (34). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Related:** [`get_device_ice`](camera.md#get_device_ice)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`sendIceInfo`); call sites m14744 · anchor `"send_ice_to_robot"`
- `a65@1.0.95` · wrapper m10115 (`sendIceInfo`); call sites m14690 · anchor `"send_ice_to_robot"`
- `a11@1.0.34` · wrapper m10010 (`sendIceInfo`); call sites m11996 · anchor `"send_ice_to_robot"`

</details>

<a id="get_device_sdp"></a>
### `get_device_sdp` — Poll the robot SDP answer

Polled every 500 ms (default) until the robot has answered.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result.dev_sdp` (34). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_device_sdp", "params": []}
```

**Related:** [`send_sdp_to_robot`](camera.md#send_sdp_to_robot)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getDeviceSdpInfo`); call sites m14750 · anchor `"get_device_sdp"`
- `a65@1.0.95` · wrapper m10115 (`getDeviceSdpInfo`); call sites m14696 · anchor `"get_device_sdp"`
- `a11@1.0.34` · wrapper m10010 (`getDeviceSdpInfo`); call sites m12002 · anchor `"get_device_sdp"`

</details>

<a id="get_device_ice"></a>
### `get_device_ice` — Poll the robot ICE candidates

Polled every 500 ms (default).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result.dev_ice` (34). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_device_ice", "params": []}
```

**Related:** [`send_ice_to_robot`](camera.md#send_ice_to_robot)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getDeviceIceInfo`); call sites m14750 · anchor `"get_device_ice"`
- `a65@1.0.95` · wrapper m10115 (`getDeviceIceInfo`); call sites m14696 · anchor `"get_device_ice"`
- `a11@1.0.34` · wrapper m10010 (`getDeviceIceInfo`); call sites m12002 · anchor `"get_device_ice"`

</details>

<a id="switch_video_quality"></a>
### `switch_video_quality` — Live-view quality

Chooses the stream definition.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"quality": "<command string>"}` where the string is the `command` of the selected entry of the app's definitions table (the string values are not decoded here).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "switch_video_quality", "params": {"quality": "command"}}
```

**Related:** [`start_camera_preview`](camera.md#start_camera_preview)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setVideoQuality`); call sites m14639, m14654 · anchor `"switch_video_quality"`
- `a65@1.0.95` · wrapper m10115 (`setVideoQuality`); call sites m14585, m14600 · anchor `"switch_video_quality"`
- `a11@1.0.34` · wrapper m10010 (`setVideoQuality`); call sites m11921 · anchor `"switch_video_quality"`

</details>

<a id="switch_water_mark"></a>
### `switch_water_mark` — Live-view watermark

Turns the watermark on or off.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"waterMark": "ON"|"OFF"}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "switch_water_mark", "params": {"waterMark": "ON"}}
```

**Related:** [`start_camera_preview`](camera.md#start_camera_preview)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setWatermark`); call sites m14198 · anchor `"switch_water_mark"`
- `a65@1.0.95` · wrapper m10115 (`setWatermark`); call sites m14168 · anchor `"switch_water_mark"`
- `a62@1.0.69` · wrapper m10109 (`setWatermark`); call sites m13733 · anchor `"switch_water_mark"`

</details>

<a id="set_homesec_password"></a>
### `set_homesec_password` — Set / change the monitoring password

Enables, changes or disables the gesture password protecting the live view.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"enable_password": 0|1, "old_password": "<md5 hex or empty>", "new_password": "<md5 hex or empty>"}` — the app sends the **MD5** of the password, not the password.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_homesec_password", "params": {"enable_password": 1, "old_password": "", "new_password": ""}}
```

**Related:** [`check_homesec_password`](camera.md#check_homesec_password), [`reset_homesec_password`](camera.md#reset_homesec_password)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setSecPassword`); call sites m14246 · anchor `"set_homesec_password"`
- `a65@1.0.95` · wrapper m10115 (`setSecPassword`); call sites m14216 · anchor `"set_homesec_password"`
- `a11@1.0.34` · wrapper m10010 (`setSecPassword`); call sites m11867 · anchor `"set_homesec_password"`

</details>

<a id="reset_homesec_password"></a>
### `reset_homesec_password` — Reset the monitoring password

Removes the password.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "reset_homesec_password", "params": []}
```

**Related:** [`set_homesec_password`](camera.md#set_homesec_password)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`resetSecPassword`); call sites m14246 · anchor `"reset_homesec_password"`
- `a65@1.0.95` · wrapper m10115 (`resetSecPassword`); call sites m14216 · anchor `"reset_homesec_password"`
- `a11@1.0.34` · wrapper m10010 (`resetSecPassword`); call sites m11867 · anchor `"reset_homesec_password"`

</details>

<a id="check_homesec_password"></a>
### `check_homesec_password` — Verify the monitoring password

Checks a password.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"password": "<md5 hex>"}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "check_homesec_password", "params": {"password": "0123456789abcdef0123456789abcdef"}}
```

**Related:** [`set_homesec_password`](camera.md#set_homesec_password)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`checkSecPassword`); call sites m14246 · anchor `"check_homesec_password"`
- `a65@1.0.95` · wrapper m10115 (`checkSecPassword`); call sites m14216 · anchor `"check_homesec_password"`
- `a11@1.0.34` · wrapper m10010 (`checkSecPassword`); call sites m11867 · anchor `"check_homesec_password"`

</details>

<a id="get_homesec_connect_status"></a>
### `get_homesec_connect_status` — Monitoring connection status

Returns the client id of the current monitoring session.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Other bundles | wrapper only: 1: a11 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.client_id` (kept as `homeSecClientID`); the status field `home_sec_status` carries the connection state (`RRHomeSecStatus`: 0 disconnected, 1 connected, 2 disconnecting).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_homesec_connect_status", "params": []}
```

**Related:** [`start_camera_preview`](camera.md#start_camera_preview)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getHomeSecConnectStatus`); call sites m14639 · anchor `"get_homesec_connect_status"`
- `a65@1.0.95` · wrapper m10115 (`getHomeSecConnectStatus`); call sites m14585 · anchor `"get_homesec_connect_status"`
- `a08@1.0.47` · wrapper m10013 (`getHomeSecConnectStatus`); call sites m12569 · anchor `"get_homesec_connect_status"`

</details>

<a id="upload_photo"></a>
### `upload_photo` — Report an obstacle photo classification

Sends the user's classification of a robot photo back to the robot/cloud.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"photos": [{"id": <photo id>, "src_type": <int>, "actual_type": <int>}]}` (a65 m14309).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "upload_photo", "params": {"photos": [{"id": 1, "src_type": 1, "actual_type": 1}]}}
```

**Behaviour in the app**

New-feature bit `isPhotoUploadSupported` (low word bit 16).

**Related:** [`get_photo`](maps.md#get_photo)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`uploadObstaclesPhotos`); call sites m14339 · anchor `"upload_photo"`
- `a65@1.0.95` · wrapper m10115 (`uploadObstaclesPhotos`); call sites m14309 · anchor `"upload_photo"`
- `a08@1.0.47` · wrapper m10013 (`uploadObstaclesPhotos`); call sites m12440 · anchor `"upload_photo"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
