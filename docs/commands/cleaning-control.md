# Cleaning control

[Home](../../README.md) / [Commands](index.md) / Cleaning control

Start, stop, pause and resume cleaning jobs, send the robot to a point or back to the dock, wake it up and make it announce itself.

## Conventions used on this page

- **Success** is decided by the plugin from the JSON-RPC reply: a reply with a truthy `result` other than the string
  `"unknown_method"` counts as success, anything else (an `error` object, a missing `result`) as failure
  (✅ Bundle · `RobotApi` wrapper `promiseWrap`, a65). The reply payload of the commands on this page is not evaluated;
  legacy captures show `{"result":["ok"],"id":…}` (⚪ Legacy).
- **Map coordinates** (zones, go-to) are millimetres in the robot's map frame: the app multiplies map-pixel values by 50
  and flips the y axis (see [map coordinates](../concepts/maps-overview.md#coordinates)).
- **Resuming** is not a single command: the app decides from the status field `in_cleaning` which job to resume
  ([status fields](../reference/status-fields.md#in_cleaning)).

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`app_start`](#app_start) | Starts a whole-map clean; also used to resume an interrupted global clean and to start building a new floor ma | ✅ Bundle |
| [`app_stop`](#app_stop) | Ends the running job (the robot stays where it is). | ✅ Bundle |
| [`app_pause`](#app_pause) | Pauses the running clean or spot clean so that it can be resumed. | ✅ Bundle |
| [`app_charge`](#app_charge) | Sends the robot back to the charging dock. | ✅ Bundle |
| [`app_spot`](#app_spot) | Cleans the area around the robot's current position. | ✅ Bundle |
| [`app_wakeup_robot`](#app_wakeup_robot) | Wakes a sleeping robot so that it accepts commands. | ✅ Bundle |
| [`app_zoned_clean`](#app_zoned_clean) | Cleans one or more rectangles of the map, each with its own repeat count. | ✅ Bundle |
| [`stop_zoned_clean`](#stop_zoned_clean) | Wrapped for every newer bundle; the only call site found is in the s5 bundle. | ✅ Bundle |
| [`resume_zoned_clean`](#resume_zoned_clean) | Resumes an interrupted zone clean. | ✅ Bundle |
| [`app_segment_clean`](#app_segment_clean) | Cleans the selected rooms; newer firmware also accepts repeat count, clean method and order. | ✅ Bundle |
| [`stop_segment_clean`](#stop_segment_clean) | Wrapped in all bundles; no call site found (the app uses `app_stop`). | ✅ Bundle (wrapper only) |
| [`resume_segment_clean`](#resume_segment_clean) | Resumes an interrupted room clean. | ✅ Bundle |
| [`app_goto_target`](#app_goto_target) | Sends the robot to map coordinates. | ✅ Bundle |
| [`stop_goto_target`](#stop_goto_target) | Cancels a running go-to. | ✅ Bundle |
| [`find_me`](#find_me) | Makes the robot emit a locator sound. | ✅ Bundle |
| [`start_clean`](#start_clean) | Listed in the Methods tables (`TimerStart`) of every bundle but never called by the plugin. | ✅ Bundle (declared only) |
| [`start_wash_then_charge`](#start_wash_then_charge) | Dock action offered when finishing a clean on a washing dock. | ✅ Bundle |
| [`app_start_build_map`](#app_start_build_map) | Starts a quick-mapping run ("Mapping" state 29). | ✅ Bundle |
| [`app_resume_build_map`](#app_resume_build_map) | Resumes an interrupted quick-mapping run. | ✅ Bundle |
| [`app_skip_current_cleaning_area`](#app_skip_current_cleaning_area) | Skips the room or zone that is being cleaned. | ✅ Bundle |
| [`app_start_replenish_clean_area`](#app_start_replenish_clean_area) | Sends the robot to clean extra zones that the user marked on the live map. | ✅ Bundle |

<a id="app_start"></a>
### `app_start` — Start (or resume) a global clean

Starts a whole-map clean; also used to resume an interrupted global clean and to start building a new floor map.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params` is an array with at most one object. Shapes found in the app code:

| `params` | Used for | Evidence |
|---|---|---|
| `[]` or omitted | plain start (older bundles, direct call) | ✅ Bundle: a01…a19, s4–s6, t4, t6, v1, e2, c1, m1s, p5 |
| `[{"clean_mop": <int>}]` | start / resume a global clean in bundles with the newer wrapper | ✅ Bundle: a14 and newer (`RobotApi.start`) |
| `[{"clean_mop": <int>, "map_index": [<map id>]}]` | start on a given saved floor map (multi-floor) | ✅ Bundle: a65 (m12959 `globalStartTask`) |
| `[{"use_new_map": 1}]` | start a clean that builds a new floor map (`createNewFloorMap`) | ✅ Bundle: all with wrapper; older bundles send it directly |

`clean_mop`: the main-screen start button sends `0`; the "resume mopping" alert sends `1` or `2` (mapping from the
status field `clean_mop_status`: `2 → 1`, `6 → 2`). The meaning of the values is not named at the call sites
(❓ Unknown); the map code names path types `MOPPING_TYPE_BOTH_BOTH=0`, `NONE=1`, `PURE=2`, `BOTH_IN_MOP=6`,
`BOTH_IN_CLEAN=7`, which suggests the same value space.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (a65 `globalStartTask`)

```json
{"id": 101, "method": "app_start", "params": [{"clean_mop": 0}]}
```

**Behaviour in the app**

- The app does not offer the start button when the battery is below 20 % unless the robot is already cleaning
  (toast instead; a65 m12959).
- After a successful call the app *optimistically* sets its own state to "cleaning" for a few seconds
  (`preMockState`) so that the UI does not flicker before the next status poll.
- Resuming a paused global clean calls `app_start` again; zone, room and quick-map jobs have their own resume
  commands ([`resume_zoned_clean`](#resume_zoned_clean), [`resume_segment_clean`](#resume_segment_clean),
  [`app_resume_build_map`](#app_resume_build_map)).

**Legacy documentation**

⚪ Legacy ([basic.md](../../basic.md)) documented `app_start` without parameters. The parameter forms above are new.

**Related:** [`app_pause`](cleaning-control.md#app_pause), [`app_stop`](cleaning-control.md#app_stop), [`app_charge`](cleaning-control.md#app_charge), [`app_wakeup_robot`](cleaning-control.md#app_wakeup_robot), [`app_zoned_clean`](cleaning-control.md#app_zoned_clean), [`app_segment_clean`](cleaning-control.md#app_segment_clean)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`createNewFloorMap, start`); call sites m12539, m12971, m13958, m14642; table key `AppStart` · anchor `"AppStart"`
- `a65@1.0.95` · wrapper m10115 (`createNewFloorMap, start`); call sites m12527, m12959, m13946, m14588; table key `AppStart` · anchor `"AppStart"`
- `t4@1.0.32` · wrapper m10010 (`createNewFloorMap, satrt`); call sites m10631, m11390, m11504; table key `AppStart` · anchor `"AppStart"`

</details>

<a id="app_stop"></a>
### `app_stop` — Stop the current job

Ends the running job (the robot stays where it is).

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |
| Call-site gate | the call sits behind `isMultiMapSegmentTimerSupported`, `isShowStopTaskAlert` (tests found in the enclosing code of the call sites; [feature flags](../concepts/feature-flags.md)) |

**Request**

`params`: none (`[]`).

**Response**

Reply fields the app reads (✅ Bundle; call sites whose function sends only this call, number of models in brackets): `result[0]` (4). Types and units are not stated by the code unless a field is described elsewhere on this page.

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_stop", "params": []}
```

**Behaviour in the app**

The app asks for confirmation first when the robot is running (`RSM.isRunning`). Afterwards the user normally sends
[`app_charge`](#app_charge) to send the robot home.

**Related:** [`app_pause`](cleaning-control.md#app_pause), [`app_charge`](cleaning-control.md#app_charge)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`stop`); call sites m12455, m12539, m12971, m13031, m13958; table key `AppStop` · anchor `"AppStop"`
- `a65@1.0.95` · wrapper m10115 (`stop`); call sites m12443, m12527, m12959, m13019, m13946; table key `AppStop` · anchor `"AppStop"`
- `t4@1.0.32` · wrapper m10010 (`stop`); call sites m10631; table key `AppStop` · anchor `"AppStop"`

</details>

<a id="app_pause"></a>
### `app_pause` — Pause the current job

Pauses the running clean or spot clean so that it can be resumed.

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
{"id": 1, "method": "app_pause", "params": []}
```

**Behaviour in the app**

Some bundles send this call through `callMethodForceWay` (local route); the newer wrapper sends it like every other
call. For a spot clean the app expects the robot to go to `WAITING` afterwards.

**Related:** [`app_start`](cleaning-control.md#app_start), [`app_stop`](cleaning-control.md#app_stop), [`app_charge`](cleaning-control.md#app_charge)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`pause`); call sites m12971, m14177, m14216, m14219, m14501; table key `AppPause` · anchor `"AppPause"`
- `a65@1.0.95` · wrapper m10115 (`pause`); call sites m12959, m14147, m14186, m14189, m14471; table key `AppPause` · anchor `"AppPause"`
- `t4@1.0.32` · wrapper m10010 (`pause`); call sites m10631, m11390, m11477; table key `AppPause` · anchor `"AppPause"`

</details>

<a id="app_charge"></a>
### `app_charge` — Return to the dock

Sends the robot back to the charging dock.

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
{"id": 1, "method": "app_charge", "params": []}
```

**Behaviour in the app**

After the call the app expects the state `BACK_TO_DOCK` and sets the "resume back to dock" flag (status field
`in_returning`). On docks with auto-empty the app sends [`app_start_collect_dust`](dock.md#app_start_collect_dust)
instead when the user chose "empty dust bin" (a65 m12959).
Alternate table: the `user.*` table calls the same action `user.app_home` ([alternate table](alternate-table.md#user.app_home)).

**Related:** [`app_pause`](cleaning-control.md#app_pause), [`app_stop`](cleaning-control.md#app_stop), [`start_wash_then_charge`](cleaning-control.md#start_wash_then_charge)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`charge`); call sites m12971, m14219, m14489, m14639, m14642; table key `AppCharge` · anchor `"AppCharge"`
- `a65@1.0.95` · wrapper m10115 (`charge`); call sites m12959, m14189, m14459, m14585, m14588; table key `AppCharge` · anchor `"AppCharge"`
- `t4@1.0.32` · wrapper m10010 (`charge`); call sites m10631, m11390; table key `AppCharge` · anchor `"AppCharge"`

</details>

<a id="app_spot"></a>
### `app_spot` — Spot clean

Cleans the area around the robot's current position.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`); two older bundles (s5, v1) pass an empty object.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_spot", "params": []}
```

**Related:** [`app_start`](cleaning-control.md#app_start), [`app_goto_target`](cleaning-control.md#app_goto_target)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`spot`); call sites m14177, m14219; table key `AppSpot` · anchor `"AppSpot"`
- `a65@1.0.95` · wrapper m10115 (`spot`); call sites m14147, m14189; table key `AppSpot` · anchor `"AppSpot"`
- `t4@1.0.32` · call sites m11390, m11477; table key `AppSpot` · anchor `"AppSpot"`

</details>

<a id="app_wakeup_robot"></a>
### `app_wakeup_robot` — Wake the robot from sleep

Wakes a sleeping robot so that it accepts commands.

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
{"id": 1, "method": "app_wakeup_robot", "params": []}
```

**Behaviour in the app**

In a65 two pages call it: the go-to-target page sends it when it opens (`_wakeupRobot`, m14147), and the self-clean button of the dock service sends it
first when the robot state is `SLEEPING` (code 2; m14546). The main start button (`app_start`, m12959) does not call it. Older bundles also contain call sites
(for example s5, t6, v1 through `RRMISDK.callMethod`); their pages were not traced.

**Legacy documentation**

⚪ Legacy README lists this command as "s5e only". The bundles contain a call site in all 42 bundles; whether a
firmware of another model answers it is not determinable from the bundles.

**Related:** [`app_start`](cleaning-control.md#app_start)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`appWakeupRobot`); call sites m14177, m14600; table key `AppWakeupRobot` · anchor `"AppWakeupRobot"`
- `a65@1.0.95` · wrapper m10115 (`appWakeupRobot`); call sites m14147, m14546; table key `AppWakeupRobot` · anchor `"AppWakeupRobot"`
- `t4@1.0.32` · call sites m11477; table key `AppWakeupRobot` · anchor `"AppWakeupRobot"`

</details>

<a id="app_zoned_clean"></a>
### `app_zoned_clean` — Clean rectangular zones

Cleans one or more rectangles of the map, each with its own repeat count.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params` is an array of zones; each zone is `[x1, y1, x2, y2, count]` — the rectangle corners in map
coordinates (mm, see [map coordinates](../concepts/maps-overview.md#coordinates)) and the number of passes.
The app appends `count` (1–3 selectable in the UI icons; 2 when the active mop mode id is 4) to the rectangle
computed from the map view.

For the `Garnet` product line (`DMM.isGarnet`) the whole parameter is wrapped:
`[{"clean_mop": <int>, "zones": [[x1,y1,x2,y2,count], …]}]`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (a65 m12218 `getZoneParams` + m12959)

```json
{"id": 102, "method": "app_zoned_clean", "params": [[25500, 25000, 27000, 26500, 1], [24000, 24000, 25000, 25000, 2]]}
```

**Behaviour in the app**

After the call the app sets its optimistic state to `ZONED_CLEAN` and the resume flag to "zone clean".

**Legacy documentation**

⚪ Legacy [zoned_clean.md](../../zoned_clean.md) documents the `[x1, y1, x2, y2, iter]` form — confirmed.

**Related:** [`stop_zoned_clean`](cleaning-control.md#stop_zoned_clean), [`resume_zoned_clean`](cleaning-control.md#resume_zoned_clean), [`app_segment_clean`](cleaning-control.md#app_segment_clean)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`zoneClean`); call sites m12971; table key `StartZonedClean` · anchor `"StartZonedClean"`
- `a65@1.0.95` · wrapper m10115 (`zoneClean`); call sites m12959; table key `StartZonedClean` · anchor `"StartZonedClean"`
- `t4@1.0.32` · wrapper m10010 (`zoneClean`); call sites m10631; table key `StartZonedClean` · anchor `"StartZonedClean"`

</details>

<a id="stop_zoned_clean"></a>
### `stop_zoned_clean` — Stop a zone clean

Wrapped for every newer bundle; the only call site found is in the s5 bundle.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 2: s5 v1 model(s) |
| Other bundles | wrapper only: 40: a01 a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 c1 e2 m1s p5 s4 s5e s6 t4 t6 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "stop_zoned_clean", "params": []}
```

**Behaviour in the app**

In the a65 plugin the generic [`app_stop`](#app_stop) is used for every job type; no call site of
`stop_zoned_clean` was found in the newer bundles although the wrapper `stopZoneClean` exists.

**Related:** [`app_zoned_clean`](cleaning-control.md#app_zoned_clean), [`app_stop`](cleaning-control.md#app_stop)

<details><summary>Sources</summary>

- `s5@1.0.47` · wrapper m10010,11444 (`stopZoneClean`); call sites m11447; table key `StopZonedClean` · anchor `"StopZonedClean"`
- `v1@1.0.46` · wrapper m10010 (`stopZoneClean`); call sites m11306; table key `StopZonedClean` · anchor `"StopZonedClean"`

</details>

<a id="resume_zoned_clean"></a>
### `resume_zoned_clean` — Resume a paused zone clean

Resumes an interrupted zone clean.

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
{"id": 1, "method": "resume_zoned_clean", "params": []}
```

**Behaviour in the app**

Chosen by the app when the status field `in_cleaning` is `2` and the robot is paused/sleeping/waiting/charging/in
error (a65 `RSM.isZoneCleanTaskShouldResume`).

**Related:** [`app_zoned_clean`](cleaning-control.md#app_zoned_clean), [`app_start`](cleaning-control.md#app_start)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`resumeZoneClean`); call sites m12971, m13958, m14642; table key `ResumeZonedClean` · anchor `"ResumeZonedClean"`
- `a65@1.0.95` · wrapper m10115 (`resumeZoneClean`); call sites m12959, m13946, m14588; table key `ResumeZonedClean` · anchor `"ResumeZonedClean"`
- `t4@1.0.32` · wrapper m10010 (`resumeZoneClean`); call sites m10631; table key `ResumeZonedClean` · anchor `"ResumeZonedClean"`

</details>

<a id="app_segment_clean"></a>
### `app_segment_clean` — Clean rooms (segments)

Cleans the selected rooms; newer firmware also accepts repeat count, clean method and order.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

Two shapes, selected by the plugin with the firmware feature `isSupportOrderSegmentClean` (fw feature code 114):

| Shape | When |
|---|---|
| `[id, id, …]` — room (segment) ids | firmware without feature 114 |
| `[{"clean_mop": <int>, "segments": [id, …], "repeat": <int>, "clean_order_mode": <int>}]` | firmware with feature 114 |

Room ids come from [`get_room_mapping`](rooms-and-areas.md#get_room_mapping) / the map. `repeat` is 1–3 (2 when the
mop mode id is 4); `clean_order_mode` is `1` when the user chose a custom room order, otherwise `0`
(✅ Bundle · a65 m12959 and m13001).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code

```json
{"id": 103, "method": "app_segment_clean", "params": [{"clean_mop": 0, "segments": [16, 17], "repeat": 1, "clean_order_mode": 0}]}
```

**Legacy documentation**

⚪ Legacy [segment_clean.md](../../segment_clean.md) documents both forms; `repeat` is confirmed. `clean_mop` and
`clean_order_mode` are new.

**Related:** [`get_room_mapping`](rooms-and-areas.md#get_room_mapping), [`resume_segment_clean`](cleaning-control.md#resume_segment_clean), [`stop_segment_clean`](cleaning-control.md#stop_segment_clean), [`app_zoned_clean`](cleaning-control.md#app_zoned_clean)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`segmentClean`); call sites m12971; table key `SegmentClean` · anchor `"SegmentClean"`
- `a65@1.0.95` · wrapper m10115 (`segmentClean`); call sites m12959; table key `SegmentClean` · anchor `"SegmentClean"`
- `t4@1.0.32` · wrapper m10010 (`segmentClean`); call sites m10631; table key `SegmentClean` · anchor `"SegmentClean"`

</details>

<a id="stop_segment_clean"></a>
### `stop_segment_clean` — Stop a room clean

Wrapped in all bundles; no call site found (the app uses `app_stop`).

| | |
|---|---|
| Evidence | ✅ Bundle (wrapper only) — no call site found in the bundles |
| Other bundles | wrapper only: all 42 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "stop_segment_clean", "params": []}
```

**Related:** [`app_segment_clean`](cleaning-control.md#app_segment_clean), [`app_stop`](cleaning-control.md#app_stop)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`stopSegmentClean`); table key `StopSegmentClean` · anchor `"StopSegmentClean"`
- `a65@1.0.95` · wrapper m10115 (`stopSegmentClean`); table key `StopSegmentClean` · anchor `"StopSegmentClean"`
- `t4@1.0.32` · wrapper m10010 (`stopSegmentClean`); table key `StopSegmentClean` · anchor `"StopSegmentClean"`

</details>

<a id="resume_segment_clean"></a>
### `resume_segment_clean` — Resume a paused room clean

Resumes an interrupted room clean.

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
{"id": 1, "method": "resume_segment_clean", "params": []}
```

**Behaviour in the app**

Chosen when `in_cleaning` is `3` and the robot is in a resumable state (a65 `isSegmentCleanTaskShouldResume`).

**Related:** [`app_segment_clean`](cleaning-control.md#app_segment_clean)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`resumeSegmentClean`); call sites m12971, m13958, m14642; table key `ResumeSegmentClean` · anchor `"ResumeSegmentClean"`
- `a65@1.0.95` · wrapper m10115 (`resumeSegmentClean`); call sites m12959, m13946, m14588; table key `ResumeSegmentClean` · anchor `"ResumeSegmentClean"`
- `t4@1.0.32` · wrapper m10010 (`resumeSegmentClean`); call sites m10631; table key `ResumeSegmentClean` · anchor `"ResumeSegmentClean"`

</details>

<a id="app_goto_target"></a>
### `app_goto_target` — Go to a point

Sends the robot to map coordinates.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params` is `[x, y]`, map coordinates in millimetres (map-view position × 50, y axis flipped; a65 m12218
`getGotoTarget`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code

```json
{"id": 104, "method": "app_goto_target", "params": [25500, 25000]}
```

**Behaviour in the app**

The app first waits until the robot state is not `LOCKED` (103, saving map). While the robot goes, the state is
`GOTO_TARGET` (16). [`stop_goto_target`](#stop_goto_target) cancels it.

**Legacy documentation**

⚪ Legacy [goto_target.md](../../goto_target.md) — confirmed. The README lists the command as "v1, s5, s6, s5e";
call sites exist in all 42 bundles.

**Related:** [`stop_goto_target`](cleaning-control.md#stop_goto_target), [`app_spot`](cleaning-control.md#app_spot)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`gotoTarget`); call sites m14177, m14702; table key `GotoTarget` · anchor `"GotoTarget"`
- `a65@1.0.95` · wrapper m10115 (`gotoTarget`); call sites m14147, m14648; table key `GotoTarget` · anchor `"GotoTarget"`
- `t4@1.0.32` · call sites m11477; table key `GotoTarget` · anchor `"GotoTarget"`

</details>

<a id="stop_goto_target"></a>
### `stop_goto_target` — Cancel go-to

Cancels a running go-to.

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
{"id": 1, "method": "stop_goto_target", "params": []}
```

**Related:** [`app_goto_target`](cleaning-control.md#app_goto_target)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`gotoTargetStop`); call sites m14177, m14639; table key `GotoTargetStop` · anchor `"GotoTargetStop"`
- `a65@1.0.95` · wrapper m10115 (`gotoTargetStop`); call sites m14147, m14585; table key `GotoTargetStop` · anchor `"GotoTargetStop"`
- `t4@1.0.32` · call sites m11477; table key `GotoTargetStop` · anchor `"GotoTargetStop"`

</details>

<a id="find_me"></a>
### `find_me` — Locate the robot (play a sound)

Makes the robot emit a locator sound.

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
{"id": 1, "method": "find_me", "params": []}
```

**Behaviour in the app**

The app debounces the button (ignores presses for 1 s) and shows a toast. A test routine in the plugin also calls it.

**Legacy documentation**

⚪ Legacy [find_me.md](../../find_me.md) — confirmed. Region gating: the plugin's `isFindMeSupported` is true for
some products everywhere and for others only outside the US/DE (FCC/CE) locations
([feature flags](../concepts/feature-flags.md)).

**Related:** [`app_wakeup_robot`](cleaning-control.md#app_wakeup_robot)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`findMe`); call sites m14168, m14405; table key `FindMe` · anchor `"FindMe"`
- `a65@1.0.95` · wrapper m10115 (`findMe`); call sites m14138, m14375; table key `FindMe` · anchor `"FindMe"`
- `t4@1.0.32` · wrapper m10010 (`findMe`); call sites m11246; table key `FindMe` · anchor `"FindMe"`

</details>

<a id="start_clean"></a>
### `start_clean` — Timer start (declared only)

Listed in the Methods tables (`TimerStart`) of every bundle but never called by the plugin.

| | |
|---|---|
| Evidence | ✅ Bundle (declared only) — no call site found in the bundles |
| Other bundles | declared only: all 42 |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

❓ Unknown — no call site in any bundle.

**Response**

Not applicable: no analysed plugin has a call site for this method (only a wrapper or a table entry), so no reply handling exists in the bundles (❓ Unknown).

**Related:** [`set_timer`](timers.md#set_timer)

<details><summary>Sources</summary>

- `a74@1.0.96` · table key `TimerStart` · anchor `"TimerStart"`
- `a65@1.0.95` · table key `TimerStart` · anchor `"TimerStart"`
- `t4@1.0.32` · table key `TimerStart` · anchor `"TimerStart"`

</details>

<a id="start_wash_then_charge"></a>
### `start_wash_then_charge` — Wash the mop, then return to the dock

Dock action offered when finishing a clean on a washing dock.

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
{"id": 1, "method": "start_wash_then_charge", "params": []}
```

**Behaviour in the app**

Offered in the "back to dock" menu as the action `washThenCharge` (a65 m12959), gated by the firmware new-feature
bit `isWashThenChargeCmdSupported` (high word bit 5).

**Related:** [`app_charge`](cleaning-control.md#app_charge), [`app_start_wash`](dock.md#app_start_wash)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`startWashThenCharge`); call sites m12971 · anchor `"start_wash_then_charge"`
- `a65@1.0.95` · wrapper m10115 (`startWashThenCharge`); call sites m12959 · anchor `"start_wash_then_charge"`
- `a62@1.0.69` · wrapper m10109 (`startWashThenCharge`); call sites m12515 · anchor `"start_wash_then_charge"`

</details>

<a id="app_start_build_map"></a>
### `app_start_build_map` — Quick map building

Starts a quick-mapping run ("Mapping" state 29).

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
{"id": 1, "method": "app_start_build_map", "params": []}
```

**Behaviour in the app**

Gated by the new-feature bit `isSupportQuickMapBuilder` (high word bit 7). While running, the robot state is 29.

**Related:** [`app_resume_build_map`](cleaning-control.md#app_resume_build_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`quickCreateMap`); call sites m12539 · anchor `"app_start_build_map"`
- `a65@1.0.95` · wrapper m10115 (`quickCreateMap`); call sites m12527 · anchor `"app_start_build_map"`
- `a62@1.0.69` · wrapper m10109 (`quickCreateMap`); call sites m13418 · anchor `"app_start_build_map"`

</details>

<a id="app_resume_build_map"></a>
### `app_resume_build_map` — Resume quick map building

Resumes an interrupted quick-mapping run.

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
{"id": 1, "method": "app_resume_build_map", "params": []}
```

**Behaviour in the app**

Chosen when `in_cleaning` is `4` (CleanResumeFlag `Quick_Build_Map`).

**Related:** [`app_start_build_map`](cleaning-control.md#app_start_build_map)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`resumeQuickBuildMap`); call sites m12971 · anchor `"app_resume_build_map"`
- `a65@1.0.95` · wrapper m10115 (`resumeQuickBuildMap`); call sites m12959 · anchor `"app_resume_build_map"`
- `a62@1.0.69` · wrapper m10109 (`resumeQuickBuildMap`); call sites m12515 · anchor `"app_resume_build_map"`

</details>

<a id="app_skip_current_cleaning_area"></a>
### `app_skip_current_cleaning_area` — Skip the current area

Skips the room or zone that is being cleaned.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |
| Call-site gate | the call sits behind `isDynamiclySkipCleanZoneSupported` (tests found in the enclosing code of the call sites; [feature flags](../concepts/feature-flags.md)) |

**Request**

`params`: object `{"source": 2}` (always `2` in the app).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "app_skip_current_cleaning_area", "params": {"source": 2}}
```

**Related:** [`app_start_replenish_clean_area`](cleaning-control.md#app_start_replenish_clean_area)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`skipCurrentCleaningArea`); call sites m12971 · anchor `"app_skip_current_cleaning_area"`
- `a65@1.0.95` · wrapper m10115 (`skipCurrentCleaningArea`); call sites m12959 · anchor `"app_skip_current_cleaning_area"`
- `a51@1.0.83` · wrapper m10115 (`skipCurrentCleaningArea`); call sites m12938 · anchor `"app_skip_current_cleaning_area"`

</details>

<a id="app_start_replenish_clean_area"></a>
### `app_start_replenish_clean_area` — Clean supplementary zones

Sends the robot to clean extra zones that the user marked on the live map.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 10: a26 a27 a46 a64 a65 a66 a72 a73 a74 a75 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |
| Call-site gate | the call sits behind `isDynamiclyAddCleanZonesSupported` (tests found in the enclosing code of the call sites; [feature flags](../concepts/feature-flags.md)) |

**Request**

`params`: `{"zones": <zones>, "source": 2}` in a65, a72, a73; no parameters in a27 and a75.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`app_skip_current_cleaning_area`](cleaning-control.md#app_skip_current_cleaning_area)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`gotoCleanSupplementZones`); call sites m12971 · anchor `"app_start_replenish_clean_area"`
- `a65@1.0.95` · wrapper m10115 (`gotoCleanSupplementZones`); call sites m12959 · anchor `"app_start_replenish_clean_area"`
- `a26@1.0.84` · wrapper m10115 (`gotoCleanSupplementZones`); call sites m12956 · anchor `"app_start_replenish_clean_area"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
