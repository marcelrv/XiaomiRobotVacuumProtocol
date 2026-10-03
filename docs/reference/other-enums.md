# Other enumerations decoded by the app

[Home](../../README.md) / Reference / Other enumerations

Small tables found in the bundles (located by their key set, so they are present even in minified bundles). Generated from [`data/enums.json`](../../data/enums.json).

<a id="backwashmode"></a>
## `BackWashMode`

back-wash (mid-clean mop washing) modes.

| Name | Value | Present in |
|---|---|---|
| `BackWashModeSmart` | 0 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `BackWashModeCustom` | 1 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `BackWashModeLevel` | 2 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |

<a id="carpetcleanmode"></a>
## `CarpetCleanMode`

carpet handling modes (set_carpet_clean_mode).

| Name | Value | Present in |
|---|---|---|
| `CarpetDynamicAdaptionMode` | 3 | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |
| `CarpetIgnoreMode` | 2 | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |
| `CarpetSelfAdaptionMode` | 1 | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |
| `CarpetAvoidMode` | 0 | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |

<a id="docktype"></a>
## `DockType`

dock type classes seen by the app.

| Name | Value | Present in |
|---|---|---|
| `Other` | -1 | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |
| `Normal` | 0 | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |

<a id="dustcollectionmode"></a>
## `DustCollectionMode`

auto-empty (dust collection) modes.

| Name | Value | Present in |
|---|---|---|
| `DustCollectionModeSmart` | 0 | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `DustCollectionModeQuick` | 1 | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `DustCollectionModeDaily` | 2 | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `DustCollectionModeStrong` | 3 | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `DustCollectionModeMax` | 4 | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |

<a id="incleaningstatus"></a>
## `InCleaningStatus`

values of the in_cleaning status field.

| Name | Value | Present in |
|---|---|---|
| `COMPLETE` | 0 | all 42 |
| `GLOBAL_CLEAN_NOT_COMPLETE` | 1 | all 42 |
| `ZONE_CLEAN_NOT_COMPLETE` | 2 | all 42 |
| `SEGMENT_CLEAN_NOT_COMPLETE` | 3 | all 42 |

<a id="loglevel"></a>
## `LogLevel`

log upload levels (enable_log_upload).

| Name | Value | Present in |
|---|---|---|
| `None` | 0 | all 42 |
| `BlackBox` | 1 | all 42 |
| `Pickup` | 2 | all 42 |
| `Full` | 4 | all 42 |

<a id="modeconstants"></a>
## `ModeConstants`

mode code constants of the app (custom fan / water / mop modes, route modes).

| Name | Value | Present in |
|---|---|---|
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

<a id="moppingtype"></a>
## `MoppingType`

mopping type of a clean task.

| Name | Value | Present in |
|---|---|---|
| `MOPPING_TYPE_NONE` | 1 | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `MOPPING_TYPE_PURE` | 2 | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `MOPPING_TYPE_BOTH_IN_CLEAN` | 7 | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `MOPPING_TYPE_BOTH_IN_MOP` | 6 | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `MOPPING_TYPE_BOTH_BOTH` | 0 | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |

<a id="operatorcode"></a>
## `OperatorCode`

operator codes.

| Name | Value | Present in |
|---|---|---|
| `OPERATOR_NONE` | 0 | all 42 |
| `OPERATOR_CN` | 1 | all 42 |
| `OPERATOR_NOT_CN` | 2 | all 42 |

<a id="privacyname"></a>
## `privacyName`

privacy policy region codes sent with enable_log_upload.

| Name | Value | Present in |
|---|---|---|
| `PN_NONE` | 0 | all 42 |
| `PN_CN` | 1 | all 42 |
| `PN_GENERAL` | 2 | all 42 |
| `PN_EU` | 3 | all 42 |
| `PN_MAX` | 4 | all 42 |

<a id="repeatmode"></a>
## `RepeatMode`

timer repeat modes (UI).

| Name | Value | Present in |
|---|---|---|
| `Once` | Once | all 42 |
| `Once` | 0 | all 42 |
| `Once` | 0000000 | all 42 |
| `Everyday` | Everyday | all 42 |
| `Everyday` | 1 | all 42 |
| `Everyday` | 1111111 | all 42 |
| `Weekdays` | Weekdays | all 42 |
| `Weekdays` | 2 | all 42 |
| `Weekdays` | 0111110 | all 42 |
| `Weekends` | Weekends | all 42 |
| `Weekends` | 3 | all 42 |
| `Weekends` | 1000001 | all 42 |

<a id="rrhomesecstatus"></a>
## `RRHomeSecStatus`

home-security (camera) connection status.

| Name | Value | Present in |
|---|---|---|
| `RRHomeSecStatusDisconnected` | 0 | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| `RRHomeSecStatusConnected` | 1 | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| `RRHomeSecStatusDisconnecting` | 2 | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |

<a id="specialinfotype"></a>
## `SpecialInfoType`

special info banner types shown on the main screen.

| Name | Value | Present in |
|---|---|---|
| `Timer` | 1 | 17: a26 a27 a29 a30 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `DryRemainTime` | 2 | 17: a26 a27 a29 a30 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `PureClean` | 3 | 17: a26 a27 a29 a30 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `PureMop` | 4 | 17: a26 a27 a29 a30 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `WaitCharge` | 5 | 17: a26 a27 a29 a30 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `UnsaveMapReason` | 6 | 17: a26 a27 a29 a30 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `HasNewMap` | 7 | 17: a26 a27 a29 a30 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `CleanMopWithCleanRouteFast` | 8 | 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |

