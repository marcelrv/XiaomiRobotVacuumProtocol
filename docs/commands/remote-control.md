# Remote control

[Home](../../README.md) / [Commands](index.md) / Remote control

Manual driving of the robot.

Manual driving works in four steps: [`app_rc_start`](#app_rc_start) enters remote-control mode (robot state `REMOTE`, 7),
[`app_rc_move`](#app_rc_move) is sent repeatedly while the user holds a direction, [`app_rc_stop`](#app_rc_stop) stops the
send loop in newer plugins, and [`app_rc_end`](#app_rc_end) leaves the mode.

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`app_rc_start`](#app_rc_start) | Puts the robot into manual mode. | ✅ Bundle |
| [`app_rc_move`](#app_rc_move) | Sets linear and angular velocity for a limited time; must be repeated to keep moving. | ✅ Bundle |
| [`app_rc_end`](#app_rc_end) | Ends manual mode. | ✅ Bundle |
| [`app_rc_stop`](#app_rc_stop) | Sent when the user releases the control. | ✅ Bundle |

<a id="app_rc_start"></a>
### `app_rc_start` — Enter remote-control mode

Puts the robot into manual mode.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`); forced local route (`callMethodForceWay` -> `callMethodFromLocal`) |

**Request**

`params`: none (`[]`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_rc_start", "params": []}
```

**Behaviour in the app**

Several bundles send this call through `callMethodForceWay` (local route only; see
[transports](../concepts/transports.md)). The app shows a safety note for 6 s after the call (a65 m14186).
The plugin only offers remote control when the firmware feature `isRemoteSupported` (fw feature code 125) is present.

**Related:** [`app_rc_move`](remote-control.md#app_rc_move), [`app_rc_end`](remote-control.md#app_rc_end)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`remoteStart`); call sites m14216, m14237, m14243, m14501, m14606; table key `AppRemoteControlStart` · anchor `"AppRemoteControlStart"`
- `a65@1.0.95` · wrapper m10115 (`remoteStart`); call sites m14186, m14207, m14213, m14471, m14552; table key `AppRemoteControlStart` · anchor `"AppRemoteControlStart"`
- `t4@1.0.32` · call sites m11390; table key `AppRemoteControlStart` · anchor `"AppRemoteControlStart"`

</details>

<a id="app_rc_move"></a>
### `app_rc_move` — Drive command

Sets linear and angular velocity for a limited time; must be repeated to keep moving.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`); forced local route (`callMethodForceWay` -> `callMethodFromLocal`) |

**Request**

`params` is **one-level** `[ {…} ]` with one object:

| Field | Type | Meaning | Evidence |
|---|---|---|---|
| `velocity` | number | linear speed in m/s, never negative: the key pad sends `0.2` for forward and `0` otherwise (a65 m14204); the joystick sends `0` when pulled backwards or sideways and otherwise a value between `0` and `0.29` (a65 m14207) | ✅ Bundle |
| `omega` | number | turn rate in rad/s, positive = turn left (key pad: `+1.05` left, `-1.05` right; joystick: `-dx / radius × π/3`, so a stick pushed left gives a positive value); range ±π/3 (≈ 1.05) | ✅ Bundle |
| `seqnum` | int | the app starts at 0 and increments by 1 for every command it sends | ✅ Bundle |
| `duration` | int (ms) | how long the robot executes the command: 1000 (key view) or 1500 (joystick view) | ✅ Bundle |

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (a65 m14186 `motionParam`)

```json
{"id": 105, "method": "app_rc_move", "params": [{"omega": 0, "velocity": 0.2, "seqnum": 1, "duration": 1000}]}
```

**Behaviour in the app**

The app re-sends the current `motionParam` periodically while the control is active and calls
[`app_rc_stop`](#app_rc_stop) when the loop ends (a65). Some bundles send the call through `callMethodForceWay`.

**Legacy documentation**

⚪ Legacy [rc.md](../../rc.md) shows a **nested** array `[[{…}]]` and the ranges `omega` ±3.1 and `velocity` ±0.3.
**Correction:** every bundle that sends the call builds a single-level array `[{…}]` (a01: `callMethod(…, [paras])`;
a65 `RobotApi.remoteMove`: `[paras]`), and the app never sends a negative velocity or exceeds 0.29, and |omega| stays within 1.05. Whether the
firmware accepts larger values is not determinable from the bundles.

**Related:** [`app_rc_start`](remote-control.md#app_rc_start), [`app_rc_end`](remote-control.md#app_rc_end), [`app_rc_stop`](remote-control.md#app_rc_stop)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`remoteMove`); call sites m14216, m14237, m14243, m14501, m14606; table key `AppRemoteControlMove` · anchor `"AppRemoteControlMove"`
- `a65@1.0.95` · wrapper m10115 (`remoteMove`); call sites m14186, m14207, m14213, m14471, m14552; table key `AppRemoteControlMove` · anchor `"AppRemoteControlMove"`
- `t4@1.0.32` · call sites m11390; table key `AppRemoteControlMove` · anchor `"AppRemoteControlMove"`

</details>

<a id="app_rc_end"></a>
### `app_rc_end` — Leave remote-control mode

Ends manual mode.

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
{"id": 1, "method": "app_rc_end", "params": []}
```

**Behaviour in the app**

Also used by the main page: if the robot state is `REMOTE` when the user presses a start/pause/charge control, the app
sends `app_rc_end` first (a65 m14147).

**Related:** [`app_rc_start`](remote-control.md#app_rc_start)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`remoteEnd`); call sites m14177, m14216, m14501, m14606, m14639; table key `AppRemoteControlEnd` · anchor `"AppRemoteControlEnd"`
- `a65@1.0.95` · wrapper m10115 (`remoteEnd`); call sites m14147, m14186, m14471, m14552, m14585; table key `AppRemoteControlEnd` · anchor `"AppRemoteControlEnd"`
- `t4@1.0.32` · call sites m11390; table key `AppRemoteControlEnd` · anchor `"AppRemoteControlEnd"`

</details>

<a id="app_rc_stop"></a>
### `app_rc_stop` — Stop the move loop

Sent when the user releases the control.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 39: a01 a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 c1 e2 m1s p5 s4 s5e s6 v1 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_rc_stop", "params": []}
```

**Behaviour in the app**

Evidence: `RobotApi.remoteStop` called from `_stopSendMove` (a65 m14186); see the availability row for the bundles that lack it.

**Related:** [`app_rc_move`](remote-control.md#app_rc_move)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`remoteStop`); call sites m14216, m14237, m14243, m14501, m14606 · anchor `"app_rc_stop"`
- `a65@1.0.95` · wrapper m10115 (`remoteStop`); call sites m14186, m14207, m14213, m14471, m14552 · anchor `"app_rc_stop"`
- `a11@1.0.34` · wrapper m10010 (`remoteStop`); call sites m11837, m11864, m11924, m11963 · anchor `"app_rc_stop"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
