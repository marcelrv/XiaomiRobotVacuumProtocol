# Feature flags and capability gates

[Home](../../README.md) / Concepts / Feature flags

The Mi Home plugin decides which controls to show from three kinds of information: **what the robot reports** (firmware feature codes and two feature words), **what the product is** (model id mapped to a product code name) and **where the robot is** (location). This page lists the three robot-reported sets with the app code that reads them, and explains how the per-model gate tables in [devices](../devices/index.md) were obtained. Because the gates live in the plugin, this is the closest evidence the bundles give for "model X offers feature Y" (see [what a bundle does and does not prove](../methodology.md#what-a-bundle-does-and-does-not-prove)).

## Where the robot reports its features

| Source | Used by | Shape |
|---|---|---|
| [`get_fw_features`](../commands/status.md#get_fw_features) | called by a01 c1 e2 s5 v1 | `result` = array of feature codes |
| [`app_get_init_status`](../commands/status.md#app_get_init_status) `result[0].feature_info` | called by 38 bundles (wrapped only in a01 c1 e2 v1) | array of feature codes (`101`…`130`) |
| `result[0].new_feature_info` | `FeatureManager` | one number; the app tests bits of the low 32-bit word with `&` and bits of the high word with `/ 2^32 >> n & 1` |
| `result[0].new_feature_info_str` | `FeatureManager` of 21 bundles (a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76) | string of hex digits, length a multiple of 8; the app parses digit groups with `parseInt("0x" + str.slice(...))` |
| `result[0].local_info.location` | `FeatureManager` | `prc` is rewritten to `cn`; compared with `cn` / `us` / `de` |
| `result[0].local_info.featureset` | `RobotStatusManager` | bit 0 = "FCC state" (`isFCC`, `isFCCOrCE`) |

All of this is ✅ Bundle (a65 m10007 `fetchDeviceLocation`, m10037 `FeatureManager`; the other bundles were extracted by script). Which codes or bits a particular robot **sets** is not in the bundles; the only evidence is the user-contributed captures in [legacy captures](#legacy-captures).

<a id="feature-codes"></a>
## Firmware feature codes (`feature_info`)

`FeatureManager.isSupportFeature(code)` is true when the code is in the array. These are all codes that any bundle tests with a literal number; a code that is not in the table is not tested by any of the 42 bundles.

| Code | Gates (bundle code) | Bundles testing it | Legacy list |
|---:|---|---:|---|
| 103 | clean-time feature (`isCleanTimeSupported`) | 3 | Clean Time Supported |
| 111 | FDS endpoint (`isSupportFDSEndPoint`) | 42 | Supports FSEndPoint |
| 112 | automatic splitting of rooms (`isSupportAutoSplitSegments`) | 42 | Supports AutoSplitSegments |
| 113 | delete-map button of the saved-map list when multi-floor is off (`showDeleteButton`, inside the map-list `render`) | 10 | Supportrs Delete Map feature |
| 114 | cleaning rooms in a chosen order (`isSupportOrderSegmentClean`) | 42 | Supports OrderSegmentClean |
| 116 | room (segment) support (`isMapSegmentSupported`); consulted only for the products `RubyPlus` and `RubySC`, every other product returns true without it | 41 | Map Segment Supported |
| 118 | custom clean mode synchronisation (`syncCustomMode`, `resetCleanMode`, `customModeDidChange`, `handleModeTabDidChange`, `updateCustomMode`) | 37 |  |
| 119 | LED switch (`isSupportLedStatusSwitch`, `isLedSwitchVisible`) | 37 | Supports Led Status Switch |
| 120 | multi-floor maps (`isMultiFloorSupported`) | 40 | Multi Floor Supported |
| 122 | timer summary (`isSupportFetchTimerSummary`, `fetchListDataFromRobot`); not used for the product `Tanos_CN` | 40 | Supports FetchTimer Summary |
| 123 | order clean (`isOrderCleanSupported`) | 37 | Orders Clean Supported |
| 124 | analysis page (`isAnalysisSupported`) | 37 | Analysis Supported |
| 125 | remote control (`isRemoteSupported`) | 37 | Remote Supported |
| 130 | voice-control debug entry (`isSupportVoiceCtrolDebug`) | 2 |  |

Codes without a literal test in any bundle: 101, 102, 104, 105, 106, 107, 108, 109, 110, 115, 117, 121, 126, 127, 128, 129. The legacy list names `115` ("Spot Clean") and has no name for the others (the legacy captures below report codes such as 117 and 121 for real robots, so the app tests do not cover every code robots send); the bundles neither confirm nor contradict `115`.

⚪ Legacy named the codes `103`, `111`-`116`, `119`, `120` and `122`-`125`. The bundles test all of them except `115`; `113` is confirmed as the delete-map button. The bundles additionally test `118` and `130`, which the legacy list leaves blank.

<a id="new_feature_info"></a>
## Feature word 1: `new_feature_info`, low word

Tested as `robotNewFeatures & mask` (✅ Bundle · a65 m10037). The same bit has different predicate names in different bundles when the code differs by generation; both names are listed.

| Bit | Predicate in the plugin (number of bundles defining it) |
|---:|---|
| 0 | `isShowCleanFinishReasonSupported` (34) |
| 1 | `isMopForbiddenSupported` (6) |
| 2 | `isReSegmentSupported` (34) |
| 3 | `isHomeSecPasswordSupported` (2), `isVideoMonitorSupported` (22) |
| 4 | `isAnyStateTransitGotoSupported` (34) |
| 5 | `isFwFilterObstacleSupported` (34) |
| 6 | `isVideoSettingSupported` (33) |
| 7 | `isIgnoreUnknownMapObjectSupported` (32) |
| 8 | `isSetChildSupported` (32) |
| 9 | `isCarpetSupported` (32) |
| 10 | `isRecordAllowed` (10) |
| 11 | `isMopPathSupported` (32) |
| 12 | `isMultiMapSegmentTimerSupported` (32) |
| 13 | `isCurrentMapRestoreEnabled` (32) |
| 14 | `isRoomNameSupported` (32) |
| 16 | `isPhotoUploadSupported` (32) |
| 18 | `isShakeMopSetSupported` (32) |
| 21 | `isMapBeautifyInternalDebugSupported` (25) |
| 22 | `isNewDataForCleanHistory` (25) |
| 23 | `isNewDataForCleanHistoryDetail` (25) |
| 24 | `isFlowLedSettingSupported` (0) |
| 25 | `isDustCollectionSettingSupported` (25) |
| 26 | `isRPCRetrySupported` (25) |
| 27 | `isAvoidCollisionSupported` (23) |
| 28 | `isSupportSetSwitchMapMode` (22) |
| 30 | `isMapCarpetAddSupport` (22) |
| 31 | `isCustomWaterBoxDistanceSupported` (22) |

<a id="new_feature_info-high"></a>
## Feature word 1: `new_feature_info`, high word

Tested as `robotNewFeatures / Math.pow(2, 32) >> n & 1`; bit numbers are within the high word (bit 0 = 2^32 of the number).

| Bit | Predicate in the plugin (number of bundles defining it) |
|---:|---|
| 1 | `isSupportSmartScene` (22) |
| 3 | `isSupportFloorEdit` (22) |
| 4 | `isSupportFurniture` (22) |
| 5 | `isWashThenChargeCmdSupported` (22) |
| 6 | `isSupportRoomTag` (22) |
| 7 | `isSupportQuickMapBuilder` (22) |
| 8 | `isSupportSmartGlobalCleanWithCustomMode` (22) |
| 9 | `isCarefulSlowMopSupported` (22) |
| 10 | `isEggModeSupported` (22) |
| 12 | `isCarpetShowOnMap` (22) |
| 13 | `isSupportedValleyElectricity` (22) |
| 14 | `isUnsaveMapReasonSupported` (22) |
| 15 | `isSupportedDrying` (1) |
| 16 | `isSupportedDownloadTestVoice` (21), `isSupportedSmartChangeWater` (1) |
| 17 | `isSupportBackupMap` (22) |
| 18 | `isSupportCustomModeInCleaning` (22) |
| 19 | `isSupportRemoteControlInCall` (21) |

<a id="feature-word-new_feature_info_str"></a>
## Feature word 2: `new_feature_info_str`

Hex string read from its right end: bit 0 is the lowest bit of the last hex digit. `slice(-8)` covers bits 0-31 (the predicates mask the 32-bit value); the digits before it carry bits 32-35 (`slice(-9, -8)`), 36-39 (`slice(-10, -9)`) and 40-43 (`slice(-11, -10)`). Each predicate additionally requires a non-empty string whose length is a multiple of 8 (most of them). Present in the code of 21 bundles (a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76); older generations never read the string. The relation between `new_feature_info` and `new_feature_info_str` (whether the string repeats the number) is ❓ Unknown: the bundles use them independently and assign different meanings to the same bit number. `isSupportIncrementalMap` is a special case: low-word bit 13 of the string in Mi Home, but bit 22 in the Roborock app (`RRMISDK.isMiApp` branch).

| Bit | Predicate in the plugin (number of bundles defining it) |
|---:|---|
| 0 | `isSupportSetVolumeInCall` (21) |
| 1 | `isSupportCleanEstimate` (21) |
| 2 | `isSupportCustomDnd` (21) |
| 3 | `isCarpetDeepCleanSupported` (16) |
| 4 | `isSupportStuckZone` (16) |
| 5 | `isSupportCustomDoorSill` (16) |
| 7 | `isWifiManageSupported` (16) |
| 8 | `isCleanRouteFastModeSupported` (16) |
| 9 | `isSupportCliffZone` (16) |
| 10 | `isSupportSmartDoorSill` (16) |
| 11 | `isSupportFloorDirection` (16) |
| 12 | `isBackChargeAutoWashSupported` (16) |
| 13 | `isSupportIncrementalMap` (6) |
| 14 | `isOfflineMapSupported` (6) |
| 15 | `isSuperDeepWashSupported` (13) |
| 16 | `isCes2022Supported` (13) |
| 17 | `isDssBelievable` (13) |
| 18 | `isMainBrushUpDownSupported` (13) |
| 19 | `isGotoPureCleanPathSupported` (13) |
| 20 | `isWaterUpDownDrainSupported` (13) |
| 22 | `isSupportIncrementalMap` (6) |
| 23 | `isSettingCarpetFirstSupported` (13) |
| 24 | `isCleanRouteDeepSlowPlusSupported` (13) |
| 25 | `isDynamiclyModifyCleanAreas` (3), `isDynamiclySkipCleanZoneSupported` (10) |
| 26 | `isDynamiclyAddCleanZonesSupported` (10) |
| 27 | `isLeftWaterDrainSupported` (13) |
| 31 | `isCornerCleanModeSupported` (10) |
| 32 | `isTwoKeyRealTimeVideoSupported` (4) |
| 33 | `isTwoKeyRealTimeVideoSupportedInCharging` (4) |
| 34 | `isSupportDirtyReplenishClean` (4) |
| 36 | `isAvoidCollisionModeSupported` (4) |
| 37 | `isVoiceControlSupported` (4) |
| 38 | `isNewEndpointSupported` (7) |
| 40 | `isCornerMopStrechOutSupported` (4) |
| 41 | `isHotWashTowelSupported` (4) |
| 42 | `isFloorDirCleanSetAnyTime` (4) |
| 44 | `isNoNeedSendCarpetPressSet` (2) |

## Other gates in `FeatureManager`

- **Product** (`DMM.currentProduct`, `RRMISDK.isTanosS()` and similar): the model id is looked up in the plugin's `DeviceModelManager` / model-group tables, which return a product code name; see the product column of [devices](../devices/index.md) and [model generations](model-generations.md).
- **Region**: `deviceLocation` (`cn`, `us`, `de`, …) and `isFCC` / `isCE` / `isOversea`.
- **Account lists**: some predicates test the Mi Home account id against lists baked into the plugin (`userGate` in `data/feature_gates.json`). The lists themselves are deliberately not reproduced here; such predicates are classified as runtime-dependent.
- **Runtime state**: the app version, the Mi Home account, debug flags, device status fields.

<a id="how-the-gates-were-evaluated"></a>
## How the gates were evaluated

For every bundle the script `tools/js/eval_features.mjs` loads the plugin's own `FeatureManager` and `DeviceModelManager` (or model-group) modules into a Node `vm` context in which every other module is an inert stub, sets the device model id, and binds `isMiApp = true` (the plugin runs inside Mi Home; a second pass with `false` marks the Roborock-app-only gates), evaluates the model-group helpers of the older plugins (`isTanosV()`, `isSapphire()`, ... each a list of model ids) for the device model, and calls each zero-argument predicate under six scenarios: location `cn`, `us`, `de` × firmware reports **nothing** (empty code list, `new_feature_info = 0`, empty string) or **everything** (codes 101-140, all bits set, string of `f`). Results are classified:

| Class | Meaning | Count over the 42 bundled models (predicate × model) |
|---|---|---:|
| `Y` | true in every scenario (no firmware or region dependence) | 518 |
| `FW` | false without the robot reporting the flag, true with it (the product allows the feature) | 1743 |
| `REG` | depends on the location (the flag may or may not also be needed) | 259 |
| `RT` | touches runtime state of the app (version, account, debug flags) that the sandbox cannot supply | 306 |
| `INV` | true only while the robot does not report the flag (inverse firmware dependence) | 1 |
| `RA` | false in Mi Home but true when `isMiApp` is false: the gate belongs to the Roborock app (for example the live-view monitor of the older plugins) | 30 |
| `N` | false in every scenario (product excluded, or an input the sandbox does not provide) | 896 |
| `ERR` | the predicate threw (usually a missing runtime input) | 5 |

What this proves: the plugin shows the feature for this model id when the robot reports the flag. What it does not prove: that the robot reports the flag; that a firmware answers the underlying RPC. `N` can also mean "needs an input the sandbox lacks", so an `N` is evidence of "never enabled by the app in these scenarios", not of "robot cannot do it". Generated tables: [feature matrix](../devices/matrix-features.md) and the per-model pages. Raw results: [`data/feature_gates.json`](../../data/feature_gates.json).

<a id="legacy-captures"></a>
## Legacy captures

⚪ Legacy: `get_fw_features` / `feature_info` lists that users posted for real robots (firmware as written in the legacy page). Unverified; the bundles contain no robot data.

| Model | Name (legacy) | Firmware | Codes reported |
|---|---|---|---|
| `v1` | Mi Robot Vacuum | 3.5.8_004018 | 101, 102, 104, 105 |
| `a10` | Roborock S6 MaxV | 3.5.8_5850 | 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125 |
| `a15` | Roborock S7 | 4.1.2_1140 | 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 122, 123, 124, 125 |
| `a27` | Roborock S7 MaxV | 4.3.5_5602 | 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125 |
| `a30` | Roborock G10 | 4.3.5_1258 | 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 122, 123, 124, 125 |
| `a38` | Roborock Q7 Max+ | 4.3.5_0866 | 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 122, 123, 124, 125 |
| `a40` | Roborock Q7+ | 4.1.5_0680 | 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 122, 123, 124, 125 |
| `m1s` | Mi Robot Vacuum 1S | ❓ not stated | 105 |
| `s5` | Roborock S5 | 3.5.8_002034 | 102, 103, 104, 105, 111, 112, 113, 114, 115, 116, 117, 118, 119, 122, 123, 125 |
| `s5e` | Roborock S5 Max | 4.1.2_1668 | 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 122, 123, 124, 125 |

Observations that can be checked against the code tables above: the capture of the old `v1` (`101, 102, 104, 105`) contains codes that no bundle tests; the S5 capture contains `102`, `103`, `104`, `105`, of which only `103` is tested by a bundle.

## See also

- [Feature matrix](../devices/matrix-features.md)
- [`app_get_init_status`](../commands/status.md#app_get_init_status)
- [Model generations](model-generations.md)
- [Methodology](../methodology.md)