<a id="unsavemaphandle"></a>
## `UnsaveMapHandle`

handling of an unsaved map.

| Name | Value | Present in |
|---|---|---|
| `Ignore` | 0 | 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `Update` | 1 | 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `Load` | 2 | 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `Done` | 3 | 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |

<a id="unsavemapreason"></a>
## `UnsaveMapReason`

reasons why a map was not saved.

| Name | Value | Present in |
|---|---|---|
| `Saved` | 0 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `ChargerOffset` | 1 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `Relocation` | 2 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `ReachMaxFloorCount` | 3 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `Unfinished` | 4 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `DidNotStartFromCharger` | 5 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `DidNotReturnToCharger` | 6 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `MapSaveNoOpen` | 7 | 10: a26 a27 a46 a64 a65 a66 a72 a73 a74 a75 |
| `MapMess` | 8 | 10: a26 a27 a46 a64 a65 a66 a72 a73 a74 a75 |

<a id="washtowelmode"></a>
## `WashTowelMode`

mop washing modes of the dock (set_wash_towel_mode).

| Name | Value | Present in |
|---|---|---|
| `WashTowelModeQuick` | 0 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `WashTowelModeDaily` | 1 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `WashTowelModeDeep` | 2 | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `WashTowelModeSuperDeep` | 8 | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |

<a id="mapstatuscodemap"></a>
## `MapStatusCodeMap`

| Code | Meaning | Present in |
|---:|---|---|
| 0 | `None` | all 42 |
| 1 | `Has_WithoutSegments` | all 42 |
| 3 | `Has_WithSegments` | all 42 |

<a id="cleanresumeflagcodemap"></a>
## `CleanResumeFlagCodeMap` (value of `in_cleaning`)

| Code:meaning | Present in |
|---|---|
| `0:None` | all 42 |
| `1:Global_Clean` | all 42 |
| `2:Zone_Clean` | all 42 |
| `3:Segment_Clean` | all 42 |
| `4:Quick_Build_Map` | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |

<a id="cleanstarttype"></a>
## Clean record start types (`start_type`)

App wording (English, newest bundle first).

| Code | Text | Present in |
|---:|---|---|
| 1 | Button | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 2 | App | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 3 | Schedules | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 4 | Mi home | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 5 | Quick start | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 101 | Routines | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 801 | Alexa | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 802 | Google | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 803 | IFTTT | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 804 | Yandex | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 805 | HomeKit | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 806 | Xiaoai | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 807 | TmallGenie | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 808 | Duer | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 809 | Dingdong | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 810 | Siri | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 811 | Clova | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 901 | WeChat | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 902 | Alipay | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 903 | Aqara | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 904 | Hisense | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 905 | HUAWEI | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |

<a id="cleanfinishcleanreasons"></a>
## Clean record finish reasons (`finish_reason`)

App wording (English, newest bundle first).

| Code | Text | Present in |
|---:|---|---|
| 21 | Cleaning interrupted by user | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 24 | Cleanup Interrupted | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 29 | Cleaning interrupted by user | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 32 | Could not continue cleaning | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 33 | Could not continue cleaning | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 34 | Cleanup Interrupted | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 35 | Cleaning interrupted by user | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 36 | Cleaning interrupted by user | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 37 | Cleaning interrupted by user | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 43 | Cleaning interrupted by user | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 45 | Positioning Failed | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 48 | Cleaning interrupted by user | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 49 | Cleaning interrupted by user | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 50 | Cleaning interrupted by user | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 51 | Cleanup Interrupted | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 52 | Finished cleaning | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 54 | Finished cleaning | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 55 | Finished cleaning | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 56 | Finished cleaning | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 57 | Finished cleaning | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 60 | Cleaning interrupted by user | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 61 | Area unreachable | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 62 | Area unreachable | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 64 | Cleanup Interrupted | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 65 | Positioning Failed | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 67 | Washing Error | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 68 | Failed to return to the dock | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 101 | Cleanup Interrupted | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 102 | Could not continue cleaning | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 103 | Cleaning interrupted by user | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 104 | Cleanup Interrupted | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 105 | Cleanup Interrupted | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 106 | Cleanup Interrupted | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 107 | Cleanup Interrupted | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 109 | Cleanup Interrupted | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 110 | Cleanup Interrupted | all except a01 c1 e2 m1s s5 t4 t6 v1 |

<a id="obstaclenames"></a>
## Obstacle types of map blocks 13–16 (type code → app name)

App wording (English, newest bundle first).

| Code | Text | Present in |
|---:|---|---|
| 0 | Wire | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 1 | Pet Waste | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 2 | Footwear | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 3 | Pedestal | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 4 | Pedestal | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 5 | Power Strip | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 9 | Scale | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 10 | Fabric | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 18 | Obstacle | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 25 | Dustpan | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 26 | Easily trapped furniture | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 27 | Easily trapped furniture | all except a01 c1 e2 m1s s5 t4 t6 v1 |
| 34 | Fabric | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 42 | Obstacle | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| 48 | Cords/wires | 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 49 | Pet | 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 50 | Pet | 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| 51 | Fabric/paper balls | 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |

## See also

- [Fan, water and mop values](fan-water-mop.md)
- [States](states.md)
