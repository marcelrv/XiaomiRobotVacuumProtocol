# Timers and Do-Not-Disturb

[Home](../../README.md) / [Commands](index.md) / Timers and Do-Not-Disturb

Cleaning schedules (robot-side and server-side), Do-Not-Disturb and valley-electricity timers.

Two timer stores exist: **robot timers** (`*_timer`) and **server timers** (`*_server_timer`). The plugin uses robot timers
when the status of the FCC flag is 0 (`local_info.featureset & 1`, see [`app_get_init_status`](status.md#app_get_init_status))
and server timers when it is 1 (✅ Bundle · a65 m13991 `setTimer`). In Mi Home on FCC robots the app also converts the
schedule to Beijing time before building the cron string. Timer identifiers are called `name` in the app and are
decimal strings created by the app (legacy `timer_id`).

A schedule is a cron string `"<min> <hour> <day> <month> <weekday>"`.

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`get_timer`](#get_timer) | Returns all robot timers with their schedule and command. | ✅ Bundle |
| [`set_timer`](#set_timer) | Creates a timer that starts a clean. | ✅ Bundle |
| [`del_timer`](#del_timer) | Removes a timer by name. | ✅ Bundle |
| [`upd_timer`](#upd_timer) | Switches a timer on or off. | ✅ Bundle |
| [`get_server_timer`](#get_server_timer) | Returns the timers kept in the server store. | ✅ Bundle |
| [`set_server_timer`](#set_server_timer) | Creates a timer in the server store (used for FCC state 1). | ✅ Bundle |
| [`del_server_timer`](#del_server_timer) | Deletes server timers by name. | ✅ Bundle |
| [`upd_server_timer`](#upd_server_timer) | Switches a server timer. | ✅ Bundle |
| [`get_timer_summary`](#get_timer_summary) | Returns the names of all robot timers. | ✅ Bundle |
| [`get_timer_detail`](#get_timer_detail) | Returns the full entry of a timer. | ✅ Bundle |
| [`get_dnd_timer`](#get_dnd_timer) | Returns the DND window and, on newer firmware, its actions. | ✅ Bundle |
| [`set_dnd_timer`](#set_dnd_timer) | Sets and enables the DND window. | ✅ Bundle |
| [`close_dnd_timer`](#close_dnd_timer) | Disables DND. | ✅ Bundle |
| [`set_dnd_timer_actions`](#set_dnd_timer_actions) | Chooses what is suppressed or resumed during DND. | ✅ Bundle |
| [`get_valley_electricity_timer`](#get_valley_electricity_timer) | Returns the "valley electricity" charging window. | ✅ Bundle |
| [`set_valley_electricity_timer`](#set_valley_electricity_timer) | Sets the window. | ✅ Bundle |
| [`close_valley_electricity_timer`](#close_valley_electricity_timer) | Disables the window. | ✅ Bundle |

<a id="get_timer"></a>
### `get_timer` — List robot timers (full)

Returns all robot timers with their schedule and command.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result` array, one entry per timer (`res.result.length` is the count). Newer plugins prefer [`get_timer_summary`](#get_timer_summary) + [`get_timer_detail`](#get_timer_detail) when fw feature 122 is present.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_timer", "params": []}
```

**Legacy documentation**

⚪ Legacy [timer.md](../../timer.md) — cron-like string; the legacy note that times are China-timezone based is consistent with the plugin converting to Beijing time for FCC robots.

**Related:** [`set_timer`](timers.md#set_timer), [`upd_timer`](timers.md#upd_timer), [`del_timer`](timers.md#del_timer), [`get_timer_summary`](timers.md#get_timer_summary)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getTimer`); call sites m13013, m14357; table key `GetTimer` · anchor `"GetTimer"`
- `a65@1.0.95` · wrapper m10115 (`getTimer`); call sites m13001, m14327; table key `GetTimer` · anchor `"GetTimer"`
- `t4@1.0.32` · wrapper m10010 (`getTimer`); call sites m11255; table key `GetTimer` · anchor `"GetTimer"`

</details>

<a id="set_timer"></a>
### `set_timer` — Create a robot timer

Creates a timer that starts a clean.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[ [<name>, [<cron>, <command>]] ]` — a one-element array whose element is the timer.
`<command>` is one of:

| Form | When | Content |
|---|---|---|
| `["start_clean", <mode>, [<segment ids>], <map id>?]` | firmware without fw feature 114 | old logic; the map id is added with `isMultiMapSegmentTimerSupported` |
| `["start_clean", {"segments": […], "repeat": 1, "fan_power": …, "clean_order_mode": …, "water_box_mode": …, "clean_mop": …, "map_index": …, "mop_mode": …, "mop_template_id": …}]` | firmware with fw feature 114 | `map_index` with multi-map timers (new-feature bit 12), `mop_mode` with `isShakeMopSetSupported` (bit 18), `mop_template_id` for the Garnet line |

✅ Bundle · a65 m13991 `getOldLogicPara` / `getNewLogicPara`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (old logic)

```json
{"id": 109, "method": "set_timer", "params": [["1700000000000", ["30 12 * * 1,2,3,4,5", ["start_clean", 102, [16, 17]]]]]}
```

**Behaviour in the app**

In the retry-capable list ([transports](../concepts/transports.md#retry-protocol)). The app stops a running clean first when the timer is for a different map.

**Related:** [`upd_timer`](timers.md#upd_timer), [`del_timer`](timers.md#del_timer), [`set_server_timer`](timers.md#set_server_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setTimer`); call sites m14021; table key `SetTimer` · anchor `"SetTimer"`
- `a65@1.0.95` · wrapper m10115 (`setTimer`); call sites m13991; table key `SetTimer` · anchor `"SetTimer"`
- `t4@1.0.32` · wrapper m10010 (`setTimer`); call sites m11267; table key `SetTimer` · anchor `"SetTimer"`

</details>

<a id="del_timer"></a>
### `del_timer` — Delete a robot timer

Removes a timer by name.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<name>]`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "del_timer", "params": ["name"]}
```

**Related:** [`set_timer`](timers.md#set_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`deleteTimer`); call sites m13013; table key `DelTimer` · anchor `"DelTimer"`
- `a65@1.0.95` · wrapper m10115 (`deleteTimer`); call sites m13001; table key `DelTimer` · anchor `"DelTimer"`
- `t4@1.0.32` · wrapper m10010 (`deleteTimer`); call sites m11255; table key `DelTimer` · anchor `"DelTimer"`

</details>

<a id="upd_timer"></a>
### `upd_timer` — Enable / disable a robot timer

Switches a timer on or off.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<name>, "on"|"off"]` (✅ Bundle · a01 wrapper `updateTimer([timer.name, cmd])`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "upd_timer", "params": ["name", "on"]}
```

**Legacy documentation**

⚪ Legacy [timer.md](../../timer.md): `[timer_id, "on"|"off"]` (the legacy text calls the two values `activate` and `deactive`) — confirmed.

**Related:** [`set_timer`](timers.md#set_timer), [`upd_server_timer`](timers.md#upd_server_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`updateTimer`); call sites m13013; table key `UpdTimer` · anchor `"UpdTimer"`
- `a65@1.0.95` · wrapper m10115 (`updateTimer`); call sites m13001; table key `UpdTimer` · anchor `"UpdTimer"`
- `t4@1.0.32` · wrapper m10010 (`updateTimer`); call sites m11255; table key `UpdTimer` · anchor `"UpdTimer"`

</details>

<a id="get_server_timer"></a>
### `get_server_timer` — List server timers

Returns the timers kept in the server store.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result` is an array of timer entries; the app deletes them one by one when migrating (`delAllServerTimersFromRobot`).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_server_timer", "params": []}
```

**Related:** [`set_server_timer`](timers.md#set_server_timer), [`del_server_timer`](timers.md#del_server_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getServerTimer`); call sites m13013, m13994; table key `GetServerTimer` · anchor `"GetServerTimer"`
- `a65@1.0.95` · wrapper m10115 (`getServerTimer`); call sites m13001, m13979; table key `GetServerTimer` · anchor `"GetServerTimer"`
- `t4@1.0.32` · wrapper m10010 (`getServerTimer`); call sites m11255, m11258; table key `GetServerTimer` · anchor `"GetServerTimer"`

</details>

<a id="set_server_timer"></a>
### `set_server_timer` — Create a server timer

Creates a timer in the server store (used for FCC state 1).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 39: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5 s5e s6 t4 t6 v1 model(s) |
| Other bundles | wrapper only: 3: a01 c1 e2 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[ [<name>, [<cron>, ["start_clean", …]]] ]` (old-logic parameter); the reply `result[0]` is a segment string (`ok` is replaced by `0`).

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result[0].replace` (39). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Behaviour in the app**

Retry-capable. In Mi Home the app additionally creates a Mi automation scene for the timer.

**Legacy documentation**

⚪ README lists the server-timer methods as "s5e only".

**Related:** [`set_timer`](timers.md#set_timer), [`upd_server_timer`](timers.md#upd_server_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setServerTimer`); call sites m14021; table key `SetServerTimer` · anchor `"SetServerTimer"`
- `a65@1.0.95` · wrapper m10115 (`setServerTimer`); call sites m13991; table key `SetServerTimer` · anchor `"SetServerTimer"`
- `t4@1.0.32` · wrapper m10010 (`setServerTimer`); call sites m11267; table key `SetServerTimer` · anchor `"SetServerTimer"`

</details>

<a id="del_server_timer"></a>
### `del_server_timer` — Delete server timers

Deletes server timers by name.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<name or ids>]`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`set_server_timer`](timers.md#set_server_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`deleteServerTimer`); call sites m13013, m13025, m13994; table key `DeleteServerTimer` · anchor `"DeleteServerTimer"`
- `a65@1.0.95` · wrapper m10115 (`deleteServerTimer`); call sites m13001, m13013, m13979; table key `DeleteServerTimer` · anchor `"DeleteServerTimer"`
- `t4@1.0.32` · wrapper m10010 (`deleteServerTimer`); call sites m11258, m11285; table key `DeleteServerTimer` · anchor `"DeleteServerTimer"`

</details>

<a id="upd_server_timer"></a>
### `upd_server_timer` — Enable / disable a server timer

Switches a server timer.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 39: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5 s5e s6 t4 t6 v1 model(s) |
| Other bundles | wrapper only: 3: a01 c1 e2 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[[<name>, "on"|"off"]]`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "upd_server_timer", "params": [["name", "on"]]}
```

**Related:** [`upd_timer`](timers.md#upd_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`updateServerTimer`); call sites m13013; table key `UpdateServerTimer` · anchor `"UpdateServerTimer"`
- `a65@1.0.95` · wrapper m10115 (`updateServerTimer`); call sites m13001; table key `UpdateServerTimer` · anchor `"UpdateServerTimer"`
- `t4@1.0.32` · wrapper m10010 (`updateServerTimer`); call sites m11255; table key `UpdateServerTimer` · anchor `"UpdateServerTimer"`

</details>

<a id="get_timer_summary"></a>
### `get_timer_summary` — List robot timer names

Returns the names of all robot timers.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 37: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5 s5e s6 t4 t6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result` is an array of timer names; the plugin calls [`get_timer_detail`](#get_timer_detail) for each.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_timer_summary", "params": []}
```

**Behaviour in the app**

Gated by fw feature code 122 (`isSupportFetchTimerSummary`) and not offered for the `Tanos_CN` product (t6).

**Related:** [`get_timer_detail`](timers.md#get_timer_detail)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getTimerListSummary`); call sites m13013, m14357 · anchor `"get_timer_summary"`
- `a65@1.0.95` · wrapper m10115 (`getTimerListSummary`); call sites m13001, m14327 · anchor `"get_timer_summary"`
- `t4@1.0.32` · wrapper m10010 (`getTimerListSummary`); call sites m11255 · anchor `"get_timer_summary"`

</details>

<a id="get_timer_detail"></a>
### `get_timer_detail` — Read one robot timer

Returns the full entry of a timer.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 37: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 p5 s4 s5 s5e s6 t4 t6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<name>]`.

**Response**

`result[0]` is the timer `[name, enabled, [cron, [cmd…]]]`: the plugin reads index 2 as the crontab pair `[cron, command]` (a65 m14327).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_timer_detail", "params": ["name"]}
```

**Related:** [`get_timer_summary`](timers.md#get_timer_summary)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getTimerDetail`); call sites m13013, m14357 · anchor `"get_timer_detail"`
- `a65@1.0.95` · wrapper m10115 (`getTimerDetail`); call sites m13001, m14327 · anchor `"get_timer_detail"`
- `t4@1.0.32` · wrapper m10010 (`getTimerDetail`); call sites m11255 · anchor `"get_timer_detail"`

</details>

<a id="get_dnd_timer"></a>
### `get_dnd_timer` — Do-Not-Disturb (read)

Returns the DND window and, on newer firmware, its actions.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` — legacy fields `start_hour`, `start_minute`, `end_hour`, `end_minute`, `enabled`; newer firmware adds an
`actions` object `{"resume": 0|1, "vol": 0|1, "led": 0|1, "dust": 0|1, "dry": 0|1}` (✅ Bundle · a65 m14531).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_dnd_timer", "params": []}
```

**Legacy documentation**

⚪ Legacy [dnd_timer.md](../../dnd_timer.md).

**Related:** [`set_dnd_timer`](timers.md#set_dnd_timer), [`set_dnd_timer_actions`](timers.md#set_dnd_timer_actions)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getDndTimer`); call sites m14168, m14585; table key `GetDndTimer` · anchor `"GetDndTimer"`
- `a65@1.0.95` · wrapper m10115 (`getDndTimer`); call sites m14138, m14531; table key `GetDndTimer` · anchor `"GetDndTimer"`
- `t4@1.0.32` · wrapper m10010 (`getDndTimer`); call sites m11297, m11453; table key `GetDndTimer` · anchor `"GetDndTimer"`

</details>

<a id="set_dnd_timer"></a>
### `set_dnd_timer` — Do-Not-Disturb (set)

Sets and enables the DND window.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<start hour>, <start minute>, <end hour>, <end minute>]` (integers, 24 h).

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result[0]` (14). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Example** — constructed from app code

```json
{"id": 110, "method": "set_dnd_timer", "params": [22, 0, 8, 0]}
```

**Related:** [`close_dnd_timer`](timers.md#close_dnd_timer), [`get_dnd_timer`](timers.md#get_dnd_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setDndTimer`); call sites m14168; table key `SetDndTimer` · anchor `"SetDndTimer"`
- `a65@1.0.95` · wrapper m10115 (`setDndTimer`); call sites m14138; table key `SetDndTimer` · anchor `"SetDndTimer"`
- `t4@1.0.32` · wrapper m10010 (`setDndTimer`); call sites m11297, m11453; table key `SetDndTimer` · anchor `"SetDndTimer"`

</details>

<a id="close_dnd_timer"></a>
### `close_dnd_timer` — Do-Not-Disturb (disable)

Disables DND.

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
{"id": 1, "method": "close_dnd_timer", "params": []}
```

**Related:** [`set_dnd_timer`](timers.md#set_dnd_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`closeDndTimer`); call sites m14168; table key `CloseDndTimer` · anchor `"CloseDndTimer"`
- `a65@1.0.95` · wrapper m10115 (`closeDndTimer`); call sites m14138; table key `CloseDndTimer` · anchor `"CloseDndTimer"`
- `t4@1.0.32` · wrapper m10010 (`closeDndTimer`); call sites m11297, m11453; table key `CloseDndTimer` · anchor `"CloseDndTimer"`

</details>

<a id="set_dnd_timer_actions"></a>
### `set_dnd_timer_actions` — Do-Not-Disturb actions

Chooses what is suppressed or resumed during DND.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"resume": 0|1, "vol": 0|1, "led": 0|1, "dust": 0|1, "dry": 0|1}` (switches in the DND page).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_dnd_timer_actions", "params": {"resume": 1, "vol": 1, "led": 1, "dust": 1, "dry": 1}}
```

**Related:** [`get_dnd_timer`](timers.md#get_dnd_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setDndTimerActions`); call sites m14585 · anchor `"set_dnd_timer_actions"`
- `a65@1.0.95` · wrapper m10115 (`setDndTimerActions`); call sites m14531 · anchor `"set_dnd_timer_actions"`
- `a34@1.0.70` · wrapper m10109 (`setDndTimerActions`); call sites m14108 · anchor `"set_dnd_timer_actions"`

</details>

<a id="get_valley_electricity_timer"></a>
### `get_valley_electricity_timer` — Off-peak charging window (read)

Returns the "valley electricity" charging window.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]`: `enabled` (1 = on), `start_hour`, `start_minute` and the matching end fields.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_valley_electricity_timer", "params": []}
```

**Behaviour in the app**

Needs new-feature bit `isSupportedValleyElectricity` (high word bit 13); the status field `charge_status` and state text "wait for charge" relate to it.

**Related:** [`set_valley_electricity_timer`](timers.md#set_valley_electricity_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getValleyElectricityTimer`); call sites m14168 · anchor `"get_valley_electricity_timer"`
- `a65@1.0.95` · wrapper m10115 (`getValleyElectricityTimer`); call sites m14138 · anchor `"get_valley_electricity_timer"`
- `a62@1.0.69` · wrapper m10109 (`getValleyElectricityTimer`); call sites m13706 · anchor `"get_valley_electricity_timer"`

</details>

<a id="set_valley_electricity_timer"></a>
### `set_valley_electricity_timer` — Off-peak charging window (set)

Sets the window.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<start hour>, <start minute>, <end hour>, <end minute>]`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_valley_electricity_timer", "params": [22, 0, 8, 0]}
```

**Related:** [`close_valley_electricity_timer`](timers.md#close_valley_electricity_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setValleyElectricityTimer`); call sites m14168 · anchor `"set_valley_electricity_timer"`
- `a65@1.0.95` · wrapper m10115 (`setValleyElectricityTimer`); call sites m14138 · anchor `"set_valley_electricity_timer"`
- `a62@1.0.69` · wrapper m10109 (`setValleyElectricityTimer`); call sites m13706 · anchor `"set_valley_electricity_timer"`

</details>

<a id="close_valley_electricity_timer"></a>
### `close_valley_electricity_timer` — Off-peak charging window (disable)

Disables the window.

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
{"id": 1, "method": "close_valley_electricity_timer", "params": []}
```

**Related:** [`set_valley_electricity_timer`](timers.md#set_valley_electricity_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`closeValleyElectricityTimer`); call sites m14168 · anchor `"close_valley_electricity_timer"`
- `a65@1.0.95` · wrapper m10115 (`closeValleyElectricityTimer`); call sites m14138 · anchor `"close_valley_electricity_timer"`
- `a62@1.0.69` · wrapper m10109 (`closeValleyElectricityTimer`); call sites m13706 · anchor `"close_valley_electricity_timer"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
