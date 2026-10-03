# Carpet handling

[Home](../../README.md) / [Commands](index.md) / Carpet handling

Carpet detection and the behaviour on carpets.

Two independent features exist: the older **carpet pressurize** switch (`get_carpet_mode` / `set_carpet_mode`, a current
threshold set) and the newer **carpet clean mode** (`set_carpet_clean_mode`). Which one the app offers depends on
firmware and product (`isCarpetSupported`, `isNewCarpetPressurize`, product lists in the
[feature flags](../concepts/feature-flags.md) page).

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`get_carpet_mode`](#get_carpet_mode) | Returns the carpet-detection (pressurize) switch and thresholds. | ✅ Bundle |
| [`set_carpet_mode`](#set_carpet_mode) | Switches carpet detection and writes its current thresholds. | ✅ Bundle |
| [`get_carpet_clean_mode`](#get_carpet_clean_mode) | Returns the carpet behaviour mode. | ✅ Bundle |
| [`set_carpet_clean_mode`](#set_carpet_clean_mode) | Chooses what the robot does on carpets. | ✅ Bundle |
| [`app_get_carpet_deep_clean_status`](#app_get_carpet_deep_clean_status) | Reads the "carpet deep clean" switch. | ✅ Bundle |
| [`app_set_carpet_deep_clean_status`](#app_set_carpet_deep_clean_status) | Switches deep cleaning of carpets. | ✅ Bundle |
| [`app_set_priority_carpet_cleaning_status`](#app_set_priority_carpet_cleaning_status) | Switches "carpet first" ordering; the status field `switch_status` bit 3 reports it. | ✅ Bundle |

<a id="get_carpet_mode"></a>
### `get_carpet_mode` — Carpet pressurize (read)

Returns the carpet-detection (pressurize) switch and thresholds.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0].enable` (1 = on); the thresholds `current_integral`, `current_high`, `current_low`, `stall_time` are written by the app, not read back.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_carpet_mode", "params": []}
```

**Legacy documentation**

⚪ Legacy README lists `get_carpet_mode` / `set_carpet_mode` as "s5e only"; call sites exist in all 42 bundles.

**Related:** [`set_carpet_mode`](carpet.md#set_carpet_mode), [`get_carpet_clean_mode`](carpet.md#get_carpet_clean_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCarpetMode`); call sites m14168, m14282; table key `GetCarpetMode` · anchor `"GetCarpetMode"`
- `a65@1.0.95` · wrapper m10115 (`getCarpetMode`); call sites m14138, m14252; table key `GetCarpetMode` · anchor `"GetCarpetMode"`
- `t4@1.0.32` · wrapper m10010 (`getCarpetMode`); call sites m11453; table key `GetCarpetMode` · anchor `"GetCarpetMode"`

</details>

<a id="set_carpet_mode"></a>
### `set_carpet_mode` — Carpet pressurize (write)

Switches carpet detection and writes its current thresholds.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[{"enable": 0|1, "current_integral": <int>, "current_high": <int>, "current_low": <int>, "stall_time": <int>}]`.
The app's default values are `550`, `625`, `500` and `10` (✅ Bundle · a65 `carpetModeParamsEnable`/`Disable`); for some
product lines (`isCarpetPressurizeSwitchUseNewPara`) other threshold values are used (a65 m14252).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (a65 constants)

```json
{"id": 108, "method": "set_carpet_mode", "params": [{"enable": 1, "current_integral": 550, "current_high": 625, "current_low": 500, "stall_time": 10}]}
```

**Related:** [`get_carpet_mode`](carpet.md#get_carpet_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCarpetMode`); call sites m14168, m14282, m14498; table key `SetCarpetMode` · anchor `"SetCarpetMode"`
- `a65@1.0.95` · wrapper m10115 (`setCarpetMode`); call sites m14138, m14252, m14468; table key `SetCarpetMode` · anchor `"SetCarpetMode"`
- `t4@1.0.32` · wrapper m10010 (`setCarpetMode`); call sites m11453; table key `SetCarpetMode` · anchor `"SetCarpetMode"`

</details>

<a id="get_carpet_clean_mode"></a>
### `get_carpet_clean_mode` — Carpet clean mode (read)

Returns the carpet behaviour mode.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |
| Call-site gate | the call sits behind `isCarpetSupported` (tests found in the enclosing code of the call sites; [feature flags](../concepts/feature-flags.md)) |

**Request**

`params`: none (`[]`).

**Response**

`result[0].carpet_clean_mode` — one of the codes in the table below.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_carpet_clean_mode", "params": []}
```

**Related:** [`set_carpet_clean_mode`](carpet.md#set_carpet_clean_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCarpetCleanMode`); call sites m10007, m12533, m13031, m14282, m14396 · anchor `"get_carpet_clean_mode"`
- `a65@1.0.95` · wrapper m10115 (`getCarpetCleanMode`); call sites m10007, m12521, m13019, m14252, m14366 · anchor `"get_carpet_clean_mode"`
- `a08@1.0.47` · wrapper m10013 (`getCarpetCleanMode`); call sites m12473 · anchor `"get_carpet_clean_mode"`

</details>

<a id="set_carpet_clean_mode"></a>
### `set_carpet_clean_mode` — Carpet clean mode (write)

Chooses what the robot does on carpets.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"carpet_clean_mode": <code>}` with the codes of `CarPetCleanModeSettingMap`:

| Code | App name |
|---|---|
| 0 | `CarpetAvoidMode` |
| 1 | `CarpetSelfAdaptionMode` |
| 2 | `CarpetIgnoreMode` |
| 3 | `CarpetDynamicAdaptionMode` |

(✅ Bundle · a27 and newer `Protocol` module; the user-visible texts are in the carpet settings page.)

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_carpet_clean_mode", "params": {"carpet_clean_mode": 0}}
```

**Behaviour in the app**

The app refuses to change it while the robot is running and asks to finish the current task first.

**Related:** [`get_carpet_clean_mode`](carpet.md#get_carpet_clean_mode), [`app_set_carpet_deep_clean_status`](carpet.md#app_set_carpet_deep_clean_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCarpetCleanMode`); call sites m10007, m14282 · anchor `"set_carpet_clean_mode"`
- `a65@1.0.95` · wrapper m10115 (`setCarpetCleanMode`); call sites m10007, m14252 · anchor `"set_carpet_clean_mode"`
- `a08@1.0.47` · wrapper m10013 (`setCarpetCleanMode`); call sites m12473 · anchor `"set_carpet_clean_mode"`

</details>

<a id="app_get_carpet_deep_clean_status"></a>
### `app_get_carpet_deep_clean_status` — Carpet deep clean (read)

Reads the "carpet deep clean" switch.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

`result.status == 1` means on.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_get_carpet_deep_clean_status", "params": {}}
```

**Related:** [`app_set_carpet_deep_clean_status`](carpet.md#app_set_carpet_deep_clean_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCarpetDeepClean`); call sites m14282 · anchor `"app_get_carpet_deep_clean_status"`
- `a65@1.0.95` · wrapper m10115 (`getCarpetDeepClean`); call sites m14252 · anchor `"app_get_carpet_deep_clean_status"`
- `a29@1.0.75` · wrapper m10112 (`getCarpetDeepClean`); call sites m13997 · anchor `"app_get_carpet_deep_clean_status"`

</details>

<a id="app_set_carpet_deep_clean_status"></a>
### `app_set_carpet_deep_clean_status` — Carpet deep clean (write)

Switches deep cleaning of carpets.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"status": 0|1}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_set_carpet_deep_clean_status", "params": {"status": 1}}
```

**Related:** [`app_get_carpet_deep_clean_status`](carpet.md#app_get_carpet_deep_clean_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCarpetDeepClean`); call sites m14282 · anchor `"app_set_carpet_deep_clean_status"`
- `a65@1.0.95` · wrapper m10115 (`setCarpetDeepClean`); call sites m14252 · anchor `"app_set_carpet_deep_clean_status"`
- `a29@1.0.75` · wrapper m10112 (`setCarpetDeepClean`); call sites m13997 · anchor `"app_set_carpet_deep_clean_status"`

</details>

<a id="app_set_priority_carpet_cleaning_status"></a>
### `app_set_priority_carpet_cleaning_status` — Clean carpets first

Switches "carpet first" ordering; the status field `switch_status` bit 3 reports it.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"status": 0|1}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_set_priority_carpet_cleaning_status", "params": {"status": 1}}
```

**Related:** [`set_carpet_clean_mode`](carpet.md#set_carpet_clean_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCarpetFirstSwitch`); call sites m14282 · anchor `"app_set_priority_carpet_cleaning_status"`
- `a65@1.0.95` · wrapper m10115 (`setCarpetFirstSwitch`); call sites m14252 · anchor `"app_set_priority_carpet_cleaning_status"`
- `a51@1.0.83` · wrapper m10115 (`setCarpetFirstSwitch`); call sites m14231 · anchor `"app_set_priority_carpet_cleaning_status"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
