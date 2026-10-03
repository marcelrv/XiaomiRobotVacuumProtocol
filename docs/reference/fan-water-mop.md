# Fan power, water flow and mop mode values

[Home](../../README.md) / Reference / Fan, water and mop

Codes used by [`set_custom_mode`](../commands/cleaning-modes.md#set_custom_mode), [`set_water_box_custom_mode`](../commands/cleaning-modes.md#set_water_box_custom_mode), [`set_mop_mode`](../commands/cleaning-modes.md#set_mop_mode) and reported in the status fields `fan_power`, `water_box_mode`, `mop_mode`. Generated from [`data/enums.json`](../../data/enums.json).

<a id="fan-power"></a>
## Fan power

Three generations of codes occur. Which one a robot uses is not selected by a command; the plugin chooses its table by model (see [device pages](../devices/index.md)).

| Generation | Code → app label | Evidence (bundles) |
|---|---|---|
| extended codes (101...) (`CleanModeMap`) | 101 → silent, 102 → balanced, 103 → turbo, 104 → Max, 105 → Gentle, 106 → Custom | 3: a01 c1 e2 |
| extended codes (101...) (`CleanModeMap`) | 101 → Silent, 102 → Balanced, 103 → Turbo, 104 → Max, 105 → Gentle, 106 → Custom | 2: a11 p5 |
| extended codes (101...) (`CleanModeMap`) | 101 → Silent, 102 → Standard, 103 → Medium, 104 → Turbo, 106 → Custom | 1: m1s |
| both families (percentage-style and 101...) (`CleanModeMap`) | 38 → silent, 60 → balanced, 75 → turbo, 100 → Max, 101 → silent, 102 → balanced, 103 → turbo, 104 → Max, 105 → Gentle, 106 → Custom | 1: s5 |
| percentage-style codes (`CleanModeMap`) | 38 → Silent, 60 → Standard, 75 → Turbo, 100 → MAX | 1: v1 |
| percentage-style codes (`CleanModeMapOld`) | 41 → Custom, 45 → silent, 50 → silent, 62 → balanced, 68 → balanced, 75 → turbo, 79 → turbo, 86 → Max, 100 → Max | 3: a01 c1 e2 |
| percentage-style codes (`CleanModeMapOld`) | 38 → Silent, 45 → Silent, 50 → Silent, 62 → Standard, 68 → Standard, 75 → Medium, 77 → Medium, 79 → Medium, 100 → Turbo | 1: m1s |
| Xiaowa/E-series table `FanModel_sapphire` | full: 100, mop: 41, power: 79, silence: 50, standard: 68 | 3: a01 c1 e2 |
| Xiaowa/E-series table `FanModel_sapphireCC` | full: 86, mop: unsupport, power: 75, silence: 45, standard: 62 | 3: a01 c1 e2 |
| Xiaowa/E-series table `FanModel_sapphire_liteC_and_liteD` | full: 104, mop: 105, power: 103, silence: 101, standard: 102 | 3: a01 c1 e2 |

### Picker presets (`CleanSettingMode`)

| Preset | Code | Present in |
|---|---:|---|
| SilentClean | 101 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| StandardClean | 102 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| StrongClean | 103 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| MaxClean | 104 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| NoClean | 105 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| MaxPlus | 108 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |

<a id="water-box-mode"></a>
## Water box mode

| Table | Code → label | Present in |
|---|---|---|
| `WaterBoxModeMap` | 204 → Custom | 3: a01 c1 e2 |
| `WaterBoxModeMap` | 200 → Off, 201 → Low, 202 → Medium, 203 → High, 204 → Custom | 3: a11 p5 s5 |
| `WaterBoxModeMap` | 201 → Low, 202 → Medium, 203 → High, 204 → Custom | 1: m1s |
| `WaterBoxModeMap` (table present, no entries) | - | 1: v1 |

### Picker presets (`WaterSettingMode`)

| Preset | Code | Present in |
|---|---:|---|
| NoWater | 200 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| LowWater | 201 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| MediumWater | 202 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| HighWater | 203 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| Custom | 207 | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |

<a id="mop-mode"></a>
## Mop mode

| Preset | Code | Present in |
|---|---:|---|
| Normal (`MopSettingMode`) | 300 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| Intensive (`MopSettingMode`) | 301 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| SlowIntensive (`MopSettingMode`) | 303 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Fast (`MopSettingMode`) | 304 | 14: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Dry (`GarnetMopMode`) | 3 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Normal (`GarnetMopMode`) | 1 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| Wet (`GarnetMopMode`) | 2 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |

<a id="mode-constants"></a>
## Mode code constants

Named constants of the app (exported by its mode-setting module); they complete the tables above: `CustomCleanMode` is the "customize" fan code, `CustomWaterMode` the "customize" water code, `CustomMopMode` the "customize" mop code.

| Constant | Code | Present in |
|---|---:|---|
| `CustomCleanMode` | 106 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| `CustomWaterMode` | 204 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| `CustomMopMode` | 302 | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| `CleanModeZero` | 105 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `WaterModeZero` | 200 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `CleanRouteDailyMode` | 300 | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |
| `CleanRouteSubtlyMode` | 301 | 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `CleanRouteDeepSlowMode` | 303 | 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `CleanRouteFastMode` | 304 | 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `CleanRouteDeepSlowPearlMode` | 305 | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |
| `CleanModeMaxPlus` | 108 | 2: a72 a73 |

## Notes

- The legacy tables ⚪ ([custom_mode.md](../../custom_mode.md), [water_box_custom_mode.md](../../water_box_custom_mode.md)) are consistent with the bundles: 101–106 extended fan codes, 200–204 and 207 water codes; new are fan code 108 (Max+), the mop "customize" code 302 and the route-mode codes 300, 301, 303, 304 and 305 ([mode code constants](#mode-constants)).
- `105` is both "Gentle" in the fan table and the "mop only" marker (`NoClean`) used by the picker; the plugin treats a fan power of 105 as a pure-mop task.
- Which codes a **firmware** accepts is not determinable from the bundles; the tables show what the app can display and send.

## See also

- [Cleaning modes commands](../commands/cleaning-modes.md)
- [Status fields](status-fields.md)
