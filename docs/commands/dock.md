# Dock (auto-empty, mop washing and drying)

[Home](../../README.md) / [Commands](index.md) / Dock (auto-empty, mop washing and drying)

Commands for multifunction docks.

These commands exist in plugins for robots with a multifunction dock: auto-empty ("dust collection"), mop washing
("wash towel", `app_start_wash`) and mop drying. The plugin identifies dock types through the status field `dock_type`
(app names O1, O2, O3, O3+, O4, O5, "Pearl", "OCD"; see [dock reference](../reference/dock.md)). Product gating is on
the [device pages](../devices/index.md). Commands whose names contain `amethyst` belong to the self-cleaning/water-change
dock family; the code name is the plugin's, the marketing meaning is not stated in the bundles.

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`app_start_wash`](#app_start_wash) | Starts the mop-washing routine at the dock. | ✅ Bundle |
| [`app_stop_wash`](#app_stop_wash) | Stops a running wash. | ✅ Bundle |
| [`app_start_collect_dust`](#app_start_collect_dust) | Starts auto-empty. | ✅ Bundle |
| [`app_stop_collect_dust`](#app_stop_collect_dust) | Stops auto-empty. | ✅ Bundle |
| [`get_dust_collection_mode`](#get_dust_collection_mode) | Returns the auto-empty mode. | ✅ Bundle |
| [`set_dust_collection_mode`](#set_dust_collection_mode) | Sets the auto-empty mode. | ✅ Bundle |
| [`get_dust_collection_switch_status`](#get_dust_collection_switch_status) | Returns whether automatic emptying is on. | ✅ Bundle |
| [`set_dust_collection_switch_status`](#set_dust_collection_switch_status) | Turns automatic emptying on or off. | ✅ Bundle |
| [`get_wash_towel_mode`](#get_wash_towel_mode) | Returns the dock mop-wash mode. | ✅ Bundle |
| [`set_wash_towel_mode`](#set_wash_towel_mode) | Sets the mop-wash mode. | ✅ Bundle |
| [`get_wash_towel_params`](#get_wash_towel_params) | Older variant of the mop-wash settings page (`getWashTowel`). | ✅ Bundle |
| [`set_wash_towel_params`](#set_wash_towel_params) | Sets the mode, status or interval of the older wash page. | ✅ Bundle |
| [`get_smart_wash_params`](#get_smart_wash_params) | Returns the smart mid-clean wash setting. | ✅ Bundle |
| [`set_smart_wash_params`](#set_smart_wash_params) | Turns "smart" mid-clean mop washing on/off and sets the interval. | ✅ Bundle |
| [`app_get_dryer_setting`](#app_get_dryer_setting) | Returns the dryer configuration. | ✅ Bundle |
| [`app_set_dryer_setting`](#app_set_dryer_setting) | Sets the drying time and status. | ✅ Bundle |
| [`app_set_dryer_status`](#app_set_dryer_status) | Starts or stops mop drying immediately. | ✅ Bundle |
| [`set_airdry_hours`](#set_airdry_hours) | Wrapper `setAirdryDuration`; no call site found. | ✅ Bundle (wrapper only) |
| [`stop_airdry_mop`](#stop_airdry_mop) | Wrapped as `stopAirdryMop` in 10 bundles (a08 a09 a10 a14 a15 a19 a23 s4 s5e s6); newer bundles name the same  | ✅ Bundle (wrapper only) |
| [`app_amethyst_self_check`](#app_amethyst_self_check) | Runs the dock self-diagnosis. | ✅ Bundle |
| [`app_amethyst_drain_all_water`](#app_amethyst_drain_all_water) | Drains the dock water tanks. | ✅ Bundle |
| [`app_empty_inbuilt_water_tank`](#app_empty_inbuilt_water_tank) | Drains the robot-side tank at the dock (wrapper `appAmethystDrainLeftWater`). | ✅ Bundle |
| [`app_get_amethyst_status`](#app_get_amethyst_status) | Reads the "smart change water" switch. | ✅ Bundle |
| [`app_set_amethyst_status`](#app_set_amethyst_status) | Sets the switch. | ✅ Bundle |
| [`update_dock`](#update_dock) | Orders a dock firmware update. | ✅ Bundle |
| [`get_wash_debug_params`](#get_wash_debug_params) | Wrapper only; no call site. | ✅ Bundle (wrapper only) |
| [`set_wash_debug_params`](#set_wash_debug_params) | Wrapper only; four separate wrappers set one key each. | ✅ Bundle (wrapper only) |
| [`get_auto_delivery_cleaning_fluid`](#get_auto_delivery_cleaning_fluid) | Reads the switch. | ✅ Bundle |
| [`set_auto_delivery_cleaning_fluid`](#set_auto_delivery_cleaning_fluid) | Turns automatic dosing on or off. | ✅ Bundle |
| [`clean_roller`](#clean_roller) | Starts or stops the mop-roller cleaning (the older name of the wash action). | ✅ Bundle |

<a id="app_start_wash"></a>
### `app_start_wash` — Wash the mop

Starts the mop-washing routine at the dock.

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
{"id": 1, "method": "app_start_wash", "params": {}}
```

**Behaviour in the app**

After the call the app expects state 23/25 (`WASHING_DUSTER`) if the dock is ready (`wash_ready`), otherwise the robot
first goes to the dock (26, "going to wash the mop"). For the `TopazS` product the app first shows an explanation alert
when a clean is in progress (a65 m12959).

**Related:** [`app_stop_wash`](dock.md#app_stop_wash), [`start_wash_then_charge`](cleaning-control.md#start_wash_then_charge), [`set_wash_towel_mode`](dock.md#set_wash_towel_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`startWash`); call sites m12971 · anchor `"app_start_wash"`
- `a65@1.0.95` · wrapper m10115 (`startWash`); call sites m12959 · anchor `"app_start_wash"`
- `a62@1.0.69` · wrapper m10109 (`startWash`); call sites m12515 · anchor `"app_start_wash"`

</details>

<a id="app_stop_wash"></a>
### `app_stop_wash` — Stop mop washing

Stops a running wash.

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
{"id": 1, "method": "app_stop_wash", "params": {}}
```

**Related:** [`app_start_wash`](dock.md#app_start_wash)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`stopWash`); call sites m12971 · anchor `"app_stop_wash"`
- `a65@1.0.95` · wrapper m10115 (`stopWash`); call sites m12959 · anchor `"app_stop_wash"`
- `a62@1.0.69` · wrapper m10109 (`stopWash`); call sites m12515 · anchor `"app_stop_wash"`

</details>

<a id="app_start_collect_dust"></a>
### `app_start_collect_dust` — Empty the dust bin into the dock

Starts auto-empty.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_start_collect_dust", "params": []}
```

**Behaviour in the app**

Offered in the dock menu; expected state while running: 22 (`COLLECTING_DUST`).

**Related:** [`app_stop_collect_dust`](dock.md#app_stop_collect_dust), [`set_dust_collection_mode`](dock.md#set_dust_collection_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`startCollectDust`); call sites m12971 · anchor `"app_start_collect_dust"`
- `a65@1.0.95` · wrapper m10115 (`startCollectDust`); call sites m12959 · anchor `"app_start_collect_dust"`
- `a08@1.0.47` · wrapper m10013 (`startCollectDust`); call sites m11510 · anchor `"app_start_collect_dust"`

</details>

<a id="app_stop_collect_dust"></a>
### `app_stop_collect_dust` — Stop emptying

Stops auto-empty.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_stop_collect_dust", "params": []}
```

**Related:** [`app_start_collect_dust`](dock.md#app_start_collect_dust)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`stopCollectDust`); call sites m12971 · anchor `"app_stop_collect_dust"`
- `a65@1.0.95` · wrapper m10115 (`stopCollectDust`); call sites m12959 · anchor `"app_stop_collect_dust"`
- `a08@1.0.47` · wrapper m10013 (`stopCollectDust`); call sites m11510 · anchor `"app_stop_collect_dust"`

</details>

<a id="get_dust_collection_mode"></a>
### `get_dust_collection_mode` — Auto-empty mode (read)

Returns the auto-empty mode.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.mode` (object, not array): 0 Smart, 1 Quick, 2 Daily, 3 Strong, 4 Max ([enums](../reference/other-enums.md#dustcollectionmode)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_dust_collection_mode", "params": []}
```

**Behaviour in the app**

Gated by new-feature bit `isDustCollectionSettingSupported` (low word bit 25).

**Related:** [`set_dust_collection_mode`](dock.md#set_dust_collection_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getDustCollectionMode`); call sites m14423, m14567 · anchor `"get_dust_collection_mode"`
- `a65@1.0.95` · wrapper m10115 (`getDustCollectionMode`); call sites m14393, m14513 · anchor `"get_dust_collection_mode"`
- `a14@1.0.53` · wrapper m10142 (`getDustCollectionMode`); call sites m13328 · anchor `"get_dust_collection_mode"`

</details>

<a id="set_dust_collection_mode"></a>
### `set_dust_collection_mode` — Auto-empty mode (write)

Sets the auto-empty mode.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"mode": <0–4>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_dust_collection_mode", "params": {"mode": 1}}
```

**Related:** [`get_dust_collection_mode`](dock.md#get_dust_collection_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setDustCollectionMode`); call sites m14423 · anchor `"set_dust_collection_mode"`
- `a65@1.0.95` · wrapper m10115 (`setDustCollectionMode`); call sites m14393 · anchor `"set_dust_collection_mode"`
- `a14@1.0.53` · wrapper m10142 (`setDustCollectionMode`); call sites m13328 · anchor `"set_dust_collection_mode"`

</details>

<a id="get_dust_collection_switch_status"></a>
### `get_dust_collection_switch_status` — Auto-empty switch (read)

Returns whether automatic emptying is on.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result` object with `status`; the status field `auto_dust_collection == 0` also means "off".

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_dust_collection_switch_status", "params": []}
```

**Related:** [`set_dust_collection_switch_status`](dock.md#set_dust_collection_switch_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getDustCollectionStatus`); call sites m14423, m14567 · anchor `"get_dust_collection_switch_status"`
- `a65@1.0.95` · wrapper m10115 (`getDustCollectionStatus`); call sites m14393, m14513 · anchor `"get_dust_collection_switch_status"`
- `a14@1.0.53` · wrapper m10142 (`getDustCollectionStatus`); call sites m13328 · anchor `"get_dust_collection_switch_status"`

</details>

<a id="set_dust_collection_switch_status"></a>
### `set_dust_collection_switch_status` — Auto-empty switch (write)

Turns automatic emptying on or off.

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
{"id": 1, "method": "set_dust_collection_switch_status", "params": {"status": 1}}
```

**Related:** [`get_dust_collection_switch_status`](dock.md#get_dust_collection_switch_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setDustCollectionStatus`); call sites m14423, m14567 · anchor `"set_dust_collection_switch_status"`
- `a65@1.0.95` · wrapper m10115 (`setDustCollectionStatus`); call sites m14393, m14513 · anchor `"set_dust_collection_switch_status"`
- `a14@1.0.53` · wrapper m10142 (`setDustCollectionStatus`); call sites m13328 · anchor `"set_dust_collection_switch_status"`

</details>

<a id="get_wash_towel_mode"></a>
### `get_wash_towel_mode` — Mop wash mode (read)

Returns the dock mop-wash mode.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

`result.wash_mode`: 0 Quick, 1 Daily, 2 Deep, 8 SuperDeep ([enums](../reference/other-enums.md#washtowelmode)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_wash_towel_mode", "params": {}}
```

**Related:** [`set_wash_towel_mode`](dock.md#set_wash_towel_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getWashTowelMode`); call sites m14426, m14429, m14567 · anchor `"get_wash_towel_mode"`
- `a65@1.0.95` · wrapper m10115 (`getWashTowelMode`); call sites m14396, m14399, m14513 · anchor `"get_wash_towel_mode"`
- `a62@1.0.69` · wrapper m10109 (`getWashTowelMode`); call sites m13958 · anchor `"get_wash_towel_mode"`

</details>

<a id="set_wash_towel_mode"></a>
### `set_wash_towel_mode` — Mop wash mode (write)

Sets the mop-wash mode.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"wash_mode": <0|1|2|8>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_wash_towel_mode", "params": {"wash_mode": 0}}
```

**Related:** [`get_wash_towel_mode`](dock.md#get_wash_towel_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setWashTowelMode`); call sites m14426, m14429 · anchor `"set_wash_towel_mode"`
- `a65@1.0.95` · wrapper m10115 (`setWashTowelMode`); call sites m14396, m14399 · anchor `"set_wash_towel_mode"`
- `a62@1.0.69` · wrapper m10109 (`setWashTowelMode`); call sites m13958 · anchor `"set_wash_towel_mode"`

</details>

<a id="get_wash_towel_params"></a>
### `get_wash_towel_params` — Mop wash parameters (older bundles)

Older variant of the mop-wash settings page (`getWashTowel`).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 1: a62 model(s) |
| Other bundles | wrapper only: 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.mode`.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_wash_towel_params", "params": []}
```

**Related:** [`set_wash_towel_params`](dock.md#set_wash_towel_params)

<details><summary>Sources</summary>

- `a62@1.0.69` · wrapper m10109 (`getWashTowel`); call sites m13955 · anchor `"get_wash_towel_params"`

</details>

<a id="set_wash_towel_params"></a>
### `set_wash_towel_params` — Mop wash parameters (older bundles, write)

Sets the mode, status or interval of the older wash page.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 1: a62 model(s) |
| Other bundles | wrapper only: 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"mode": <int>}`, `{"status": <int>}` or `{"interval": <int>}` (separate wrapper calls).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_wash_towel_params", "params": {"mode": 1}}
```

**Related:** [`get_wash_towel_params`](dock.md#get_wash_towel_params)

<details><summary>Sources</summary>

- `a62@1.0.69` · wrapper m10109 (`setWashTowelInterval, setWashTowelParams, setWashTowelStatus`); call sites m13955 · anchor `"set_wash_towel_params"`

</details>

<a id="get_smart_wash_params"></a>
### `get_smart_wash_params` — Back-wash settings (read)

Returns the smart mid-clean wash setting.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

`{"smart_wash": 0|1, "wash_interval": <seconds>}` (the page shows the interval in minutes = seconds ÷ 60).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_smart_wash_params", "params": {}}
```

**Related:** [`set_smart_wash_params`](dock.md#set_smart_wash_params)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getSmartWashParams`); call sites m14426, m14429, m14567 · anchor `"get_smart_wash_params"`
- `a65@1.0.95` · wrapper m10115 (`getSmartWashParams`); call sites m14396, m14399, m14513 · anchor `"get_smart_wash_params"`
- `a62@1.0.69` · wrapper m10109 (`getSmartWashParams`); call sites m13958 · anchor `"get_smart_wash_params"`

</details>

<a id="set_smart_wash_params"></a>
### `set_smart_wash_params` — Back-wash settings (write)

Turns "smart" mid-clean mop washing on/off and sets the interval.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"smart_wash": 0|1, "wash_interval": <seconds>}`; the app sends `minutes × 60` (a65 m14396). Mode names: `BackWashMode` Smart 0, Custom 1, Level 2.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_smart_wash_params", "params": {"smart_wash": 1, "wash_interval": 3600}}
```

**Related:** [`get_smart_wash_params`](dock.md#get_smart_wash_params)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setSmartWashParams`); call sites m14426, m14429 · anchor `"set_smart_wash_params"`
- `a65@1.0.95` · wrapper m10115 (`setSmartWashParams`); call sites m14396, m14399 · anchor `"set_smart_wash_params"`
- `a62@1.0.69` · wrapper m10109 (`setSmartWashParams`); call sites m13958 · anchor `"set_smart_wash_params"`

</details>

<a id="app_get_dryer_setting"></a>
### `app_get_dryer_setting` — Mop drying settings (read)

Returns the dryer configuration.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.status` (truthy = drying switch on) and `result.on.dry_time` (drying time in seconds; the UI offers 7200, 10800 and 14400) — ✅ Bundle · a65 m14513 `getDryerSetting`.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_get_dryer_setting", "params": []}
```

**Related:** [`app_set_dryer_setting`](dock.md#app_set_dryer_setting)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getDryerSetting`); call sites m14429, m14567, m14576 · anchor `"app_get_dryer_setting"`
- `a65@1.0.95` · wrapper m10115 (`getDryerSetting`); call sites m14399, m14513, m14522 · anchor `"app_get_dryer_setting"`
- `a62@1.0.69` · wrapper m10109 (`getDryerSetting`); call sites m14045 · anchor `"app_get_dryer_setting"`

</details>

<a id="app_set_dryer_setting"></a>
### `app_set_dryer_setting` — Mop drying settings (write)

Sets the drying time and status.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"on": {"dry_time": <seconds>}, "status": <0|1>}`; the UI offers 7200, 10800 and 14400 (`DryerTimeMap`, a65 m14513).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_set_dryer_setting", "params": {"on": {"dry_time": 7200}, "status": 1}}
```

**Behaviour in the app**

Needs new-feature bit `isSupportedDrying` (high word bit 15).

**Related:** [`app_set_dryer_status`](dock.md#app_set_dryer_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setDryerSetting`); call sites m14429, m14567, m14576, m14579 · anchor `"app_set_dryer_setting"`
- `a65@1.0.95` · wrapper m10115 (`setDryerSetting`); call sites m14399, m14513, m14522, m14525 · anchor `"app_set_dryer_setting"`
- `a62@1.0.69` · wrapper m10109 (`setDryerSetting`); call sites m14045 · anchor `"app_set_dryer_setting"`

</details>

<a id="app_set_dryer_status"></a>
### `app_set_dryer_status` — Start / stop drying

Starts or stops mop drying immediately.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"status": 0|1}`; the dock button sends `0` when `RSM.isDrying`, otherwise `1`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_set_dryer_status", "params": {"status": 1}}
```

**Related:** [`app_set_dryer_setting`](dock.md#app_set_dryer_setting), [`stop_airdry_mop`](dock.md#stop_airdry_mop)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setDryerStatus`); call sites m12971, m14576 · anchor `"app_set_dryer_status"`
- `a65@1.0.95` · wrapper m10115 (`setDryerStatus`); call sites m12959, m14522 · anchor `"app_set_dryer_status"`
- `a62@1.0.69` · wrapper m10109 (`setDryerStatus`); call sites m14045 · anchor `"app_set_dryer_status"`

</details>

<a id="set_airdry_hours"></a>
### `set_airdry_hours` — Air-dry hours (wrapped)

Wrapper `setAirdryDuration`; no call site found.

| | |
|---|---|
| Evidence | ✅ Bundle (wrapper only) — no call site found in the bundles |
| Other bundles | wrapper only: 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"hours": <minutes>}` (the wrapper names the value `minutes`).

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_airdry_hours", "params": {"hours": 120}}
```

**Related:** [`set_fan_motor_work_timeout`](cleaning-modes.md#set_fan_motor_work_timeout)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setAirdryDuration`) · anchor `"set_airdry_hours"`
- `a65@1.0.95` · wrapper m10115 (`setAirdryDuration`) · anchor `"set_airdry_hours"`
- `a08@1.0.47` · wrapper m10013 (`setAirdryDuration`) · anchor `"set_airdry_hours"`

</details>

<a id="stop_airdry_mop"></a>
### `stop_airdry_mop` — Stop air-dry (wrapped)

Wrapped as `stopAirdryMop` in 10 bundles (a08 a09 a10 a14 a15 a19 a23 s4 s5e s6); newer bundles name the same wrapper after `stop_fan_motor_work`; no call site for this spelling.

| | |
|---|---|
| Evidence | ✅ Bundle (wrapper only) — no call site found in the bundles |
| Other bundles | wrapper only: 10: a08 a09 a10 a14 a15 a19 a23 s4 s5e s6 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "stop_airdry_mop", "params": []}
```

**Related:** [`stop_fan_motor_work`](cleaning-modes.md#stop_fan_motor_work)

<details><summary>Sources</summary>

- `a23@1.0.53` · wrapper m10142 (`stopAirdryMop`) · anchor `"stop_airdry_mop"`
- `a15@1.0.53` · wrapper m10142 (`stopAirdryMop`) · anchor `"stop_airdry_mop"`
- `a08@1.0.47` · wrapper m10013 (`stopAirdryMop`) · anchor `"stop_airdry_mop"`

</details>

<a id="app_amethyst_self_check"></a>
### `app_amethyst_self_check` — Dock self-check

Runs the dock self-diagnosis.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_amethyst_self_check", "params": {}}
```

**Related:** [`app_amethyst_drain_all_water`](dock.md#app_amethyst_drain_all_water)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`appAmethystSelfCheck`); call sites m14588, m14600 · anchor `"app_amethyst_self_check"`
- `a65@1.0.95` · wrapper m10115 (`appAmethystSelfCheck`); call sites m14534, m14546 · anchor `"app_amethyst_self_check"`
- `a34@1.0.70` · wrapper m10109 (`appAmethystSelfCheck`); call sites m14111 · anchor `"app_amethyst_self_check"`

</details>

<a id="app_amethyst_drain_all_water"></a>
### `app_amethyst_drain_all_water` — Drain all water

Drains the dock water tanks.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_amethyst_drain_all_water", "params": {}}
```

**Related:** [`app_empty_inbuilt_water_tank`](dock.md#app_empty_inbuilt_water_tank)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`appAmethystDrainWater`); call sites m14600 · anchor `"app_amethyst_drain_all_water"`
- `a65@1.0.95` · wrapper m10115 (`appAmethystDrainWater`); call sites m14546 · anchor `"app_amethyst_drain_all_water"`
- `a51@1.0.83` · wrapper m10115 (`appAmethystDrainWater`); call sites m14525 · anchor `"app_amethyst_drain_all_water"`

</details>

<a id="app_empty_inbuilt_water_tank"></a>
### `app_empty_inbuilt_water_tank` — Empty the built-in water tank

Drains the robot-side tank at the dock (wrapper `appAmethystDrainLeftWater`).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_empty_inbuilt_water_tank", "params": {}}
```

**Behaviour in the app**

Only offered while the robot is charging on the dock.

**Related:** [`app_amethyst_drain_all_water`](dock.md#app_amethyst_drain_all_water)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`appAmethystDrainLeftWater`); call sites m14633 · anchor `"app_empty_inbuilt_water_tank"`
- `a65@1.0.95` · wrapper m10115 (`appAmethystDrainLeftWater`); call sites m14579 · anchor `"app_empty_inbuilt_water_tank"`
- `a51@1.0.83` · wrapper m10115 (`appAmethystDrainLeftWater`); call sites m14558 · anchor `"app_empty_inbuilt_water_tank"`

</details>

<a id="app_get_amethyst_status"></a>
### `app_get_amethyst_status` — Smart water change (read)

Reads the "smart change water" switch.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 1: a62 model(s) |
| Other bundles | wrapper only: 19: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a74 a75 a76 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.status` (0/1).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_get_amethyst_status", "params": []}
```

**Related:** [`app_set_amethyst_status`](dock.md#app_set_amethyst_status)

<details><summary>Sources</summary>

- `a62@1.0.69` · wrapper m10109 (`getAmethystStatus`); call sites m14045 · anchor `"app_get_amethyst_status"`

</details>

<a id="app_set_amethyst_status"></a>
### `app_set_amethyst_status` — Smart water change (write)

Sets the switch.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 1: a62 model(s) |
| Other bundles | wrapper only: 19: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a74 a75 a76 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"status": 0|1}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_set_amethyst_status", "params": {"status": 1}}
```

**Behaviour in the app**

New-feature bit `isSupportedSmartChangeWater` (high word bit 16).

**Related:** [`app_get_amethyst_status`](dock.md#app_get_amethyst_status)

<details><summary>Sources</summary>

- `a62@1.0.69` · wrapper m10109 (`setAmethystStatus`); call sites m14045 · anchor `"app_set_amethyst_status"`

</details>

<a id="update_dock"></a>
### `update_dock` — Update dock firmware

Orders a dock firmware update.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "update_dock", "params": {}}
```

**Behaviour in the app**

Debug/settings page; the toasts of the debug variant are Chinese.

**Related:** [`get_dock_info`](status.md#get_dock_info)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`updateDock`); call sites m14405 · anchor `"update_dock"`
- `a65@1.0.95` · wrapper m10115 (`updateDock`); call sites m14375 · anchor `"update_dock"`
- `a29@1.0.75` · wrapper m10112 (`updateDock`); call sites m14105 · anchor `"update_dock"`

</details>

<a id="get_wash_debug_params"></a>
### `get_wash_debug_params` — Wash debug parameters (read)

Wrapper only; no call site.

| | |
|---|---|
| Evidence | ✅ Bundle (wrapper only) — no call site found in the bundles |
| Other bundles | wrapper only: 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_wash_debug_params", "params": []}
```

**Related:** [`set_wash_debug_params`](dock.md#set_wash_debug_params)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCleanRollerDebugInfo`) · anchor `"get_wash_debug_params"`
- `a65@1.0.95` · wrapper m10115 (`getCleanRollerDebugInfo`) · anchor `"get_wash_debug_params"`
- `a62@1.0.69` · wrapper m10109 (`getCleanRollerDebugInfo`) · anchor `"get_wash_debug_params"`

</details>

<a id="set_wash_debug_params"></a>
### `set_wash_debug_params` — Wash debug parameters (write)

Wrapper only; four separate wrappers set one key each.

| | |
|---|---|
| Evidence | ✅ Bundle (wrapper only) — no call site found in the bundles |
| Other bundles | wrapper only: 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"washinterval": <v>}`, `{"dryingtime": <v>}`, `{"rollerspeed": <v>}` or `{"moppingspeed": <v>}`.

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Related:** [`get_wash_debug_params`](dock.md#get_wash_debug_params)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setDryingTime, setMoppingSpeed, setRollerSpeed, setWashInterval`) · anchor `"set_wash_debug_params"`
- `a65@1.0.95` · wrapper m10115 (`setDryingTime, setMoppingSpeed, setRollerSpeed, setWashInterval`) · anchor `"set_wash_debug_params"`
- `a62@1.0.69` · wrapper m10109 (`setDryingTime, setMoppingSpeed, setRollerSpeed, setWashInterval`) · anchor `"set_wash_debug_params"`

</details>

<a id="get_auto_delivery_cleaning_fluid"></a>
### `get_auto_delivery_cleaning_fluid` — Automatic cleaning-fluid dosing (read)

Reads the switch.

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
{"id": 1, "method": "get_auto_delivery_cleaning_fluid", "params": {}}
```

**Related:** [`set_auto_delivery_cleaning_fluid`](dock.md#set_auto_delivery_cleaning_fluid)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getAutoDeliveryCleanFluid`); call sites m14567 · anchor `"get_auto_delivery_cleaning_fluid"`
- `a65@1.0.95` · wrapper m10115 (`getAutoDeliveryCleanFluid`); call sites m14513 · anchor `"get_auto_delivery_cleaning_fluid"`
- `a29@1.0.75` · wrapper m10112 (`getAutoDeliveryCleanFluid`); call sites m14243 · anchor `"get_auto_delivery_cleaning_fluid"`

</details>

<a id="set_auto_delivery_cleaning_fluid"></a>
### `set_auto_delivery_cleaning_fluid` — Automatic cleaning-fluid dosing (write)

Turns automatic dosing on or off.

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
{"id": 1, "method": "set_auto_delivery_cleaning_fluid", "params": {"status": 1}}
```

**Related:** [`get_auto_delivery_cleaning_fluid`](dock.md#get_auto_delivery_cleaning_fluid)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setAutoDeliveryCleanFluid`); call sites m14567 · anchor `"set_auto_delivery_cleaning_fluid"`
- `a65@1.0.95` · wrapper m10115 (`setAutoDeliveryCleanFluid`); call sites m14513 · anchor `"set_auto_delivery_cleaning_fluid"`
- `a29@1.0.75` · wrapper m10112 (`setAutoDeliveryCleanFluid`); call sites m14243 · anchor `"set_auto_delivery_cleaning_fluid"`

</details>

<a id="clean_roller"></a>
### `clean_roller` — Clean the roller (older dock generation)

Starts or stops the mop-roller cleaning (the older name of the wash action).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 10: a08 a09 a10 a14 a15 a19 a23 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"action": 0}` starts, `{"action": 1}` stops (`startCleanRoller` / `stopCleanRoller`, a14 wrapper).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "clean_roller", "params": {"action": 0}}
```

**Related:** [`app_start_wash`](dock.md#app_start_wash)

<details><summary>Sources</summary>

- `a23@1.0.53` · wrapper m10142 (`startCleanRoller, stopCleanRoller`); call sites m11546 · anchor `"clean_roller"`
- `a15@1.0.53` · wrapper m10142 (`startCleanRoller, stopCleanRoller`); call sites m11546 · anchor `"clean_roller"`
- `a08@1.0.47` · wrapper m10013 (`startCleanRoller, stopCleanRoller`); call sites m11987 · anchor `"clean_roller"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
