# Status fields

[Home](../../README.md) / Reference / Status fields

The object returned as `result[0]` of `get_prop ["get_status"]` ([`get_prop`](../commands/status.md#get_prop)). The table lists the fields that the plugin's status parser reads, their interpretation (read from the app code) and in how many of the 42 analysed bundles the parser reads them. A field that is not read by a bundle may still be sent by the robot. Presence columns are generated from [`data/status_fields.json`](../../data/status_fields.json); the interpretation is curated in `tools/curated/status_fields.yaml`.

## Core state

| Field | Type | Meaning (from the app code) | Read by | Evidence |
|---|---|---|---|---|
| `state` | int | Robot state code. The app reads it in `getComputedState` / `parseRobotMotionStatus` (newer bundles) or `parseStatus` (older). Derived "computed states" are described in [states](states.md#computed-states). | 42 / 42 | a65 m10010 |
| `battery` | int | Battery percent (`parseInt`). With `state == 8` and `battery == 100` the app shows state 100 "Fully charged". | 42 / 42 | a65 m10010 |
| `error_code` | int | Error code ([errors](errors.md)). Newer bundles use `error_code` or, when it is absent, `dock_error_status`. | 42 / 42 | a65 m10010 |
| `dock_error_status` | int | Dock error code (> 0 while a dock error is active); used as `errorCode` when `error_code` is absent and also kept separately. | 22 / 42 | a65 m10010 |
| <a id="in_cleaning"></a>`in_cleaning` | int | Which job is unfinished: 0 none, 1 global, 2 zone, 3 room (segment), 4 quick map building (`CleanResumeFlagCodeMap`). Decides which resume command the app sends. | 42 / 42 | a65 m10010 |
| `in_returning` | int | `1` = a "return to dock" task is pending (resume flag `Has`). | 42 / 42 | a65 m10010 |
| `in_fresh_state` | int | The app stores `isRunning = (in_fresh_state != 1)`. | 42 / 42 | a65 m10010 |
| `lock_status` | int | `1` makes the app show state 103 (locked / saving map) regardless of `state`. | 42 / 42 | a65 m10010 getComputedState |
| `clean_mop_status` | int | Mop phase of a clean: `1` vacuum only (or absent), `2` mop only, `7` vacuum+mop (vacuum phase), `6` vacuum+mop (mop phase); drives computed states 6301–6310. | 32 / 42 | a65 m10010 getComputedState |
| `back_type` | int | `1` with `state == 6` means "going back to wash the mop" (computed state 6310). | 22 / 42 | a65 m10010 |
| `clean_area` | int | Area of the current clean in mm² (the app converts with `fromSqmmToSqm`). | 42 / 42 | a65 m10010 |
| `clean_time` | int | Duration of the current clean in seconds (converted to minutes). | 42 / 42 | a65 m10010 |
| `clean_percent` | int | Progress percentage of the current clean (stored as `cleanProgress`). | 16 / 42 | a65 m10010 |
| `last_clean_t` | int | Unix time of the last clean; the app computes hours since then (used for the 72-hour mop warning). | 13 / 42 | a65 m10010 |
| `msg_ver` | int | Message version of the firmware. Read outside the status parser by the remote-control page, which refuses to start when the value is missing or below 1 (it shows the string `RemoteControlPage_54`), and by a settings page that compares it with the constant `FIRMWARE_VER_REQUIRE` (1) and disables its slider and buttons below it. Identifier scan: present in a01 a11 c1 e2 m1s p5 s5 t4 t6 v1. | other pages (10 bundles) | v1 (remote-control page, settings page) |
| `common_status` | int | Bit mask; bit 0 set (or the field absent) allows the "special logic" of the charging-resume reminders (`isSpecialLogicAllowed`). | status parser (newer bundles) | a65 m10010 |

## Fan, water and mop

| Field | Type | Meaning (from the app code) | Read by | Evidence |
|---|---|---|---|---|
| `fan_power` | int | Fan power code ([fan values](fan-water-mop.md#fan-power)); the app falls back to 102 when the value is unknown. | 42 / 42 | a65 m10010 |
| `water_box_mode` | int | Water mode code ([water values](fan-water-mop.md#water-box-mode)). | 41 / 42 | a65 m10010 |
| `mop_mode` | int | Mop route code ([mop values](fan-water-mop.md#mop-mode)). | 32 / 42 | a65 m10010 |
| `mop_template_id` | int | Id of the active custom mop template. | 22 / 42 | a65 m10010 |
| `distance_off` | int | Fine water level (used with water mode 207); `0` when absent. | 22 / 42 | a65 m10010 |
| `water_box_status` | int | `1` = water tank attached. | 42 / 42 | a65 m10010 |
| `water_box_carriage_status` | int | `1` = mop carriage attached. | 41 / 42 | a65 m10010 |
| `mop_forbidden_enable` | int | `1` = no-mop zones enabled. | 41 / 42 | a65 m10010 |
| `water_shortage_status` | int | Water shortage indicator (value kept as integer; the reminder "mop stopped" is derived from it). | 32 / 42 | a65 m10010 |
| `corner_clean_mode` | int | Truthy = corner clean on. | 10 / 42 | a65 m10010 |

## Maps

| Field | Type | Meaning (from the app code) | Read by | Evidence |
|---|---|---|---|---|
| <a id="map_status"></a>`map_status` | int | Bit-packed: `code % 4` = map status (0 none, 1 map without rooms, 3 map with rooms); `code >> 2` = id of the loaded saved map (63 is mapped to -1). While `is_locating` the id is -1. | 42 / 42 | a65 m10010 |
| `lab_status` | int | `1` map saving on; `3` map saving + multi-floor on. | 42 / 42 | a65 m10010 |
| `is_locating` | int | Truthy while the robot is relocating. | 34 / 42 | a65 m10010 |
| `switch_map_mode` | int | Automatic map switching mode (see [`set_switch_map_mode`](../commands/maps.md#set_switch_map_mode)). | 22 / 42 | a65 m10010 |
| `unsave_map_reason` | int | Why the last map was not saved ([`UnsaveMapReason`](other-enums.md#unsavemapreason)). | 22 / 42 | a65 m10010 |
| `unsave_map_flag` | int | Pending handling of an unsaved map ([`UnsaveMapHandle`](other-enums.md#unsavemaphandle)). | 22 / 42 | a65 m10010 |
| `sfzs` | int | `1` = the clean uses the extra "supplement" zones (`isCleanFBZEnabled`). | 22 / 42 | a65 m10010 |
| `replenish_mode` | int | Supplementary clean status (`supplementCleanStatus`). | 2 / 42 | a65 m10010 |
| `is_exploring` | int | `1` = exploration run. | 34 / 42 | a65 m10010 |

## Switch words

| Field | Type | Meaning (from the app code) | Read by | Evidence |
|---|---|---|---|---|
| `switch_status` | int | Bit mask: bit 0 offline map on; bit 1 cleaning-fluid module present (also `clean_fluid == 1`); bit 3 "carpet first" on. | 16 / 42 | a65 m10010 |
| `dss` | int | Dock supply status, 2-bit groups: bits 0–1 water level up/down ready (`== 2`), bits 2–3 clean water box, 4–5 dirty water box, 6–7 dust bag, 8–9 water-box filter, 10–11 cleaning fluid. The meaning of the 2-bit values is not named in the code. | 13 / 42 | a65 m10010 |
| `wash_status` | int | Low byte = washing task status; bits ≥ 8 = washing mode. | 13 / 42 | a65 m10010 |
| `wash_ready` | int | `1` = dock ready to wash. | 22 / 42 | a65 m10010 |
| `dock_type` | int | Dock type code ([dock reference](dock.md)). | 32 / 42 | a65 m10010 |
| `auto_dust_collection` | int | `0` = automatic emptying off. | 25 / 42 | a65 m10010 |
| `dry_status` | int | With `state == 8` (charging): `1` = mop drying in progress. | 17 / 42 | a65 getComputedState |
| `charge_status` | int | With valley-electricity support: `0` while charging is paused ("waiting for charge"). | 22 / 42 | a65 getComputedState |
| `stop_fan_motor_work_status` | int | With `state == 15` (docking): `1` = stopping air-drying (computed state 202). | 22 / 42 | a65 getComputedState |
| `fan_motor_work_status` | int | `1` while charging = air-drying running. | 5 / 42 | a65 m10010 |
| `fan_motor_work_time` | int | Remaining air-dry time (shown in a special info banner). | 5 / 42 | a65 m10010 |
| `rdt` | int | Remaining dry time (`dryRemainTime`). | 17 / 42 | a65 m10010 |
| `clean_fluid` | int | `1` = cleaning-fluid module present. | 13 / 42 | a65 m10010 |
| `dnd_enabled` | int | `1` = Do-Not-Disturb enabled. | 42 / 42 | a65 m10010 |
| `debug_mode` | int | `1` = Wi-Fi debug mode. | 25 / 42 | a65 m10010 |
| `in_warmup` | int | `1` = robot warming up. | 22 / 42 | a65 m10010 |
| `voice_chat_status` | int | `1` = voice chat active (state 28). | 22 / 42 | a65 m10010 |
| `avoid_count` | int | Number of avoided obstacles (stored as `avoidCount`). | 25 / 42 | a65 m10010 |
| `kct` | int | Keep-clean time (`keepCleanTime`), 0 when absent. | 2 / 42 | a65 m10010 |
| `adbumper_status` | int[3] | Three bumper sensor bytes (left, middle, right): bit 7 = bumper pressed; bits 1, 3, 4, 6 = obstacle sensed. | 32 / 42 | a65 m10010 |
| `events` | array | Event list processed by `parseEvents`; the event layout is not described here (❓ Unknown). | 29 / 42 | a65 m10010 |

## Monitoring

| Field | Type | Meaning (from the app code) | Read by | Evidence |
|---|---|---|---|---|
| `camera_status` | int | Same bit field as [`get_camera_status`](../commands/camera.md#get_camera_status). | 34 / 42 | a65 m10010 + m12998 |
| `home_sec_status` | int | Monitoring connection state (`RRHomeSecStatus`: 0 disconnected, 1 connected, 2 disconnecting). | 34 / 42 | a65 m10010 |
| `home_sec_enable_password` | int | `1` = monitoring password enabled. | 34 / 42 | a65 m10010 |
| `home_sec_client_id` | string | Client id of the monitoring session (one bundle). | 1 / 42 |  |

## Other fields read by the parser

`return_roller_status`

## Legacy-only fields

Fields documented by the pre-existing repo text that **no** bundle reads: `msg_seq`, `clean_mode`, `begin_time`, `clean_trigger`, `back_trigger`, `clean_strategy`, `map_present`. They may still be returned by firmware; the bundles say nothing about them (⚪ Legacy).

## Decoding notes

- `map_status`: `value % 4` = 0 no map, 1 map without rooms, 3 map with rooms; `value >> 2` = saved-map id; id 63 is treated as "none".
- Truthiness: the plugin often uses `!!status.x` or `== 1`; treat anything non-zero as on only where the table says so.
- Units: `clean_area` mm², `clean_time` s, `battery` %. The `fan_power` code families are in [fan, water and mop values](fan-water-mop.md).

## See also

- [States](states.md)
- [Errors](errors.md)
- [Command: get_prop](../commands/status.md#get_prop)
