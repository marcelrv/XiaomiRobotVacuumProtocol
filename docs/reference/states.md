# Robot state codes

[Home](../../README.md) / Reference / State codes

The `state` field of the status object ([status fields](status-fields.md)) and the app's own wording for each code. English strings are the plugin's own (`en_strings`); where several wordings occur the newest bundle is shown first. Generated from [`data/enums.json`](../../data/enums.json).

| Code | Origin | App constant | English wording (newest bundle) | Other wording | Present in |
|---:|---|---|---|---|---|
| 0 | `state` | `UNKNOWN` | Getting Info | Acquiring status; Getting info | all 42 |
| 1 | `state` | `INITIAL` | Cleaning | Clean up | all 42 |
| 2 | `state` | `SLEEPING` | Sleeping | Sleep | all 42 |
| 3 | `state` | `WAITING` | Ready | Waiting for instructions | all 42 |
| 5 | `state` | `CLEAN` | Cleaning | Clean up | all 42 |
| 6 | `state` | `BACK_TO_DOCK` | Returning to Dock | Docking; Recharging; Returning to dock to charge | all 42 |
| 7 | `state` | `REMOTE` | Remote Controlling | Remote Control; Remote control; Using remote control | all 42 |
| 8 | `state` | `CHARGING` | Charging |  | all 42 |
| 9 | `state` | `CHARGE_ERROR` | Charging Error | Charging error | all 42 |
| 10 | `state` | `PAUSE` | Pause |  | all 42 |
| 11 | `state` | `SPOT_CLEAN` | Spot Clean | Spot cleaning; Spot cleanup | all 42 |
| 12 | `state` | `MALFUNCTIONING` | Error | Report an error | all 42 |
| 13 | `state` | `PREPARE_SHUTDOWN` | Powering off | Powering Off; Prepare to turn off; Turning off | 17: a01 a08 a09 a10 a11 a19 c1 e2 m1s p5 s4 s5 s5e s6 t4 t6 v1 |
| 14 | `state` | `UPDATING` | Updating |  | all 42 |
| 15 | `state` | `RUB_TO_DOCK` | Returning to Dock | Docking; Recharging; Returning to dock to charge | all 42 |
| 16 | `state` | `GOTO_TARGET` | Going to the target point | Going to the target | all 42 |
| 17 | `state` | `ZONED_CLEAN` | Zone cleaning | Zone clean; Zone cleanup; Zoned cleanup | all 42 |
| 18 | `state` | `SEGMENT_CLEAN` | Room Cleaning | Room clean; Room cleanup | all 42 |
| 22 | `state` | `COLLECTING_DUST` | Emptying | Emptying Dustbin | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 23 | `state` | `WASHING_DUSTER` | Washing the mop | Washing the cloth | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 25 | `state` | `WASHING_DUSTER` | Washing the mop |  | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 26 | `state` | `BACK_TO_DOCK_WASHING_DUSTER` | Going to wash the mop |  | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 28 | `state` | `VOICE_CHATTING` | In call… |  | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 29 | `state` | `QUICK_BUILDING_MAP` | Mapping |  | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 30 | `state` | `EGG_ATTACK` | scanning |  | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 100 | computed | `FULL_CHARGE` | Charged | Charging completed; Full charged; Fully Charged; Fully charged | all 42 |
| 101 | display table only | `OFF_LINE` | Offline |  | all 42 |
| 102 | display table only | `UNKNOW` | Unknow status. Update plug-in | Status unknown. Update plug-ins; Unknown status, please update plug-ins | all 42 |
| 103 | computed | `LOCKED` | Saving Map | Map saving; Saving map; The map is being saved | all 42 |
| 202 | computed | `AIR_DRYING_STOPPING` | Stopping air-drying |  | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 6301 | computed | `MOPPING` | Washing | Mopping | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 6302 | computed | `CLEAN_MOP_CLEANING` | Cleaning | Cleaning (vacuum + mop) | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 6303 | computed | `CLEAN_MOP_MOPPING` | Washing | Mopping (vacuum + mop) | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 6304 | computed | `SEGMENT_MOPPING` | Room Washing | Room mop | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 6305 | computed | `SEGMENT_CLEAN_MOP_CLEANING` | Room Cleaning | Cleaning selective room (vacuum + mop) | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 6306 | computed | `SEGMENT_CLEAN_MOP_MOPPING` | Room Washing | Mopping selective room (vacuum + mop) | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 6307 | computed | `ZONED_MOPPING` | Zone Washing | Zone mop | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 6308 | computed | `ZONED_CLEAN_MOP_CLEANING` | Zone cleaning | Zone cleaning (vacuum + mop) | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 6309 | computed | `ZONED_CLEAN_MOP_MOPPING` | Zone Washing | Zone mopping (vacuum + mop) | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 6310 | computed | `BACK_TO_DOCK_WASHING_DUSTER` | Going to wash the mop | Returning to dock to wash the cloth | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |

