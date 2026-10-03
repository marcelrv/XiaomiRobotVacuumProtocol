# Diagnostic, test and internal commands

[Home](../../README.md) / [Commands](index.md) / Diagnostic, test and internal commands

Calls that are part of the plugin but are internal, experimental or test features. They are listed for completeness; do not assume that a robot answers them.

These calls belong to debug pages, experiments, promotional features and the transport itself. They are included because
they are method strings the plugins can send. Where a call is hidden behind a developer/debug page, the entry says so.

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`retry_request`](#retry_request) | Used by the plugin's retry protocol to ask whether a deferred call has completed. | ✅ Bundle (wrapper only) |
| [`resolve_error`](#resolve_error) | Tells the robot that the user has resolved an error condition (mostly dock errors). | ✅ Bundle |
| [`set_ces_action`](#set_ces_action) | Sends a demo `type` / `action` pair (name refers to CES 2022). | ✅ Bundle |
| [`app_keep_easter_egg`](#app_keep_easter_egg) | Periodic keep-alive of the easter-egg mode. | ✅ Bundle |
| [`app_start_easter_egg`](#app_start_easter_egg) | Starts the "egg attack" feature (state 30, text "scanning"). | ✅ Bundle |
| [`app_set_dynamic_config`](#app_set_dynamic_config) | Debug page: points the robot to a configuration file for testing. | ✅ Bundle |
| [`test_do_speak`](#test_do_speak) | Triggers a speech test (a72, a73 only). | ✅ Bundle |
| [`test_get_enable_wakeup`](#test_get_enable_wakeup) | Reads the wake-word switch. | ✅ Bundle |
| [`test_set_enable_wakeup`](#test_set_enable_wakeup) | Switches the wake-word. | ✅ Bundle |
| [`test_get_move_in_place`](#test_get_move_in_place) | Reads the switch. | ✅ Bundle |
| [`test_set_move_in_place`](#test_set_move_in_place) | Switches turning in place on voice commands. | ✅ Bundle |
| [`test_get_voice_keep_seconds`](#test_get_voice_keep_seconds) | Reads the duration the robot stays awake after the wake word. | ✅ Bundle |
| [`test_set_voice_keep_seconds`](#test_set_voice_keep_seconds) | Sets the duration. | ✅ Bundle |

<a id="retry_request"></a>
### `retry_request` — Poll a deferred request (transport mechanism)

Used by the plugin's retry protocol to ask whether a deferred call has completed.

| | |
|---|---|
| Evidence | ✅ Bundle (wrapper only) — sent by the retry loop inside `asyncCallMethod` of the generation-B bundles; the extraction counts it as wrapper-only because no UI code calls it |
| Other bundles | wrapper only: 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"retry_id": <id>, "method": "<original method>", "retry_count": <int>}` (✅ Bundle · a65 m10115 `retry`).

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "retry_request", "params": {"retry_id": 1, "method": "set_timer", "retry_count": 1}}
```

**Behaviour in the app**

See [transports](../concepts/transports.md#retry-protocol). Sent by the wrapper itself every 2 s, at most 8 times.

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`retryRequest`) · anchor `"retry_request"`
- `a65@1.0.95` · wrapper m10115 (`retryRequest`) · anchor `"retry_request"`
- `a14@1.0.53` · wrapper m10142 (`retryRequest`) · anchor `"retry_request"`

</details>

<a id="resolve_error"></a>
### `resolve_error` — Acknowledge an error

Tells the robot that the user has resolved an error condition (mostly dock errors).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"error_code": <int>}` — the dock error status, or the code shown in the error dialog.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "resolve_error", "params": {"error_code": 1}}
```

**Behaviour in the app**

On the `Garnet` product line a resume-mopping alert follows.

**Related:** [`app_get_init_status`](status.md#app_get_init_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`resolveError`); call sites m13031, m13958 · anchor `"resolve_error"`
- `a65@1.0.95` · wrapper m10115 (`resolveError`); call sites m13019, m13946 · anchor `"resolve_error"`
- `a62@1.0.69` · wrapper m10109 (`resolveError`); call sites m12587, m13514 · anchor `"resolve_error"`

</details>

<a id="set_ces_action"></a>
### `set_ces_action` — Trade-show demo action

Sends a demo `type` / `action` pair (name refers to CES 2022).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"type": <int>, "action": <int>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_ces_action", "params": {"type": 1, "action": 0}}
```

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCes2022Action`); call sites m14603 · anchor `"set_ces_action"`
- `a65@1.0.95` · wrapper m10115 (`setCes2022Action`); call sites m14549 · anchor `"set_ces_action"`
- `a51@1.0.83` · wrapper m10115 (`setCes2022Action`); call sites m14528 · anchor `"set_ces_action"`

</details>

<a id="app_keep_easter_egg"></a>
### `app_keep_easter_egg` — "Cupid mode" keep-alive

Periodic keep-alive of the easter-egg mode.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_keep_easter_egg", "params": {}}
```

**Related:** [`app_start_easter_egg`](diagnostic.md#app_start_easter_egg)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`eggKeep`); call sites m14489 · anchor `"app_keep_easter_egg"`
- `a65@1.0.95` · wrapper m10115 (`eggKeep`); call sites m14459 · anchor `"app_keep_easter_egg"`
- `a62@1.0.69` · wrapper m10109 (`eggKeep`); call sites m14018 · anchor `"app_keep_easter_egg"`

</details>

<a id="app_start_easter_egg"></a>
### `app_start_easter_egg` — "Cupid mode" start (easter egg)

Starts the "egg attack" feature (state 30, text "scanning").

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_start_easter_egg", "params": {}}
```

**Behaviour in the app**

The a65 strings call the feature "Cupid Mode"; while it runs the app sends [`app_keep_easter_egg`](#app_keep_easter_egg) periodically.

**Related:** [`app_keep_easter_egg`](diagnostic.md#app_keep_easter_egg)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`startEggAttack`); call sites m14489 · anchor `"app_start_easter_egg"`
- `a65@1.0.95` · wrapper m10115 (`startEggAttack`); call sites m14459 · anchor `"app_start_easter_egg"`
- `a62@1.0.69` · wrapper m10109 (`startEggAttack`); call sites m14018 · anchor `"app_start_easter_egg"`

</details>

<a id="app_set_dynamic_config"></a>
### `app_set_dynamic_config` — Download a test configuration

Debug page: points the robot to a configuration file for testing.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"version": <v>, "url": "<url>", "signature_url": "<url>"}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_set_dynamic_config", "params": {"version": 1, "url": "https://example.invalid/file.pkg", "signature_url": "https://example.invalid/file.pkg"}}
```

**Behaviour in the app**

Only reachable from a debug page.

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setConfigTestUrl`); call sites m14564 · anchor `"app_set_dynamic_config"`
- `a65@1.0.95` · wrapper m10115 (`setConfigTestUrl`); call sites m14510 · anchor `"app_set_dynamic_config"`
- `a34@1.0.70` · wrapper m10109 (`setConfigTestUrl`); call sites m14087 · anchor `"app_set_dynamic_config"`

</details>

<a id="test_do_speak"></a>
### `test_do_speak` — Voice-control test: speak

Triggers a speech test (a72, a73 only).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 2: a72 a73 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "test_do_speak", "params": {}}
```

**Related:** [`test_set_enable_wakeup`](diagnostic.md#test_set_enable_wakeup)

<details><summary>Sources</summary>

- `a73@1.0.92` · wrapper m10115 (`setVCTestDoSpeak`); call sites m14414 · anchor `"test_do_speak"`
- `a72@1.0.92` · wrapper m10115 (`setVCTestDoSpeak`); call sites m14414 · anchor `"test_do_speak"`

</details>

<a id="test_get_enable_wakeup"></a>
### `test_get_enable_wakeup` — Voice-control test: wake-up (read)

Reads the wake-word switch.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 2: a72 a73 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.enable_wakeup`.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "test_get_enable_wakeup", "params": []}
```

**Related:** [`test_set_enable_wakeup`](diagnostic.md#test_set_enable_wakeup)

<details><summary>Sources</summary>

- `a73@1.0.92` · wrapper m10115 (`getVCTestEnableWakeup`); call sites m14414 · anchor `"test_get_enable_wakeup"`
- `a72@1.0.92` · wrapper m10115 (`getVCTestEnableWakeup`); call sites m14414 · anchor `"test_get_enable_wakeup"`

</details>

<a id="test_set_enable_wakeup"></a>
### `test_set_enable_wakeup` — Voice-control test: wake-up (write)

Switches the wake-word.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 2: a72 a73 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"enable_wakeup": 0|1}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "test_set_enable_wakeup", "params": {"enable_wakeup": 1}}
```

**Behaviour in the app**

Debug entry gated by fw feature code 130 (`isSupportVoiceCtrolDebug`).

**Related:** [`test_get_enable_wakeup`](diagnostic.md#test_get_enable_wakeup)

<details><summary>Sources</summary>

- `a73@1.0.92` · wrapper m10115 (`setVCTestEnableWakeup`); call sites m14414 · anchor `"test_set_enable_wakeup"`
- `a72@1.0.92` · wrapper m10115 (`setVCTestEnableWakeup`); call sites m14414 · anchor `"test_set_enable_wakeup"`

</details>

<a id="test_get_move_in_place"></a>
### `test_get_move_in_place` — Voice-control test: move in place (read)

Reads the switch.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 2: a72 a73 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.move_in_place`.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "test_get_move_in_place", "params": []}
```

**Related:** [`test_set_move_in_place`](diagnostic.md#test_set_move_in_place)

<details><summary>Sources</summary>

- `a73@1.0.92` · wrapper m10115 (`getVCTestMoveInPlace`); call sites m14414 · anchor `"test_get_move_in_place"`
- `a72@1.0.92` · wrapper m10115 (`getVCTestMoveInPlace`); call sites m14414 · anchor `"test_get_move_in_place"`

</details>

<a id="test_set_move_in_place"></a>
### `test_set_move_in_place` — Voice-control test: move in place (write)

Switches turning in place on voice commands.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 2: a72 a73 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"move_in_place": 0|1}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "test_set_move_in_place", "params": {"move_in_place": 1}}
```

**Related:** [`test_get_move_in_place`](diagnostic.md#test_get_move_in_place)

<details><summary>Sources</summary>

- `a73@1.0.92` · wrapper m10115 (`setVCTestMoveInPlace`); call sites m14414 · anchor `"test_set_move_in_place"`
- `a72@1.0.92` · wrapper m10115 (`setVCTestMoveInPlace`); call sites m14414 · anchor `"test_set_move_in_place"`

</details>

<a id="test_get_voice_keep_seconds"></a>
### `test_get_voice_keep_seconds` — Voice-control test: keep-awake time (read)

Reads the duration the robot stays awake after the wake word.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 2: a72 a73 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.keep_seconds`.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "test_get_voice_keep_seconds", "params": []}
```

**Related:** [`test_set_voice_keep_seconds`](diagnostic.md#test_set_voice_keep_seconds)

<details><summary>Sources</summary>

- `a73@1.0.92` · wrapper m10115 (`getVCTestVoiceKeepSeconds`); call sites m14414 · anchor `"test_get_voice_keep_seconds"`
- `a72@1.0.92` · wrapper m10115 (`getVCTestVoiceKeepSeconds`); call sites m14414 · anchor `"test_get_voice_keep_seconds"`

</details>

<a id="test_set_voice_keep_seconds"></a>
### `test_set_voice_keep_seconds` — Voice-control test: keep-awake time (write)

Sets the duration.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 2: a72 a73 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"keep_seconds": <int>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "test_set_voice_keep_seconds", "params": {"keep_seconds": 60}}
```

**Related:** [`test_get_voice_keep_seconds`](diagnostic.md#test_get_voice_keep_seconds)

<details><summary>Sources</summary>

- `a73@1.0.92` · wrapper m10115 (`setVCTestVoiceKeepSeconds`); call sites m14414 · anchor `"test_set_voice_keep_seconds"`
- `a72@1.0.92` · wrapper m10115 (`setVCTestVoiceKeepSeconds`); call sites m14414 · anchor `"test_set_voice_keep_seconds"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
