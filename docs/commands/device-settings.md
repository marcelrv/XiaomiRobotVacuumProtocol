# Device settings

[Home](../../README.md) / [Commands](index.md) / Device settings

LED, child lock and sensor behaviour switches.

Simple on/off settings. Replies are objects or arrays depending on the call; the read calls below say which. The status
object also exposes some of these switches (`lock_status`, `switch_status`, `camera_status`, …), see
[status fields](../reference/status-fields.md).

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`get_led_status`](#get_led_status) | Reads the LED switch. | ✅ Bundle |
| [`set_led_status`](#set_led_status) | Switches the robot status LED. | ✅ Bundle |
| [`get_flow_led_status`](#get_flow_led_status) | Reads the "flow" LED switch. | ✅ Bundle |
| [`set_flow_led_status`](#set_flow_led_status) | Switches the flow LED. | ✅ Bundle |
| [`get_child_lock_status`](#get_child_lock_status) | Reads the child-lock switch (status field `lock_status` also reports it). | ✅ Bundle |
| [`set_child_lock_status`](#set_child_lock_status) | Switches the child lock. | ✅ Bundle |
| [`get_collision_avoid_status`](#get_collision_avoid_status) | Reads the "avoid collision" (bumper-sensor) switch. | ✅ Bundle |
| [`set_collision_avoid_status`](#set_collision_avoid_status) | Switches the setting. | ✅ Bundle |

<a id="get_led_status"></a>
### `get_led_status` — Status LED (read)

Reads the LED switch.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

Result layout not decoded for all bundles (`result[0]` is the value in older bundles).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_led_status", "params": []}
```

**Behaviour in the app**

Shown when `isLedSwitchVisible` (not for the `TanosS` product unless fw feature 119 is present).

**Related:** [`set_led_status`](device-settings.md#set_led_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getLedStatus`); call sites m14168; table key `GetLedStatus` · anchor `"GetLedStatus"`
- `a65@1.0.95` · wrapper m10115 (`getLedStatus`); call sites m14138; table key `GetLedStatus` · anchor `"GetLedStatus"`
- `t4@1.0.32` · wrapper m10010 (`getLedStatus`); call sites m11453; table key `GetLedStatus` · anchor `"GetLedStatus"`

</details>

<a id="set_led_status"></a>
### `set_led_status` — Status LED (write)

Switches the robot status LED.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[0|1]`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_led_status", "params": [1]}
```

**Related:** [`get_led_status`](device-settings.md#get_led_status), [`set_flow_led_status`](device-settings.md#set_flow_led_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setLedStatus`); call sites m14168; table key `SetLedStatus` · anchor `"SetLedStatus"`
- `a65@1.0.95` · wrapper m10115 (`setLedStatus`); call sites m14138; table key `SetLedStatus` · anchor `"SetLedStatus"`
- `t4@1.0.32` · wrapper m10010 (`setLedStatus`); call sites m11453; table key `SetLedStatus` · anchor `"SetLedStatus"`

</details>

<a id="get_flow_led_status"></a>
### `get_flow_led_status` — Flow LED (read)

Reads the "flow" LED switch.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.status == 1` means on.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_flow_led_status", "params": []}
```

**Behaviour in the app**

New-feature bit `isFlowLedSettingSupported` (low word bit 24).

**Related:** [`set_flow_led_status`](device-settings.md#set_flow_led_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getFlowSettingStatus`); call sites m14168 · anchor `"get_flow_led_status"`
- `a65@1.0.95` · wrapper m10115 (`getFlowSettingStatus`); call sites m14138 · anchor `"get_flow_led_status"`
- `a14@1.0.53` · wrapper m10142 (`getFlowSettingStatus`); call sites m13007 · anchor `"get_flow_led_status"`

</details>

<a id="set_flow_led_status"></a>
### `set_flow_led_status` — Flow LED (write)

Switches the flow LED.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"status": 0|1}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_flow_led_status", "params": {"status": 1}}
```

**Related:** [`get_flow_led_status`](device-settings.md#get_flow_led_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setFlowSettingStatus`); call sites m14168 · anchor `"set_flow_led_status"`
- `a65@1.0.95` · wrapper m10115 (`setFlowSettingStatus`); call sites m14138 · anchor `"set_flow_led_status"`
- `a14@1.0.53` · wrapper m10142 (`setFlowSettingStatus`); call sites m13007 · anchor `"set_flow_led_status"`

</details>

<a id="get_child_lock_status"></a>
### `get_child_lock_status` — Child lock (read)

Reads the child-lock switch (status field `lock_status` also reports it).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result.lock_status` (32). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_child_lock_status", "params": []}
```

**Behaviour in the app**

Only read when `isSetChildSupported` (new-feature low word bit 8).

**Related:** [`set_child_lock_status`](device-settings.md#set_child_lock_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getChildLockStatus`); call sites m14168 · anchor `"get_child_lock_status"`
- `a65@1.0.95` · wrapper m10115 (`getChildLockStatus`); call sites m14138 · anchor `"get_child_lock_status"`
- `a08@1.0.47` · wrapper m10013 (`getChildLockStatus`); call sites m12254 · anchor `"get_child_lock_status"`

</details>

<a id="set_child_lock_status"></a>
### `set_child_lock_status` — Child lock (write)

Switches the child lock.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"lock_status": 0|1}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_child_lock_status", "params": {"lock_status": 1}}
```

**Related:** [`get_child_lock_status`](device-settings.md#get_child_lock_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setChildLockStatus`); call sites m14168 · anchor `"set_child_lock_status"`
- `a65@1.0.95` · wrapper m10115 (`setChildLockStatus`); call sites m14138 · anchor `"set_child_lock_status"`
- `a08@1.0.47` · wrapper m10013 (`setChildLockStatus`); call sites m12254 · anchor `"set_child_lock_status"`

</details>

<a id="get_collision_avoid_status"></a>
### `get_collision_avoid_status` — Collision avoidance (read)

Reads the "avoid collision" (bumper-sensor) switch.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |
| Call-site gate | the call sits behind `isAvoidCollisionSupported` (tests found in the enclosing code of the call sites; [feature flags](../concepts/feature-flags.md)) |

**Request**

`params`: none (`[]`).

**Response**

`result.status == 1` means on.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_collision_avoid_status", "params": []}
```

**Behaviour in the app**

New-feature bit `isAvoidCollisionSupported` (low word bit 27).

**Related:** [`set_collision_avoid_status`](device-settings.md#set_collision_avoid_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCollisionAvoidStatus`); call sites m14285, m14405 · anchor `"get_collision_avoid_status"`
- `a65@1.0.95` · wrapper m10115 (`getCollisionAvoidStatus`); call sites m14255, m14375 · anchor `"get_collision_avoid_status"`
- `a14@1.0.53` · wrapper m10142 (`getCollisionAvoidStatus`); call sites m13286 · anchor `"get_collision_avoid_status"`

</details>

<a id="set_collision_avoid_status"></a>
### `set_collision_avoid_status` — Collision avoidance (write)

Switches the setting.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"status": 0|1}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_collision_avoid_status", "params": {"status": 1}}
```

**Related:** [`get_collision_avoid_status`](device-settings.md#get_collision_avoid_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCollisionAvoidStatus`); call sites m13031, m14285, m14405 · anchor `"set_collision_avoid_status"`
- `a65@1.0.95` · wrapper m10115 (`setCollisionAvoidStatus`); call sites m13019, m14255, m14375 · anchor `"set_collision_avoid_status"`
- `a14@1.0.53` · wrapper m10142 (`setCollisionAvoidStatus`); call sites m13286 · anchor `"set_collision_avoid_status"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