Origin: `state` = decoded from the status field `state`; computed = derived by the app from other fields (next section); display table only = an entry of the display map for which this analysis found no code path that assigns it (101 `OFF_LINE`, 102 `UNKNOW`, whose constant is not defined in the app's state enumeration). Codes 23 and 25 both map to the constant `WASHING_DUSTER`; the app uses different strings for them in different plugin generations.

## Computed states

Newer plugins do not show the raw firmware code for some situations; they compute a display state from several status fields (✅ Bundle · a65 m10010 `getComputedState`). These codes can therefore **not** be read from the `state` field:

| Computed code | Condition |
|---:|---|
| 100 | `state == 8` (charging) and `battery == 100` |
| 103 | `lock_status == 1` |
| 202 | `state == 15` and `stop_fan_motor_work_status == 1` (stopping air-drying) |
| 6 | `state == 15` otherwise (docking is shown as "returning to dock") |
| 6310 | `state == 6` and `back_type == 1` (going to wash the mop) |
| 6301 / 6302 / 6303 | `state == 5` with `clean_mop_status` 2 (mop only) / 7 / 6 |
| 6304 / 6305 / 6306 | `state == 18` (room clean) with `clean_mop_status` 2 / 7 / 6 |
| 6307 / 6308 / 6309 | `state == 17` (zone clean) with `clean_mop_status` 2 / 7 / 6 |

A "wait for charge" label replaces the text of state 8 when valley-electricity charging is waiting (`charge_status == 0`).

## Groupings used by the app

| Predicate | States |
|---|---|
| cleaning | 5, 17, 18, 11 |
| ready for a new clean | 2, 3, 10 or charging (8, 100) and no unfinished job |
| resumable | 10, 2, 3, 12 or a back-to-dock task or charging |
| on dock | 8, 100, 14, 22, 23 |
| in a back-to-dock task | 6, 26, 22 or drying |

(a65 m10010 `isCleaning`, `isReadyToNewClean`, `isReadyForCleanTaskResume`, `isOnDock`, `isInBackDockTask`.)

## Differences from the legacy table

⚪ Legacy [status.md](../../status.md) lists codes 0-18 and 100. Codes 0-3, 5-18 and 100 occur in the bundles' display map (13 only in the 17 older bundles). Code 4 ("Remote Control" in the legacy table and in 🔶 openHAB) is **not** in the display map; the display map uses **7** for remote control (openHAB: 7 = "Manual Mode"). The app itself contains two disagreeing tables: its `RobotStateCode` constants list `REMOTE: 4` and `SEARCH_FOR_DOCK: 7` (a65 m12515), while the display map used for the status text maps 7 to the remote-control string. This looks like a renumbering inside the app; it does not prove that firmware never reports 4. The bundles add 22, 23, 25, 26, 28, 29, 30, 101, 102, 103, 202 and the computed 6301-6310.

## See also

- [Status fields](status-fields.md)
- [Errors](errors.md)
- [Status command](../commands/status.md)
