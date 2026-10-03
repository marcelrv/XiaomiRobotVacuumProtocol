# Feature matrix

[Home](../../README.md) / [Devices](index.md) / Feature matrix

Result of executing every `FeatureManager` predicate of each model's own plugin for that model id ([method](../concepts/feature-flags.md#how-the-gates-were-evaluated)). Cells: `Y` enabled for the product, `F` product allows it but the robot must report the firmware flag, `R` depends on location, `r` depends on app runtime state, `-` never enabled, `i` enabled only while the robot does not report the flag, `a` off in Mi Home but on in the Roborock app, `e` the predicate threw in the sandbox, blank = predicate not present in that plugin version. Generated from [`data/feature_gates.json`](../../data/feature_gates.json).

## Generation B (newer plugins)

| Predicate | Definition (newest bundle) | a14 | a15 | a23 | a26 | a27 | a29 | a30 | a34 | a37 | a38 | a40 | a46 | a51 | a52 | a62 | a64 | a65 | a66 | a69 | a70 | a72 | a73 | a74 | a75 | a76 |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `groundOnlySupportCarpet` |  |  |  |  | - | - | - | - |  |  |  |  | - | - |  |  | - | - | - | - | - | - | i | - | - | - |
| `is2022CESIpad` | account list |  |  |  | r | r |  |  |  |  |  |  | r | r |  |  | r | r | r | r | r | r | r | r | r |  |
| `is3DMapSupported` | product: isTanosSMax, isTopazSPlus, isTopazSC, isTopazSV, isPearlPlus, isTanosSC… |  |  |  | r | r | r | r | r | r | r | r | r | r | r | - | r | r | r | r | r | r | r | r | r | r |
| `isAnalysisSupported` | fw code 124 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isAnyStateTransitGotoSupported` | low bit 4 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isArMapSupported` | product: isTanosSMax, isTopazSPlus, isTopazSC, isTopazSV, isPearlPlus, isTanosSC… |  |  |  | r | r | r | r | r | r | r | r | r | r | r | - | r | r | r | r | r | r | r | r | r | r |
| `isAvoidCarpetSupported` |  | R | R | R | Y | Y | R | R | - | - | - | - | Y | Y | R | R | Y | Y | Y | Y | Y | Y | Y | Y | Y | R |
| `isAvoidCollisionModeSupported` | string bit 36 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | F | F |  |  |  | F | F |  |  |  |
| `isAvoidCollisionSupported` | low bit 27 |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isBackChargeAutoWashSupported` | string bit 12 |  |  |  | F | F | F | F |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F | F |
| `isCE` | region |  |  |  | R | R | R | R |  |  |  |  | R | R |  |  | R | R | R | R | R | R | R | R | R | R |
| `isCameraSupported` | product: TanosV_CN, TanosV_CE, TopazSV_CN, TopazSV_CE, TanosSV | - | - | - | Y | Y | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| `isCarefulSlowMopSupported` | high bit 9 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isCarpetDeepCleanSupported` | string bit 3 |  |  |  | F | F | F | F |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F | F |
| `isCarpetShowOnMap` | high bit 12 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isCarpetSupported` | low bit 9 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isCes2022Supported` | string bit 16 |  |  |  | F | F |  |  |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F |  |
| `isCleanRouteDeepSlowPlusSupported` | string bit 24 |  |  |  | F | F |  |  |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F |  |
| `isCleanRouteFastModeSupported` | string bit 8 |  |  |  | F | F | F | F |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F | F |
| `isCleanRouteSettingSupported` |  |  |  |  | Y | Y |  |  |  |  |  |  | Y | Y |  |  | Y | Y | Y | Y | Y | F | F | Y | Y |  |
| `isCornerCleanModeSupported` | string bit 31 |  |  |  | F | F |  |  |  |  |  |  | F |  |  |  | F | F | F |  |  | F | F | F | F |  |
| `isCornerMopStrechOutSupported` | string bit 40 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | F | F |  |  |  | F | F |  |  |  |
| `isCurrentMapRestoreEnabled` | low bit 13 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isCustomModeIconSupported` |  | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R |
| `isCustomModeSupported` | product: Ruby, Ruby2, Rubys, Sapphire, SapphireC, SapphireLite… | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `isCustomWaterBoxDistanceSupported` | low bit 31 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isDebugMidRebootOnMijiaSupported` | account list |  |  |  | r | r |  |  |  |  |  |  | r | r |  |  | r | r | r | r | r | r | r | r | r |  |
| `isDebuggableV1User` | account list |  |  |  | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r |
| `isDisableBackAndMore` | account list | r | r | r |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `isDssBelievable` | string bit 17 |  |  |  | F | F |  |  |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F |  |
| `isDustCollectionSettingSupported` | low bit 25 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isDynamicAdaptionCarpetSupported` | product: isTopazSV |  |  |  | R | R | F | F | - | - | - | - | R | R | - | - | R | R | R | R | R | R | R | R | R | F |
| `isDynamiclyAddCleanZonesSupported` | string bit 26 |  |  |  | F | F |  |  |  |  |  |  | F |  |  |  | - | - | F |  |  | F | F | - | F |  |
| `isDynamiclyModifyCleanAreas` | string bit 25 |  |  |  |  |  |  |  |  |  |  |  |  | F |  |  |  |  |  | F | F |  |  |  |  |  |
| `isDynamiclySkipCleanZoneSupported` | string bit 25 |  |  |  | F | F |  |  |  |  |  |  | F |  |  |  | - | - | F |  |  | F | F | - | F |  |
| `isEggModeSupported` | high bit 10 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | - | F | F | F | F | F | F | F | F | F | F |
| `isElectronicWaterBoxSupported` | product: RubysLite, TanosV_CN, TanosV_CE, TanosE, TanosSL, isUltronLite | - | - | - | - | - | - | - | - | Y | Y | - | - | - | - | - | - | - | - | - | - | - | Y | - | - | - |
| `isExplorationFuncSupported` | account list | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r |
| `isFCC` | region | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R |
| `isFCCOrCE` | region | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R |
| `isFindMeSupported` | product: Rubys, RubySC, RubysE, RubyPlus, Tanos_CN, Tanos_CE | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R |
| `isFloorDirCleanSetAnyTime` | string bit 42 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | F | F |  |  |  | F | F |  |  |  |
| `isFlowLedSettingSupported` | low bit 24 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isFwFilterObstacleSupported` | low bit 5 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isGotoPureCleanPathSupported` | string bit 19 |  |  |  | F | F |  |  |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F |  |
| `isHotWashTowelSupported` | string bit 41 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | F | F |  |  |  | F | F |  |  |  |
| `isIgnoreUnknownMapObjectSupported` | low bit 7 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isIn3DMapBlackList` | account list |  |  |  | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r |
| `isInARMapWhiteList` | account list |  |  |  | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r |
| `isLedSwitchVisible` | fw code 119; product: TanosS | F | F | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `isLeftWaterDrainSupported` | string bit 27 |  |  |  | F | F |  |  |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F |  |
| `isLogAllowed` | account list | r | r | r |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `isMainBrushUpDownSupported` | string bit 18 |  |  |  | F | F |  |  |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F |  |
| `isMapBeautifyDebugUser` | account list |  |  |  | r | r | r | r |  |  |  |  | r | r |  |  | r | r | r | r | r | r | r | r | r | r |
| `isMapBeautifyInternalDebugSupported` | low bit 21 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isMapCarpetAddSupport` | low bit 30 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isMapSegmentSupported` | fw code 116; product: RubyPlus, RubySC | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `isMaxPlusModeSupported` | product: isTopazSV, isPearlPlus, isTanosSMax, isTopazSPlus, isUltron, isUltronSPlus… |  |  |  | Y | Y | - | - | - | - | - | - | Y | Y | Y | Y | Y | Y | Y | Y | Y | - | - | Y | Y | - |
| `isModelOrderSupported` | product: Rubys, TanosE, Tanos_CE, Tanos_CN, TanosV_CN, TanosV_CE…; region | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R |
| `isMopForbiddenSupported` | product: isTanosV, isTanos, isTopazSV, isPearlPlus, TanosE, TanosSL… | F | F | F | Y | Y | - | - | - | F | F | - | - | Y | F | - | - | - | - | - | - | - | Y | Y | Y | - |
| `isMopPathSupported` | low bit 11 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isMultiFloorSupported` | fw code 120 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isMultiMapSegmentTimerSupported` | low bit 12 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isNewDataForCleanHistory` | low bit 22 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isNewDataForCleanHistoryDetail` | low bit 23 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isNewEndpointSupported` | string bit 38 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | F | F |  | F |  | F | F | F | F |  |
| `isNewFuncSupported` | account list | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `isNewRemoteViewSupported` | product: isTopazSPlus, isTanos, isTanosV, isTanosE, isTanosS, isTanosSPlus… |  |  |  | Y | Y | Y | Y | - | - | - | - | Y | Y | Y | Y | Y | Y | Y | Y | Y | - | - | - | - | Y |
| `isNoNeedSendCarpetPressSet` | string bit 44 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | F | F |  |  |  |
| `isNonePureCleanMopWithMaxPlus` | product: isUltronLite, isUltronE |  |  |  | - | - |  |  |  |  |  |  | - | - |  |  | - | - | - | - | - | Y | Y | - | - |  |
| `isObaAccount` | account list | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r |
| `isObjectPhotoShowSupported` | product: isTanosSPlus, isTanosSMax, isTopazSPlus, isUltron, isUltronSPlus, isTopazSC… |  |  |  | Y | Y | Y | Y | Y | Y | Y | Y | - | - | - | Y | - | - | - | - | - | Y | - | - | - | Y |
| `isObstaclesSupport` |  |  |  |  | Y | Y | - | - |  |  |  |  | Y | Y |  |  | Y | Y | Y | Y | Y | - | Y | Y | Y | - |
| `isOfflineMapSupported` | string bit 14; product: isMiApp |  |  |  | a | a | F | F |  |  |  |  | a | a |  |  | a | a | a | a | a | a | a | a | a | F |
| `isOpenMiShopSupported` | product: isTopazS, isTopazSPlus, isTopazSC, isTopazSV, isPearlPlus, isTanosSL… |  |  |  | a | a | a | a | a | a | a | a | a | Y | a | a | a | a | a | Y | Y | Y | Y | Y | Y | a |
| `isOrderCleanSupported` | fw code 123 | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R | R |
| `isOtaMiIOTAllowed` | account list | r | r | r |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `isOversea` | region |  |  |  | R | R | R | R |  |  |  |  | R | R | R |  | R | R | R | R | R | R | R | R | R | R |
| `isPetModeSettingSupported` |  |  |  |  | Y | Y | - | - |  |  |  |  | Y | Y |  |  | - | - | Y | Y | Y | - | - | - | - | - |
| `isPhotoUploadSupported` | low bit 16 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isPureCleanMopSupported` | product: isTopazS, isTopazSV, isPearlPlus, isTopazSPlus, isTopazSC, isTanosSMax… |  |  |  | Y | Y | Y | Y | - | - | - | - | Y | Y | Y | Y | Y | Y | Y | Y | Y | - | - | Y | Y | Y |
| `isRPCRetrySupported` | low bit 26 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isReSegmentSupported` | low bit 2 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isReactiveAISupported` | product: isTanosV, isTanosSPlus, isTanosSMax, isTopazSPlus, isUltron, isUltronSPlus… |  |  |  | Y | Y | - | - |  |  |  |  | Y | Y |  |  | Y | Y | Y | Y | Y | - | Y | Y | Y | - |
| `isRecordAllowed` | low bit 10; account list | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isRemoteSupported` | fw code 125 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isRoomNameSupported` | low bit 14 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isRubberBrushCarpetSupported` | product: TanosSC, TanosSE, TanosSL |  |  |  | - | - | - | - | Y | Y | Y | Y | - | - | - | - | - | - | - | - | - | Y | Y | - | - | - |
| `isSelfAdaptionCarpetSupported` | product: isTanosS, isTanosSPlus, isTopazS, isTopazSPower, isTopazSV |  |  |  | R | R | Y | Y | Y | - | - | Y | R | R | Y | Y | R | R | R | R | R | R | R | R | R | Y |
| `isSetChildSupported` | low bit 8 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isSettingCarpetFirstSupported` | string bit 23 |  |  |  | F | F |  |  |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F |  |
| `isShakeMopSetSupported` | low bit 18 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isShakeMopStrengthSupported` | product: TanosS, TanosSPlus, isGarnet, isTopazSV, isPearlPlus, isCoral… | Y | Y | Y | Y | Y | Y | Y | - | - | - | - | Y | Y | Y | Y | Y | Y | Y | Y | Y | - | - | Y | Y | Y |
| `isSharedAllowed` | product: isMiApp; account list | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r | r |
| `isShowCarpetEditEntrance` |  |  |  |  | F | F |  |  |  |  |  |  | F | F |  |  | F | F | F | F | F | F | Y | F | F |  |
| `isShowCarpetSweeperView` | product: TanosSL; region |  |  |  |  |  | Y | Y | Y | R | R | Y |  |  | Y | Y |  |  |  |  |  |  |  |  |  | Y |
| `isShowCleanFinishReasonSupported` | low bit 0 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isShowPureMopPath` | product: UltronSPlus |  |  |  | - | - |  |  |  |  |  |  | - | - |  |  | - | - | - | Y | Y | - | - |  |  |  |
| `isSingleLineLaserProduct` | product: isTopazSC, isPearl |  |  |  | - | - | - | - |  |  |  |  | - | - |  |  | Y | Y | - | - | - | - | Y | Y | Y | - |
| `isStructuredLightSupported` | product: TanosSPlus, TanosSMax, TopazSPlus, Ultron, UltronSPlus | - | - | Y | - | - | - | - | - | - | - | - | Y | Y | Y | - | - | - | Y | Y | Y | - | - | - | - | - |
| `isSuperDeepWashSupported` | string bit 15 |  |  |  | F | F |  |  |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F |  |
| `isSupportBackupMap` | high bit 17 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isSupportCleanEstimate` | string bit 1 |  |  |  | F | F | F | F | F | F | F | F | F | F | F |  | F | F | F | F | F | F | F | F | F | F |
| `isSupportCliffZone` | string bit 9 |  |  |  | F | F | F | F |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F | F |
| `isSupportCustomCarpet` | product: UltronLite |  |  |  | - | - |  |  |  |  |  |  | - | - |  |  | - | - | - | - | - | - | Y | - | - |  |
| `isSupportCustomDnd` | string bit 2 |  |  |  | F | F | F | F | F | F | F | F | F | F | F |  | F | F | F | F | F | F | F | F | F | F |
| `isSupportCustomDoorSill` | string bit 5 |  |  |  | F | F | F | F |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F | F |
| `isSupportCustomModeInCleaning` | high bit 18 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isSupportDirtyReplenishClean` | string bit 34 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | F | F |  |  |  | F | F |  |  |  |
| `isSupportDisturbInVideoSetting` | product: TanosV_CE, TopazSV_CE | Y | Y | Y | Y | - | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `isSupportFetchTimerSummary` | fw code 122; product: Tanos_CN | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isSupportFloorDirection` | string bit 11 |  |  |  | F | F | F | F |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F | F |
| `isSupportFloorEdit` | high bit 3 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isSupportFurniture` | high bit 4 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isSupportIncrementalMap` | string bit 13; string bit 22; product: isMiApp |  |  |  | F | F | F | F |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F | F |
| `isSupportLedStatusSwitch` | fw code 119; product: RubyPlus | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `isSupportMainSlideForMapShow` |  |  |  |  | r | r | r | r | r | r | r | r | r | r | r | Y | r | r | r | r | r | r | r | r | r | r |
| `isSupportMapElementSel` |  |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isSupportMapRotate` |  |  |  |  | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `isSupportMapTypeSel` |  |  |  |  | r | r | r | r | r | r | r | r | r | r | r | - | r | r | r | r | r | r | r | r | r | r |
| `isSupportMopBackPWMSet` | product: Pearl |  |  |  | - | - |  |  |  |  |  |  | - | - |  |  | - | - | - | - | - | - | - | Y | Y |  |
| `isSupportPetModeAlert` |  | - | - | Y |  |  |  |  | - | - | - | - |  |  | Y | - |  |  |  |  |  |  |  |  |  |  |
| `isSupportQuickMapBuilder` | high bit 7 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isSupportRemoteControlInCall` | high bit 19 |  |  |  | F | F | F | F | F | F | F | F | F | F | F |  | F | F | F | F | F | F | F | F | F | F |
| `isSupportRoomTag` | high bit 6 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isSupportSetSwitchMapMode` | low bit 28 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isSupportSetVolumeInCall` | string bit 0 |  |  |  | F | F | F | F | F | F | F | F | F | F | F |  | F | F | F | F | F | F | F | F | F | F |
| `isSupportSmartDoorSill` | string bit 10 |  |  |  | F | F | F | F |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F | F |
| `isSupportSmartGlobalCleanWithCustomMode` | high bit 8 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isSupportSmartScene` | high bit 1 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isSupportStuckZone` | string bit 4 |  |  |  | F | F | F | F |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F | F |
| `isSupportVoiceCtrolDebug` | fw code 130 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | F | F |  |  |  |
| `isSupportWaterMode` |  |  |  |  | Y | Y | Y | Y | - | Y | Y | - | Y | Y | Y | Y | Y | Y | Y | Y | Y | - | Y | Y | Y | Y |
| `isSupportedDownloadTestVoice` | high bit 16 |  |  |  | F | F | F | F | F | F | F | F | F | F | F |  | F | F | F | F | F | F | F | F | F | F |
| `isSupportedDrying` | high bit 15; product: isTopazSV_CE; region |  |  |  | R | F | R | R | e | e | e | e | R | R | e | F | R | R | R | R | R | R | R | R | R | R |
| `isSupportedSmartChangeWater` | high bit 16 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | F |  |  |  |  |  |  |  |  |  |  |
| `isSupportedValleyElectricity` | high bit 13 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isTwoKeyRealTimeVideoSupported` | string bit 32 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | F | F |  |  |  | F | F |  |  |  |
| `isTwoKeyRealTimeVideoSupportedInCharging` | string bit 33 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | F | F |  |  |  | F | F |  |  |  |
| `isUnsaveMapReasonSupported` | high bit 14 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isVideoLiveCallSupported` | product: isTopazSV, isPearlPlus, isCoral |  |  |  | Y | Y | - | - |  |  |  |  | - | - |  |  | - | - | - | - | - | - | - | - | - | - |
| `isVideoMonitorModelSupported` | product: isTanosV, isTopazSV, isPearlPlus, isCoral |  |  |  | Y | Y | - | - |  |  |  |  | - | - |  |  | - | - | - | - | - | - | - | - | - | - |
| `isVideoMonitorSupported` | low bit 3 | - | - | - | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isVideoSettingSupported` | low bit 6 | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isVoiceControlSupported` | string bit 37 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | F | F |  |  |  | F | F |  |  |  |
| `isWashThenChargeCmdSupported` | high bit 5 |  |  |  | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F | F |
| `isWaterUpDownDrainSupported` | string bit 20 |  |  |  | F | F |  |  |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F |  |
| `isWifiManageSupported` | string bit 7 |  |  |  | F | F | F | F |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F | F |
| `shouldShowCarpetSettingView` | product: isTanosSL |  |  |  | F | F |  |  |  |  |  |  | F | F |  |  | F | F | F | F | F | F | F | F | F |  |
| `shouldShowGuidePage` |  | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `shouldShowIgnoreCarpetView` |  | Y | Y | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `shouldShowSoftCleanMode` | product: RubyPlus, TanosV_CE | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| `shouldShowTroubleShootingGuide` | product: TanosV_CE, TanosV_CN, TanosE | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |

## Generation A (older plugins)

| Predicate | Definition (newest bundle) | a01 | a08 | a09 | a10 | a11 | a19 | c1 | e2 | m1s | p5 | s4 | s5 | s5e | s6 | t4 | t6 | v1 |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `isAnalysisSupported` | fw code 124 | F | F | F | F | F | F | F | F |  | F | F |  | F | F |  |  |  |
| `isAnyStateTransitGotoSupported` | low bit 4 |  | F | F | F | F | F |  |  |  | F | F |  | F | F |  |  |  |
| `isCameraSupported` | product: TanosV_CN, TanosV_CE, TopazSV_CN, TopazSV_CE, TanosSV | - | - | Y | Y | - | - | - | - |  | - | - | - | - | - | - | - |  |
| `isCarpetSupported` | low bit 9 |  | F | F | F |  | F |  |  |  |  | F |  | F | F |  |  |  |
| `isCleanRecordDetailToShowMapSupported` | product: isSapphire, isSapphireLiteCC, isSapphireLiteD | Y |  |  |  |  |  | - | Y |  |  |  |  |  |  |  |  |  |
| `isCleanTimeSupported` | fw code 103 | F |  |  |  |  |  | F | F |  |  |  |  |  |  |  |  |  |
| `isCurrentMapRestoreEnabled` | low bit 13 |  | F | F | F |  | F |  |  |  |  | F |  | F | F |  |  |  |
| `isCustomCleanTimeSettingSupported` | product: isSapphireCC | - |  |  |  |  |  | Y | - |  |  |  |  |  |  |  |  |  |
| `isCustomModeIconSupported` |  |  | - | R | R |  | - |  |  |  |  | - |  | R | - |  |  |  |
| `isCustomModeSupported` | product: Ruby, Ruby2, Rubys, Sapphire, SapphireC, SapphireLite… |  | - | Y | Y |  | - |  |  |  |  | - |  | Y | - |  |  |  |
| `isCustomSoundSupported` | product: isSapphire, isSapphireLiteD, isSapphireLiteCC | Y |  |  |  |  |  | - | Y |  |  |  |  |  |  |  |  |  |
| `isElectronicWaterBoxSupported` | product: RubysLite, TanosV_CN, TanosV_CE, TanosE, TanosSL, isUltronLite | - | - | Y | Y | Y | - | - | - | - | - | - | - | Y | - | - | - |  |
| `isExplorationFuncSupported` | account list |  | r | r | r | r | r |  |  |  | r | r |  | r | r |  |  |  |
| `isFCCOrCE` | region |  | R | R | R |  | R |  |  |  |  | R |  | R | R |  |  |  |
| `isFindMeSupported` | product: Rubys, RubySC, RubysE, RubyPlus, Tanos_CN, Tanos_CE |  | Y | R | R |  | Y |  |  |  |  | Y |  | R | Y |  |  |  |
| `isFwFilterObstacleSupported` | low bit 5 |  | F | F | F | F | F |  |  |  | F | F |  | F | F |  |  |  |
| `isHomeSecPasswordSupported` | low bit 3 |  |  |  |  | F |  |  |  |  | F |  |  |  |  |  |  |  |
| `isIgnoreUnknownMapObjectSupported` | low bit 7 |  | F | F | F |  | F |  |  |  |  | F |  | F | F |  |  |  |
| `isLogAllowed` | account list |  | r | r | r | r | r |  |  |  |  | r |  | r | r |  |  |  |
| `isMapInMainPageSupported` | product: isSapphire | - |  |  |  |  |  | - | Y |  |  |  |  |  |  |  |  |  |
| `isMapSegmentSupported` | fw code 116; product: RubyPlus, RubySC | Y | F | Y | Y | Y | Y | Y | Y | Y | F | F | Y | Y | Y | F | Y | Y |
| `isModelCustomModeSupported` |  |  | R | R | R |  | R |  |  |  |  | R |  | R | R |  |  |  |
| `isModelFindMeSupported` | product: isRubys, isRubysC, isRubysE, isRubyplus, isTanosT6, isTanosS6 |  | Y | R | R |  | Y |  |  |  |  | Y |  | R | Y |  |  |  |
| `isModelOrderSupported` | product: Rubys, TanosE, Tanos_CE, Tanos_CN, TanosV_CN, TanosV_CE…; region |  | Y | Y | Y |  | R |  |  |  |  | Y |  | Y | Y |  |  |  |
| `isMopForbiddenSupported` | product: isTanosV, isTanos, isTopazSV, isPearlPlus, TanosE, TanosSL… |  | F | F | F | F | F |  |  |  | F | F |  | F | F |  |  |  |
| `isMopPathSupported` | low bit 11 |  | F | F | F |  | F |  |  |  |  | F |  | F | F |  |  |  |
| `isMultiFloorSupported` | fw code 120 | F | F | F | F | F | F | F | F | - | F | F | F | F | F | F | F |  |
| `isMultiMapSegmentTimerSupported` | low bit 12 |  | F | F | F |  | F |  |  |  |  | F |  | F | F |  |  |  |
| `isNewFuncSupported` | account list |  | Y | Y | Y | Y | Y |  |  |  | r | Y |  | Y | Y |  |  |  |
| `isObaAccount` | account list | r | r | r | r | r | r | r | r |  | r | r |  | r | r |  |  |  |
| `isOrderCleanSupported` | fw code 123 | F | F | F | F | F | R | F | F |  | F | F |  | F | F |  |  |  |
| `isPhotoUploadSupported` | low bit 16 |  | F | F | F |  | F |  |  |  |  | F |  | F | F |  |  |  |
| `isReSegmentSupported` | low bit 2 |  | F | F | F | F | F |  |  |  | F | F |  | F | F |  |  |  |
| `isRecordAllowed` | low bit 10; account list |  | F | F | F |  | F |  |  |  |  | F |  | F | F |  |  |  |
| `isRemoteSupported` | fw code 125 | F | F | F | F | F | F | F | F |  | F | F |  | F | F |  |  |  |
| `isRoomNameSupported` | low bit 14 |  | F | F | F |  | F |  |  |  |  | F |  | F | F |  |  |  |
| `isSetChildSupported` | low bit 8 |  | F | F | F |  | F |  |  |  |  | F |  | F | F |  |  |  |
| `isShakeMopSetSupported` | low bit 18 |  | F | F | F |  | F |  |  |  |  | F |  | F | F |  |  |  |
| `isShowCleanFinishReasonSupported` | low bit 0 |  | F | F | F | F | F |  |  |  | F | F |  | F | F |  |  |  |
| `isSoftCleanModeSupported` |  | Y | - | - | - | - | - | - | Y | Y | Y | - | Y | - | - | - | Y | Y |
| `isSoftCleanModeSupportedInMain` | product: isTanosV, isTanosE, isTanos, isRubySC, isRubysLite, isRubysE |  | - | Y | - |  | - |  |  |  |  | - |  | - | - |  |  |  |
| `isVideoMonitorSupported` | low bit 3 |  | - | a | a | - | - |  |  |  | - | - |  | - | - |  |  |  |
| `isVideoSettingSupported` | low bit 6 |  | F | F | F | F | F |  |  |  |  | F |  | F | F |  |  |  |
| `isWaterBoxSupported` | product: Tanos_CE, Tanos_CN | - | - | - | - | - | - | - | - |  | - | - | - | - | Y | - |  |  |
