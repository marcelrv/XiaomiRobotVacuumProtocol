# Fan power, water flow and mop modes

[Home](../../README.md) / [Commands](index.md) / Fan power, water flow and mop modes

Suction power, water box flow, mop route and the user-defined "customize clean mode" / mop-template features.

Three numeric families describe how the robot cleans: **fan power** (suction), **water box mode** (water flow) and **mop
mode** (route). The values the app knows are listed in
[fan, water and mop values](../reference/fan-water-mop.md). The status object reports the current values in
`fan_power`, `water_box_mode` and `mop_mode`; per-room overrides are the "customize clean mode" entries below.

Newer plugins combine the three into one call, [`set_clean_motor_mode`](#set_clean_motor_mode).

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`get_custom_mode`](#get_custom_mode) | Returns the current fan power value. | ✅ Bundle |
| [`set_custom_mode`](#set_custom_mode) | Sets the fan power code. | ✅ Bundle |
| [`get_water_box_custom_mode`](#get_water_box_custom_mode) | Returns the water box mode. | ✅ Bundle |
| [`set_water_box_custom_mode`](#set_water_box_custom_mode) | Sets the water box mode. | ✅ Bundle |
| [`get_clean_motor_mode`](#get_clean_motor_mode) | Wrapped in 32 bundles (a08 a09 a10 a14 … a76, s4 s5e s6); no call site found. | ✅ Bundle (wrapper only) |
| [`set_clean_motor_mode`](#set_clean_motor_mode) | Sets fan power and water mode (and mop mode) in one call. | ✅ Bundle |
| [`set_mop_mode`](#set_mop_mode) | Sets the mop mode code (`300`, `301`, `303`, `304`). | ✅ Bundle |
| [`get_customize_clean_mode`](#get_customize_clean_mode) | Returns the list of per-room ("customize clean mode") settings. | ✅ Bundle |
| [`set_customize_clean_mode`](#set_customize_clean_mode) | Writes the whole per-room list in one call. | ✅ Bundle |
| [`get_custom_clean_time`](#get_custom_clean_time) | Reads the maximum clean time setting; only in the oldest plugin generation. | ✅ Bundle |
| [`set_custom_clean_time`](#set_custom_clean_time) | Sets the maximum clean time in seconds. | ✅ Bundle |
| [`set_clean_sequence`](#set_clean_sequence) | Stores a custom order of room ids. | ✅ Bundle |
| [`get_clean_sequence`](#get_clean_sequence) | Returns the stored room order. | ✅ Bundle |
| [`add_mop_template_params`](#add_mop_template_params) | Adds a user-defined mop template (dock mop-washing parameters). | ✅ Bundle |
| [`update_mop_template_params`](#update_mop_template_params) | Replaces the parameters of an existing template. | ✅ Bundle |
| [`del_mop_template_params`](#del_mop_template_params) | Deletes a template by id. | ✅ Bundle |
| [`sort_mop_template_params`](#sort_mop_template_params) | Sets the display order of templates. | ✅ Bundle |
| [`get_mop_template_params_by_id`](#get_mop_template_params_by_id) | Returns the full parameters of one template. | ✅ Bundle |
| [`get_mop_template_params_summary`](#get_mop_template_params_summary) | Returns the template list. | ✅ Bundle |
| [`set_mop_template_id`](#set_mop_template_id) | Makes a template the active one. | ✅ Bundle |
| [`set_water_box_distance_off`](#set_water_box_distance_off) | Sets the custom water level used with water mode 207. | ✅ Bundle |
| [`set_corner_clean_mode`](#set_corner_clean_mode) | Switches the corner-cleaning option. | ✅ Bundle |
| [`get_mop_motor_status`](#get_mop_motor_status) | Reads the "layer mode" of the mop motor. | ✅ Bundle |
| [`set_mop_motor_status`](#set_mop_motor_status) | Sets the mop motor "layer mode". | ✅ Bundle |
| [`get_mop_reverse_pwm_values`](#get_mop_reverse_pwm_values) | Reads a debug parameter page value. | ✅ Bundle |
| [`set_mop_reverse_pwm_values`](#set_mop_reverse_pwm_values) | Writes the debug value. | ✅ Bundle |
| [`set_fan_motor_work_timeout`](#set_fan_motor_work_timeout) | Sets the fan "air drying" timeout in minutes (0 disables). | ✅ Bundle |
| [`get_fan_motor_work_timeout`](#get_fan_motor_work_timeout) | Reads the configured timeout. | ✅ Bundle |
| [`stop_fan_motor_work`](#stop_fan_motor_work) | Stops a running air-dry (also wrapped as `stopAirdryMop`). | ✅ Bundle |
| [`set_clean_follow_ground_material_status`](#set_clean_follow_ground_material_status) | Switches "follow floor material direction" cleaning. | ✅ Bundle |
| [`get_clean_follow_ground_material_status`](#get_clean_follow_ground_material_status) | Reads the switch. | ✅ Bundle |

<a id="get_custom_mode"></a>
### `get_custom_mode` — Get the fan power

Returns the current fan power value.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 20: a01 a08 a09 a10 a11 a14 a15 a19 a23 c1 e2 m1s p5 s4 s5 s5e s6 t4 t6 v1 model(s) |
| Other bundles | wrapper only: 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` is the fan power code (integer); the app tests for `105` ("mop" mode) to show a toast (a14 m12944).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_custom_mode", "params": []}
```

**Legacy documentation**

⚪ Legacy [custom_mode.md](../../custom_mode.md): "<100 = percent, >100 = extended modes". The bundles list the
extended codes 101–106 and 108 in newer builds and the percentage-style codes in
[fan values](../reference/fan-water-mop.md#fan-power); the same call is used for both.

**Related:** [`set_custom_mode`](cleaning-modes.md#set_custom_mode), [`get_water_box_custom_mode`](cleaning-modes.md#get_water_box_custom_mode)

<details><summary>Sources</summary>

- `a23@1.0.53` · wrapper m10142 (`getCustomMode`); call sites m12944; table key `GetCustomMode` · anchor `"GetCustomMode"`
- `a15@1.0.53` · wrapper m10142 (`getCustomMode`); call sites m12944; table key `GetCustomMode` · anchor `"GetCustomMode"`
- `t4@1.0.32` · wrapper m10010 (`getCustomMode`); call sites m11390; table key `GetCustomMode` · anchor `"GetCustomMode"`

</details>

<a id="set_custom_mode"></a>
### `set_custom_mode` — Set the fan power

Sets the fan power code.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<code>]` — one integer. Codes used by the app: `101` Silent, `102` Balanced, `103` Turbo, `104` Max, `105`
Gentle/"mop only" (`NoClean`), `106` customize, `108` Max+ (newer builds); older sapphire-family bundles use the
percentage-style codes of [fan values](../reference/fan-water-mop.md#fan-power). (⚪ Legacy [custom_mode.md](../../custom_mode.md) names the parameter `fan_level`.)

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code

```json
{"id": 106, "method": "set_custom_mode", "params": [102]}
```

**Behaviour in the app**

The mode picker sends this call and then, on products with an electronic water box, also
[`set_water_box_custom_mode`](#set_water_box_custom_mode) / [`set_clean_motor_mode`](#set_clean_motor_mode)
(a65 m10016).

**Legacy documentation**

⚪ Legacy: values 38 / 60 / 75 / 100 / 105 — present in the bundles as the "old" map of the Max/Turbo labels.

**Related:** [`get_custom_mode`](cleaning-modes.md#get_custom_mode), [`set_clean_motor_mode`](cleaning-modes.md#set_clean_motor_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCustomMode`); call sites m10016, m13031, m14168, m14354; table key `SetCustomMode` · anchor `"SetCustomMode"`
- `a65@1.0.95` · wrapper m10115 (`setCustomMode`); call sites m10016, m13019, m14138, m14324; table key `SetCustomMode` · anchor `"SetCustomMode"`
- `t4@1.0.32` · wrapper m10010 (`setCustomMode`); call sites m10628, m10838, m10841, m11453; table key `SetCustomMode` · anchor `"SetCustomMode"`

</details>

<a id="get_water_box_custom_mode"></a>
### `get_water_box_custom_mode` — Get the water flow

Returns the water box mode.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 4: a14 a15 a23 a62 model(s) |
| Other bundles | wrapper only: 38: a01 a08 a09 a10 a11 a19 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 c1 e2 m1s p5 s4 s5 s5e s6 t4 t6 v1 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` is the water mode code; the a62 mop-mode page maps anything other than 201/202/203 to 201.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_water_box_custom_mode", "params": []}
```

**Legacy documentation**

⚪ Legacy [water_box_custom_mode.md](../../water_box_custom_mode.md) also lists a response object
`{"water_box_mode", "distance_off"}`; no bundle reads that shape (the app reads `distance_off` from the status object).

**Related:** [`set_water_box_custom_mode`](cleaning-modes.md#set_water_box_custom_mode), [`set_water_box_distance_off`](cleaning-modes.md#set_water_box_distance_off)

<details><summary>Sources</summary>

- `a62@1.0.69` · wrapper m10109 (`getWaterBoxMode`); call sites m13928; table key `GetWaterBoxMode` · anchor `"GetWaterBoxMode"`
- `a23@1.0.53` · wrapper m10142 (`getWaterBoxMode`); call sites m13307; table key `GetWaterBoxMode` · anchor `"GetWaterBoxMode"`
- `a14@1.0.53` · wrapper m10142 (`getWaterBoxMode`); call sites m13307; table key `GetWaterBoxMode` · anchor `"GetWaterBoxMode"`

</details>

<a id="set_water_box_custom_mode"></a>
### `set_water_box_custom_mode` — Set the water flow

Sets the water box mode.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<code>]`. Codes: `200` off, `201` low, `202` medium, `203` high, `204` customize, `207` custom levels
([water values](../reference/fan-water-mop.md#water-box-mode)). The fine-grained level is set with
[`set_water_box_distance_off`](#set_water_box_distance_off).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_water_box_custom_mode", "params": [0]}
```

**Legacy documentation**

⚪ Legacy names the first parameter `water_flow_mode` and documents a second parameter form `{"water_box_mode": …, "distance_off": …}`. No bundle sends it; the bundles
use the separate `set_water_box_distance_off` call.

**Related:** [`get_water_box_custom_mode`](cleaning-modes.md#get_water_box_custom_mode), [`set_water_box_distance_off`](cleaning-modes.md#set_water_box_distance_off)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setWaterBoxMode`); call sites m10016, m13031, m14354; table key `SetWaterBoxMode` · anchor `"SetWaterBoxMode"`
- `a65@1.0.95` · wrapper m10115 (`setWaterBoxMode`); call sites m10016, m13019, m14324; table key `SetWaterBoxMode` · anchor `"SetWaterBoxMode"`
- `t4@1.0.32` · wrapper m10010 (`setWaterBoxMode`); call sites m10628, m10838, m10850; table key `SetWaterBoxMode` · anchor `"SetWaterBoxMode"`

</details>

<a id="get_clean_motor_mode"></a>
### `get_clean_motor_mode` — Get combined clean motor mode

Wrapped in 32 bundles (a08 a09 a10 a14 … a76, s4 s5e s6); no call site found.

| | |
|---|---|
| Evidence | ✅ Bundle (wrapper only) — no call site found in the bundles |
| Other bundles | wrapper only: 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[]` (a72) / `[mode]` (a08).

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_clean_motor_mode", "params": []}
```

**Related:** [`set_clean_motor_mode`](cleaning-modes.md#set_clean_motor_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getMopMode`) · anchor `"get_clean_motor_mode"`
- `a65@1.0.95` · wrapper m10115 (`getMopMode`) · anchor `"get_clean_motor_mode"`
- `a08@1.0.47` · wrapper m10013 (`getMopMode`) · anchor `"get_clean_motor_mode"`

</details>

<a id="set_clean_motor_mode"></a>
### `set_clean_motor_mode` — Set fan, water and mop mode at once

Sets fan power and water mode (and mop mode) in one call.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 37: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5 s5e s6 t4 t6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[{"fan_power": <int>, "water_box_mode": <int>}]`, or with a third key
`[{"fan_power": …, "water_box_mode": …, "mop_mode": <int>}]` (✅ Bundle · a08 wrapper `setCleanMotorMode` /
`setCleanMopMode`; a65 m10016: `setCleanMopMode(fanPower, newWater, 300)`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code

```json
{"id": 107, "method": "set_clean_motor_mode", "params": [{"fan_power": 102, "water_box_mode": 202, "mop_mode": 300}]}
```

**Related:** [`set_custom_mode`](cleaning-modes.md#set_custom_mode), [`set_water_box_custom_mode`](cleaning-modes.md#set_water_box_custom_mode), [`set_mop_mode`](cleaning-modes.md#set_mop_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCleanMopMode, setCleanMotorMode`); call sites m10016, m13031, m14354 · anchor `"set_clean_motor_mode"`
- `a65@1.0.95` · wrapper m10115 (`setCleanMopMode, setCleanMotorMode`); call sites m10016, m13019, m14324 · anchor `"set_clean_motor_mode"`
- `t4@1.0.32` · wrapper m10010 (`setCleanMotorMode`); call sites m10628 · anchor `"set_clean_motor_mode"`

</details>

<a id="set_mop_mode"></a>
### `set_mop_mode` — Set the mop route mode

Sets the mop mode code (`300`, `301`, `303`, `304`).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<code>]`; codes in [mop values](../reference/fan-water-mop.md#mop-mode).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_mop_mode", "params": [0]}
```

**Behaviour in the app**

After the call the app stores the value as `RSM.mopMode`; for 301/303/304 it additionally adjusts the water mode.

**Related:** [`set_clean_motor_mode`](cleaning-modes.md#set_clean_motor_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setMopMode`); call sites m10016 · anchor `"set_mop_mode"`
- `a65@1.0.95` · wrapper m10115 (`setMopMode`); call sites m10016 · anchor `"set_mop_mode"`
- `a08@1.0.47` · wrapper m10013 (`setMopMode`); call sites m11849 · anchor `"set_mop_mode"`

</details>

<a id="get_customize_clean_mode"></a>
### `get_customize_clean_mode` — Get the per-room clean modes

Returns the list of per-room ("customize clean mode") settings.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 38: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5 s5e s6 t4 t6 model(s) |
| Other bundles | alternate table only: 3: a01 c1 e2 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result` is an array (one element per customised room); the app keeps it as `customCleanModes` and passes it back unchanged.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_customize_clean_mode", "params": []}
```

**Related:** [`set_customize_clean_mode`](cleaning-modes.md#set_customize_clean_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCustomCleanMode`); call sites m10112; table key `GetCustomCleanMode` · anchor `"GetCustomCleanMode"`
- `a65@1.0.95` · wrapper m10115 (`getCustomCleanMode`); call sites m10112; table key `GetCustomCleanMode` · anchor `"GetCustomCleanMode"`
- `t4@1.0.32` · wrapper m10010 (`getCustomCleanMode`); call sites m10553; table key `GetCustomCleanMode` · anchor `"GetCustomCleanMode"`

</details>

<a id="set_customize_clean_mode"></a>
### `set_customize_clean_mode` — Set the per-room clean modes

Writes the whole per-room list in one call.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 38: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5 s5e s6 t4 t6 model(s) |
| Other bundles | alternate table only: 3: a01 c1 e2 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params` is the **array of room objects** (not wrapped again), each of the form
`{"segment": <room id>, "fan_power": <int>, "water_box_mode": <int>, "mop_mode": <int>, "mop_template_id": <int>}`
(✅ Bundle · a65 m14324: the "smart" preset fills `fan_power` 101 or 102, `water_box_mode` 202, `mop_mode` 300).
An empty array `[]` resets the customisation (m14321/`resetCleanMode`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_customize_clean_mode", "params": {"segment": 16, "fan_power": 1, "water_box_mode": 1, "mop_mode": 1, "mop_template_id": 1}}
```

**Behaviour in the app**

In the retry list: the plugin adds `need_retry` ([transports](../concepts/transports.md#retry-protocol)).

**Related:** [`get_customize_clean_mode`](cleaning-modes.md#get_customize_clean_mode), [`get_room_mapping`](rooms-and-areas.md#get_room_mapping)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCustomCleanMode`); call sites m14354; table key `SetCustomCleanMode` · anchor `"SetCustomCleanMode"`
- `a65@1.0.95` · wrapper m10115 (`setCustomCleanMode`); call sites m14324; table key `SetCustomCleanMode` · anchor `"SetCustomCleanMode"`
- `t4@1.0.32` · wrapper m10010 (`setCustomCleanMode`); call sites m10886; table key `SetCustomCleanMode` · anchor `"SetCustomCleanMode"`

</details>

<a id="get_custom_clean_time"></a>
### `get_custom_clean_time` — Custom clean time (legacy feature)

Reads the maximum clean time setting; only in the oldest plugin generation.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 3: a01 c1 e2 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` is a duration in seconds from the list 0, 600, 1200, … 3600 (`0` = automatic). Gated by a firmware feature id (103).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_custom_clean_time", "params": []}
```

**Related:** [`set_custom_clean_time`](cleaning-modes.md#set_custom_clean_time)

<details><summary>Sources</summary>

- `a01@1.0.51` · call sites m11522, m11582; table key `GetCustomCleanTime` · anchor `"GetCustomCleanTime"`
- `e2@1.0.48` · call sites m11519, m11579; table key `GetCustomCleanTime` · anchor `"GetCustomCleanTime"`
- `c1@1.0.48` · call sites m11519, m11579; table key `GetCustomCleanTime` · anchor `"GetCustomCleanTime"`

</details>

<a id="set_custom_clean_time"></a>
### `set_custom_clean_time` — Set the custom clean time

Sets the maximum clean time in seconds.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 3: a01 c1 e2 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<seconds>]`; choices offered: 0 (auto), 600, 1200, 1800, 2400, 3000, 3600.

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result.length` (3), `result[0]` (3). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_custom_clean_time", "params": [3600]}
```

**Related:** [`get_custom_clean_time`](cleaning-modes.md#get_custom_clean_time)

<details><summary>Sources</summary>

- `a01@1.0.51` · call sites m11582; table key `SetCustomCleanTime` · anchor `"SetCustomCleanTime"`
- `e2@1.0.48` · call sites m11579; table key `SetCustomCleanTime` · anchor `"SetCustomCleanTime"`
- `c1@1.0.48` · call sites m11579; table key `SetCustomCleanTime` · anchor `"SetCustomCleanTime"`

</details>

<a id="set_clean_sequence"></a>
### `set_clean_sequence` — Set the room cleaning order

Stores a custom order of room ids.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Other bundles | wrapper only: 1: s5 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: the array of selected room ids in order; `[]` resets the order.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_clean_sequence", "params": []}
```

**Behaviour in the app**

Listed in the retry-capable methods ([transports](../concepts/transports.md#retry-protocol)).

**Related:** [`get_clean_sequence`](cleaning-modes.md#get_clean_sequence), [`app_segment_clean`](cleaning-control.md#app_segment_clean)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCleanSequence`); call sites m14351 · anchor `"set_clean_sequence"`
- `a65@1.0.95` · wrapper m10115 (`setCleanSequence`); call sites m14321 · anchor `"set_clean_sequence"`
- `a11@1.0.34` · wrapper m10010 (`setCleanSequence`); call sites m10748 · anchor `"set_clean_sequence"`

</details>

<a id="get_clean_sequence"></a>
### `get_clean_sequence` — Get the room cleaning order

Returns the stored room order.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 34: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5e s6 model(s) |
| Other bundles | wrapper only: 1: s5 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result` is the array of room ids (`cleanSequence`).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_clean_sequence", "params": []}
```

**Related:** [`set_clean_sequence`](cleaning-modes.md#set_clean_sequence)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCleanSequence`); call sites m10112 · anchor `"get_clean_sequence"`
- `a65@1.0.95` · wrapper m10115 (`getCleanSequence`); call sites m10112 · anchor `"get_clean_sequence"`
- `a11@1.0.34` · wrapper m10010 (`getCleanSequence`); call sites m10271 · anchor `"get_clean_sequence"`

</details>

<a id="add_mop_template_params"></a>
### `add_mop_template_params` — Create a custom mop mode

Adds a user-defined mop template (dock mop-washing parameters).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: one object `config` assembled by the editor; the readable fields of a template (see
[`get_mop_template_params_by_id`](#get_mop_template_params_by_id)) are `name`, `dry_time`, `roller_speed`,
`wash_count`, `wash_interval_time`, `wash_time`, `move_speed`, `sys_type`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`update_mop_template_params`](cleaning-modes.md#update_mop_template_params), [`del_mop_template_params`](cleaning-modes.md#del_mop_template_params), [`set_mop_template_id`](cleaning-modes.md#set_mop_template_id)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`addCustomMopMode`); call sites m13001 · anchor `"add_mop_template_params"`
- `a65@1.0.95` · wrapper m10115 (`addCustomMopMode`); call sites m12989 · anchor `"add_mop_template_params"`
- `a62@1.0.69` · wrapper m10109 (`addCustomMopMode`); call sites m12554 · anchor `"add_mop_template_params"`

</details>

<a id="update_mop_template_params"></a>
### `update_mop_template_params` — Update a custom mop mode

Replaces the parameters of an existing template.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: the template object (same keys as above plus `id`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`add_mop_template_params`](cleaning-modes.md#add_mop_template_params)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`updateCustomMopMode`); call sites m13001 · anchor `"update_mop_template_params"`
- `a65@1.0.95` · wrapper m10115 (`updateCustomMopMode`); call sites m12989 · anchor `"update_mop_template_params"`
- `a62@1.0.69` · wrapper m10109 (`updateCustomMopMode`); call sites m12554 · anchor `"update_mop_template_params"`

</details>

<a id="del_mop_template_params"></a>
### `del_mop_template_params` — Delete a custom mop mode

Deletes a template by id.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"id": <int>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "del_mop_template_params", "params": {"id": 1}}
```

**Behaviour in the app**

The app refuses (toast) when the template is currently in use.

**Related:** [`add_mop_template_params`](cleaning-modes.md#add_mop_template_params)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`delCustomMopMode`); call sites m13001 · anchor `"del_mop_template_params"`
- `a65@1.0.95` · wrapper m10115 (`delCustomMopMode`); call sites m12989 · anchor `"del_mop_template_params"`
- `a62@1.0.69` · wrapper m10109 (`delCustomMopMode`); call sites m12554 · anchor `"del_mop_template_params"`

</details>

<a id="sort_mop_template_params"></a>
### `sort_mop_template_params` — Reorder custom mop modes

Sets the display order of templates.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"ids": [<id>, …], "show_index": <int>}` — `show_index` is the number of templates in the first group (a65 m14426).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "sort_mop_template_params", "params": {"ids": [1], "show_index": 1}}
```

**Related:** [`get_mop_template_params_summary`](cleaning-modes.md#get_mop_template_params_summary)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`sortCustomMopModes`); call sites m14456 · anchor `"sort_mop_template_params"`
- `a65@1.0.95` · wrapper m10115 (`sortCustomMopModes`); call sites m14426 · anchor `"sort_mop_template_params"`
- `a62@1.0.69` · wrapper m10109 (`sortCustomMopModes`); call sites m13985 · anchor `"sort_mop_template_params"`

</details>

<a id="get_mop_template_params_by_id"></a>
### `get_mop_template_params_by_id` — Read a custom mop mode

Returns the full parameters of one template.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"id": <int>}`.

**Response**

`result` object with `dry_time`, `name`, `roller_speed`, `sys_type`, `wash_count`, `wash_interval_time`, `wash_time`, `move_speed` (✅ Bundle · a65 m12989).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_mop_template_params_by_id", "params": {"id": 1}}
```

**Related:** [`get_mop_template_params_summary`](cleaning-modes.md#get_mop_template_params_summary)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCustomMopModeDetail`); call sites m13001 · anchor `"get_mop_template_params_by_id"`
- `a65@1.0.95` · wrapper m10115 (`getCustomMopModeDetail`); call sites m12989 · anchor `"get_mop_template_params_by_id"`
- `a62@1.0.69` · wrapper m10109 (`getCustomMopModeDetail`); call sites m12554 · anchor `"get_mop_template_params_by_id"`

</details>

<a id="get_mop_template_params_summary"></a>
### `get_mop_template_params_summary` — List custom mop modes

Returns the template list.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 9: a29 a30 a34 a37 a38 a40 a52 a62 a76 model(s) |
| Other bundles | wrapper only: 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`{}`).

**Response**

`result` is the list shown on the mop-mode page (`customMopModeListData`); element fields were not decoded here (❓ Unknown).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_mop_template_params_summary", "params": {}}
```

**Related:** [`get_mop_template_params_by_id`](cleaning-modes.md#get_mop_template_params_by_id)

<details><summary>Sources</summary>

- `a76@1.0.77` · wrapper m10112 (`getCustomMopModeList`); call sites m12713 · anchor `"get_mop_template_params_summary"`
- `a30@1.0.75` · wrapper m10112 (`getCustomMopModeList`); call sites m12707 · anchor `"get_mop_template_params_summary"`
- `a62@1.0.69` · wrapper m10109 (`getCustomMopModeList`); call sites m12542 · anchor `"get_mop_template_params_summary"`

</details>

<a id="set_mop_template_id"></a>
### `set_mop_template_id` — Select a custom mop mode

Makes a template the active one.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"mop_template_id": <int>}`; the status field `mop_template_id` reports it back.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_mop_template_id", "params": {"mop_template_id": 1}}
```

**Related:** [`get_mop_template_params_summary`](cleaning-modes.md#get_mop_template_params_summary)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCustomMopById`); call sites m12995 · anchor `"set_mop_template_id"`
- `a65@1.0.95` · wrapper m10115 (`setCustomMopById`); call sites m12983 · anchor `"set_mop_template_id"`
- `a62@1.0.69` · wrapper m10109 (`setCustomMopById`); call sites m12548, m12587 · anchor `"set_mop_template_id"`

</details>

<a id="set_water_box_distance_off"></a>
### `set_water_box_distance_off` — Fine water level

Sets the custom water level used with water mode 207.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |
| Call-site gate | the call sits behind `isCustomWaterBoxDistanceSupported` (tests found in the enclosing code of the call sites; [feature flags](../concepts/feature-flags.md)) |

**Request**

`params`: `{"distance_off": <int>}`. The slider code sends `sliderWaterTotal − slider position`
(a65 m10016: `setWaterBoxDistance(sliderWaterTotal - value)`); one bundle uses `265 − value` (a30). The value range is
therefore device-dependent and ❓ Unknown as a firmware range.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_water_box_distance_off", "params": {"distance_off": 20}}
```

**Behaviour in the app**

Offered only when the firmware reports the new-feature bit `isCustomWaterBoxDistanceSupported` (low word bit 31).

**Related:** [`set_water_box_custom_mode`](cleaning-modes.md#set_water_box_custom_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setWaterBoxDistance`); call sites m10016 · anchor `"set_water_box_distance_off"`
- `a65@1.0.95` · wrapper m10115 (`setWaterBoxDistance`); call sites m10016 · anchor `"set_water_box_distance_off"`
- `a62@1.0.69` · wrapper m10109 (`setWaterBoxDistance`); call sites m10016 · anchor `"set_water_box_distance_off"`

</details>

<a id="set_corner_clean_mode"></a>
### `set_corner_clean_mode` — Corner clean on/off

Switches the corner-cleaning option.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 10: a26 a27 a46 a64 a65 a66 a72 a73 a74 a75 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"status": 0|1}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_corner_clean_mode", "params": {"status": 1}}
```

**Behaviour in the app**

Offered when `isCornerCleanModeSupported`; the status field `corner_clean_mode` reports it.

**Related:** [`set_clean_motor_mode`](cleaning-modes.md#set_clean_motor_mode)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setCornerCleanMode`); call sites m10016 · anchor `"set_corner_clean_mode"`
- `a65@1.0.95` · wrapper m10115 (`setCornerCleanMode`); call sites m10016 · anchor `"set_corner_clean_mode"`
- `a26@1.0.84` · wrapper m10115 (`setCornerCleanMode`); call sites m10016 · anchor `"set_corner_clean_mode"`

</details>

<a id="get_mop_motor_status"></a>
### `get_mop_motor_status` — Mop lifting mode (read)

Reads the "layer mode" of the mop motor.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 4: a14 a15 a23 a62 model(s) |
| Other bundles | wrapper only: 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.status` (object, not array): 0 or 1 (other values are treated as 0).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_mop_motor_status", "params": []}
```

**Related:** [`set_mop_motor_status`](cleaning-modes.md#set_mop_motor_status)

<details><summary>Sources</summary>

- `a62@1.0.69` · wrapper m10109 (`getMopMontorStatus`); call sites m13928 · anchor `"get_mop_motor_status"`
- `a23@1.0.53` · wrapper m10142 (`getMopMontorStatus`); call sites m13307 · anchor `"get_mop_motor_status"`
- `a14@1.0.53` · wrapper m10142 (`getMopMontorStatus`); call sites m13307 · anchor `"get_mop_motor_status"`

</details>

<a id="set_mop_motor_status"></a>
### `set_mop_motor_status` — Mop lifting mode (write)

Sets the mop motor "layer mode".

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 4: a14 a15 a23 a62 model(s) |
| Other bundles | wrapper only: 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"status": 0|1}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_mop_motor_status", "params": {"status": 1}}
```

**Related:** [`get_mop_motor_status`](cleaning-modes.md#get_mop_motor_status)

<details><summary>Sources</summary>

- `a62@1.0.69` · wrapper m10109 (`setMopMontorStatus`); call sites m13928 · anchor `"set_mop_motor_status"`
- `a23@1.0.53` · wrapper m10142 (`setMopMontorStatus`); call sites m13307 · anchor `"set_mop_motor_status"`
- `a14@1.0.53` · wrapper m10142 (`setMopMontorStatus`); call sites m13307 · anchor `"set_mop_motor_status"`

</details>

<a id="get_mop_reverse_pwm_values"></a>
### `get_mop_reverse_pwm_values` — Mop back-PWM (debug)

Reads a debug parameter page value.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`{}`).

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result.pwm` (11). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_mop_reverse_pwm_values", "params": {}}
```

**Behaviour in the app**

Debug page only (a65 m14387; the page has Chinese debug texts).

**Related:** [`set_mop_reverse_pwm_values`](cleaning-modes.md#set_mop_reverse_pwm_values)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getMopBackPWM`); call sites m14417 · anchor `"get_mop_reverse_pwm_values"`
- `a65@1.0.95` · wrapper m10115 (`getMopBackPWM`); call sites m14387 · anchor `"get_mop_reverse_pwm_values"`
- `a51@1.0.83` · wrapper m10115 (`getMopBackPWM`); call sites m14366 · anchor `"get_mop_reverse_pwm_values"`

</details>

<a id="set_mop_reverse_pwm_values"></a>
### `set_mop_reverse_pwm_values` — Mop back-PWM (debug write)

Writes the debug value.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: an object `param` built by the debug page from an integer entered by the user.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`get_mop_reverse_pwm_values`](cleaning-modes.md#get_mop_reverse_pwm_values)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setMopBackPWM`); call sites m14417 · anchor `"set_mop_reverse_pwm_values"`
- `a65@1.0.95` · wrapper m10115 (`setMopBackPWM`); call sites m14387 · anchor `"set_mop_reverse_pwm_values"`
- `a51@1.0.83` · wrapper m10115 (`setMopBackPWM`); call sites m14366 · anchor `"set_mop_reverse_pwm_values"`

</details>

<a id="set_fan_motor_work_timeout"></a>
### `set_fan_motor_work_timeout` — Air-dry duration

Sets the fan "air drying" timeout in minutes (0 disables).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"timeout": <minutes>}`; the app sends 360 for "on" and 0 for "off" (a65 m14420).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_fan_motor_work_timeout", "params": {"timeout": 360}}
```

**Related:** [`get_fan_motor_work_timeout`](cleaning-modes.md#get_fan_motor_work_timeout), [`stop_fan_motor_work`](cleaning-modes.md#stop_fan_motor_work)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setFanMotorWorkTimeout`); call sites m14450 · anchor `"set_fan_motor_work_timeout"`
- `a65@1.0.95` · wrapper m10115 (`setFanMotorWorkTimeout`); call sites m14420 · anchor `"set_fan_motor_work_timeout"`
- `a14@1.0.53` · wrapper m10142 (`setFanMotorWorkTimeout`); call sites m13007, m13304 · anchor `"set_fan_motor_work_timeout"`

</details>

<a id="get_fan_motor_work_timeout"></a>
### `get_fan_motor_work_timeout` — Air-dry duration (read)

Reads the configured timeout.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` minutes (0 = off).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_fan_motor_work_timeout", "params": []}
```

**Related:** [`set_fan_motor_work_timeout`](cleaning-modes.md#set_fan_motor_work_timeout)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getFanMotorWorkTimeout`); call sites m14450 · anchor `"get_fan_motor_work_timeout"`
- `a65@1.0.95` · wrapper m10115 (`getFanMotorWorkTimeout`); call sites m14420 · anchor `"get_fan_motor_work_timeout"`
- `a14@1.0.53` · wrapper m10142 (`getFanMotorWorkTimeout`); call sites m13007 · anchor `"get_fan_motor_work_timeout"`

</details>

<a id="stop_fan_motor_work"></a>
### `stop_fan_motor_work` — Stop air drying

Stops a running air-dry (also wrapped as `stopAirdryMop`).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "stop_fan_motor_work", "params": []}
```

**Related:** [`set_fan_motor_work_timeout`](cleaning-modes.md#set_fan_motor_work_timeout), [`stop_airdry_mop`](dock.md#stop_airdry_mop)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`stopAirdryMop`); call sites m14450 · anchor `"stop_fan_motor_work"`
- `a65@1.0.95` · wrapper m10115 (`stopAirdryMop`); call sites m14420 · anchor `"stop_fan_motor_work"`
- `a62@1.0.69` · wrapper m10109 (`stopAirdryMop`); call sites m13979 · anchor `"stop_fan_motor_work"`

</details>

<a id="set_clean_follow_ground_material_status"></a>
### `set_clean_follow_ground_material_status` — Clean along the floor direction

Switches "follow floor material direction" cleaning.

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
{"id": 1, "method": "set_clean_follow_ground_material_status", "params": {"status": 1}}
```

**Related:** [`get_clean_follow_ground_material_status`](cleaning-modes.md#get_clean_follow_ground_material_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setFloorDirectionCleanStatus`); call sites m14345 · anchor `"set_clean_follow_ground_material_status"`
- `a65@1.0.95` · wrapper m10115 (`setFloorDirectionCleanStatus`); call sites m14315 · anchor `"set_clean_follow_ground_material_status"`
- `a29@1.0.75` · wrapper m10112 (`setFloorDirectionCleanStatus`); call sites m14045 · anchor `"set_clean_follow_ground_material_status"`

</details>

<a id="get_clean_follow_ground_material_status"></a>
### `get_clean_follow_ground_material_status` — Clean along the floor direction (read)

Reads the switch.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result.status == 1` means on.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_clean_follow_ground_material_status", "params": []}
```

**Related:** [`set_clean_follow_ground_material_status`](cleaning-modes.md#set_clean_follow_ground_material_status)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getFloorDirectionCleanStatus`); call sites m14345 · anchor `"get_clean_follow_ground_material_status"`
- `a65@1.0.95` · wrapper m10115 (`getFloorDirectionCleanStatus`); call sites m14315 · anchor `"get_clean_follow_ground_material_status"`
- `a29@1.0.75` · wrapper m10112 (`getFloorDirectionCleanStatus`); call sites m14045 · anchor `"get_clean_follow_ground_material_status"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
