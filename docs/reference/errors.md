# Error codes

[Home](../../README.md) / Reference / Error codes

The `error_code` (or `dock_error_status`) of the status object and the plugin's own explanation. The *internal name* is the plugin's key for the entry (✅ Bundle · `Errors` table of the Main constants module). Titles are the app's English strings; the newest bundle is shown, other wordings are collapsed in the last column. Generated from [`data/enums.json`](../../data/enums.json).

| Code | Internal name | Title (newest) | Detail (newest) | Present in | Variants |
|---:|---|---|---|---|---|
| 0 | `OK` |  |  | all 42 |  |
| 1 | `Laser` | LiDAR Sensor error | LiDAR turret or laser blocked. Check for obstruction and retry. If there is no obstacle, relocate your robot and restart. | all 42 | 6 |
| 2 | `Bumper` | Bumper stuck | Bumper stuck. Clean it and lightly tap to release it. If there is no obstacle, relocate your robot and restart. | all 42 | 4 |
| 3 | `Drop` | Wheels suspended | Relocate your robot and restart. | all 42 | 4 |
| 4 | `Cliff` | Cliff sensor error | Robot suspended. Relocate it and restart. Or clean cliff sensors to correct this error. | all 42 | 4 |
| 5 | `MainStall` | Main brush jammed. | Clean main brush and bearings and restart. | all 42 | 3 |
| 6 | `SideStall` | Side brush jammed. | Remove and clean side brush and restart. | all 42 | 3 |
| 7 | `Wheel` | The robot is stuck, or main wheels are jammed. | Clean the main wheels then move the robot to a new location and restart. | all 42 | 3 |
| 8 | `Stuck` | The robot is trapped or stuck. | Clear any obstacles around the robot. Or move the robot to a new location and restart. | all 42 | 3 |
| 9 | `Dustbin` | Dustbin not installed | Reinstall dustbin and filter in place. If the problem persists, replace the filter. | all 42 | 4 |
| 10 | `Strainer` | Filter is wet or blocked. | Filter blocked or wet. Clean, dry for at least 24 hours and retry. If the problem persists, replace the filter. | all 42 | 3 |
| 11 | `Compass` | Strong magnetic field detected. | Strong magnetic field detected. Move robot away from magnetic tape and restart.  | all 42 | 3 |
| 12 | `Power` | Low battery | Charge the robot before use. | all 42 | 1 |
| 13 | `Charge` | Charging Error | Use a dry cloth to clean the charging contacts on the dock and on the robot. | all 42 | 5 |
| 14 | `Battery` | Unit temperature protection | Battery temperature too high or too low. Move the robot to a location with normal temperature range and wait one hour before restarting. | all 42 | 4 |
| 15 | `WallSensor` | The wall sensor is dirty. | The wall sensor is dirty. Clean the wall sensor. | all 42 | 2 |
| 16 | `Acc` | Robot is tilted | The robot is tilted. Move it to flat ground and restart. | all 42 | 2 |
| 17 | `SideBrush` | Side brush error | The side brush is not working. Reset the robot. | all 42 | 3 |
| 18 | `Fan` | Fan error |  Reset the robot. | all 42 | 4 |
| 19 | `Dock` | Dock not connected to power | Dock not connected to power. Check power cable and try again. | all 42 | 2 |
| 20 | `Mouse` | *(no English string; key `localization_strings_Main_Constants_102`)* | The ground tracking sensor may be dirty or covered with dust. Please use a dry cloth to wipe it, place the robot back to its original location and start it. | 3: a01 c1 e2 |  |
| 21 | `Lds` | Vertical Bumper Error | Vertical bumper error. Clean it, move the robot to a new location, and restart. | all 42 | 5 |
| 22 | `BackSensor` | Recharge Sensor Error | Use a dry cloth to clean the recharge sensor and retry | all 42 | 5 |
| 23 | `DockSensor` | Could not Reach Dock | Remove any obstacles around the dock and retry. | all 42 | 4 |
| 24 | `Forbidden` | No-Go Zone or Invisible Wall detected | No-Go Zone or Invisible Wall detected. Move the robot to a new location | all 42 | 4 |
| 25 | `VisualSensor` | Camera Error | Cameras dirty or covered. Clean or remove cover. | all 42 | 5 |
| 26 | `LightTouch` | Wall sensor error | Wall sensor error. Clean the wall sensor. | all 42 | 3 |
| 27 | `AudioError` | Jammed mop module | Check the mop module and move the robot to a new location and restart. | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 | 2 |
| 28 | `CarpetError` | The robot may be on a carpet | Please wipe the ultrasonic sensor or restart the robot away from the carpet | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 | 1 |
| 29 | `FindAItem` | if `isTanosS`: Unable to cross the carpet; else: Suspected pet waste found. | if `isTanosS`: Please place the robot on the other side of the carpet and restart it; else: The robot has been suspended, please check and restart | all except a01 c1 e2 m1s t4 t6 v1 | 6 |
| 30 | `ImageFPSError` | *(Chinese debug text, no English string)* | *(Chinese debug text, no English string)* | all except a01 c1 e2 m1s s5 t4 t6 v1 |  |
| 32 | `CollectDustError1` | No dustbin or filter installed | No dock dustbin or filter installed | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 | 1 |
| 33 | `CollectDustError2` | *(no English string; key `collecting_dusk_error33_title`)* | *(no English string; key `collecting_dusk_error33_desc`)* | 7: a08 a09 a10 a19 s4 s5e s6 | 1 |
| 34 | `CollectDustError3` | Clean the Auto-Empty Dock bin | Dock dustbin or air duct jammed, check and make it clean. | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 | 2 |
| 35 | `CollectDustError4` | Auto-Empty Dock voltage error | Unable to empty the dustbin | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 | 1 |
| 36 | `MoppingRoller1` | Wash roller may be jammed. | Remove and clean the wash roller. | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 | 1 |
| 37 | `MoppingRollerError2` | Wash roller not lowered properly. | Remove and clean the main brush and wash roller. | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 | 1 |
| 38 | `ClearWaterboxHoare` | Check the clean water tank. | Check tank placement or refill as required. | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 | 1 |
| 39 | `DirtyWaterboxHoare` | Check the dirty water tank. | Check tank placement or empty as required. | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 | 1 |
| 40 | `SinkStrainerHoare` | Water filter not installed. | Reinstall the water filter. | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 | 1 |
| 41 | `ClearWaterBoxExcepiton` | Clean water tank empty. | Refill tank. | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 | 1 |
| 42 | `ClearBrushExcepiton` | Check that the water filter has been correctly installed. | Check for correct water filter installation or jammed cleaner brush, and reinstall the mop making sure that it is flat. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 43 | `ClearBrushExcepiton` | Positioning button Error | Check if the positioning button is stuck, then move the robot away from the dock and restart. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 44 | `FilterScreenExcepiton` | Check and secure the dirty water tank cover | Water filter blocked. Clean and reinstall. If the problem persists, check that the dirty water tank cover is closed and the latch is secured. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 45 | `MoppingRoller1` | Wash roller may be jammed. | Remove and clean the wash roller. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 48 | `UpWaterException` | Refill error | Check if your water supply is available. If yes, re-plug the connection cable for the fill&drain element and retry. If the problem persists, contact customer support. | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |  |
| 49 | `DrainWaterException` | Drain error | Check for anything blocking the drainage outlet and remove. If the problem persists, contact customer support. | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |  |
| 51 | `TemperatureProtection` | Unit temperature protection | Move the robot to a location at room temperature and wait for a certain period. | 17: a26 a27 a29 a30 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 | 1 |
| 52 | `CleanCarouselException` | Please check the cleaning tray. | 1.Secure cleaning tray in place;2.Check for anything stuck in the dock water outlet;3.Please check and secure the dirty water tank cover. | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 | 1 |
| 53 | `CleanCarouselWaterFull` | Cleaning tray full. | The dock water outlet may be blocked, please check and remove; if it is not, check and secure the dirty tank cover and the latch. | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 | 1 |
| 54 | `WaterCarriageDrop` | The mop mount fell off.  | The mop cloth mount fell off, please reinstall it to resume working.  | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |  |
| 100-122 | `Inner` | Internal error | Internal error. Reset the robot. | all 42 | 4 |
| 123-124 | `Inner` | Internal error | Internal error. Reset the robot. | all except a01 c1 e2 m1s t6 v1 | 1 |
| 125 | `Inner` | Internal error | Internal error. Reset the robot. | all except v1 | 3 |
| 126-127 | `Inner` | Dock Error | An abnormality inside the base is detected, plug in and unplug the power supply and try again. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 128-129 | `Inner` | Internal error | Internal error. Reset the robot. | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |  |
| 130-131 | `Inner` | Dock Error | An abnormality inside the base is detected, plug in and unplug the power supply and try again. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 134 | `Inner` | Dock Error | An abnormality inside the base is detected, plug in and unplug the power supply and try again. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 135 | `Inner` | Wash roller may be jammed. | Remove and clean the wash roller. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 137 | `Inner` | Wash roller may be jammed. | Remove and clean the wash roller. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 138 | `Inner` | Clean main brush and bearings. | Clean main brush and bearings and restart. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 140 | `Inner` | Clean main brush and bearings. | Clean main brush and bearings and restart. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 141 | `Inner` | The robot is stuck, or main wheels are jammed. | Clean the main wheels. Or relocate your robot and restart. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 143 | `Inner` | The robot is stuck, or main wheels are jammed. | Clean the main wheels. Or relocate your robot and restart. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 145 | `Inner` | Dock Error | An abnormality inside the base is detected, plug in and unplug the power supply and try again. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 147-150 | `Inner` | Dock Error | An abnormality inside the base is detected, plug in and unplug the power supply and try again. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 151-153 | `Inner` | Dock Error | An abnormality inside the base is detected, plug in and unplug the power supply and try again. | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |  |
| 154 | `Inner` | Side brush error | The side brush is not working. Reset the robot. | 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 155 | `Inner` | Fan error |  Reset the robot. | 16: a26 a27 a29 a30 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |  |
| 156-159 | `Inner` | Dock Error | An abnormality inside the base is detected, plug in and unplug the power supply and try again. | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |  |
| 253-254 | `Inner` | Internal error | Internal error. Reset the robot. | 13: a26 a27 a46 a51 a64 a65 a66 a69 a70 a72 a73 a74 a75 |  |
| 255 | `Inner` | Internal error | Internal error. Reset the robot. | all 42 | 4 |
| 644 | `Binfull` | Empty the dustbin | Dustbin is full. Empty the dustbin | all 42 | 3 |

## Notes

- Source tables: the `Errors` table of the main constants module in every bundle, and in the a01, c1 and e2 bundles additionally `ErrorsCodeToastMap`, which carries code 20 (`Mouse`).
- A run of consecutive codes with identical content is shown as one row (for example 100-122).
- The same internal name can carry different wording per product line; e.g. code 29 (`FindAItem`) reads "Unable to cross the carpet" for the product `TanosS` and "Suspected pet waste found" otherwise in the newest bundles, and an item-detection text in older ones. A text of the form `if ...: ...; else: ...` means the plugin chooses the string by product at run time.
- Titles shown as *(no English string; key ...)* are keys that are missing from the bundle's English string table; entries shown as Chinese debug text exist only as Chinese test strings in the plugin (for example the image-frame error 30).
- Codes 100-159 and 253-255 are mapped to generic "inner error" entries; the plugin shows a service-contact text for them.
- Code 644 is the plugin's "bin full" entry (`Binfull`). Code 254 is an *inner error* entry ("Internal error") present only in the newer bundles, and 255 is also an inner error. ⚪ Legacy listed 254 as "Bin full" (openHAB 🔶 does too).
- Code 20 is **not** "Unknown Error" (⚪ Legacy / 🔶 openHAB wording): the a01, c1 and e2 bundles map it to `Mouse`, "Please clean the motion tracking sensor and place the robot back to its original location and start it."; no other bundle has an entry for 20.
- ⚪ Legacy [status.md](../../status.md) lists codes 0-24, 254, 255 and -1. Codes above 25 in the table are new.

<a id="app-side-codes"></a>
## App-side codes (not robot error codes)

These numbers are produced by the plugin itself and never appear in `error_code`.

### Live-view (video) errors

| Code | App name | English hint | Present in |
|---:|---|---|---|
| -100 | `Video_StartPreviewFailed_unKnownReason` | Network failed. Please check the robot's network and try again. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -101 | `Video_StartPreviewFailed_robotInCharge` | Please move the device away from the charging dock to view the video. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -102 | `Video_StartPreviewFailed_cameraStatusError` | Camera error. Please restart the robot and try again. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -103 | `Video_StartPreviewFailed_innerUnknowReason` | Please disable and then re-enable the remote viewing function, or restart the device and try again. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -104 | `Video_StartPreviewFailed_alreadyInPreview` | Please check if the video is being displayed on another phone. If not, please wait a minute and try again. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -105 | `Video_StartPreviewFailed_passwordError` | Please reset the robot and try again. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -106 | `Video_StartPreviewFailed_passwordErrorFrequently` | Please reset the robot and try again. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -107 | `Video_StartPreviewFailed_robotIsDisconnecting` | Resource occupied. Please try again later. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -108 | `Video_StartPreviewFailed_requestTurnserverFailed` | Network connection error. Please check your network and try again. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -110 | `Video_GetTurnServerFailed` | Network connection error. Please check your network and try again. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -111 | `Video_GetDeviceSdpFailed` | Network connection error. Please check your network and try again. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -112 | `Video_SendSDKSdpToDeviceFailed_responseTimeout` | Camera error. Please restart the robot and try again. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -113 | `Video_SendSDKSdpToDeviceFailed_processedError` | Network connection error. Please check your network and try again. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -114 | `Video_PreviewTimeout` | Phone or robot network error. Please check the network connection or switch to a different network and try again. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -115 | `Video_PreviewCalledError` | Operation too frequent. Please try again later. | 33: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| -116 | `Video_PreviewDustCollectionError` | Unable to remote viewing. Emptying in progress. | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |

### Map operation errors (`mapOpErrorCode`)

| Name | Value | Present in |
|---|---:|---|
| `VENDOR_ERROR_CODE` | -10000 | all 42 |
| `PROCESS_BUSY_ERROR_CODE` | -10001 | all 42 |
| `ERROR_ACCESS_DENIED` | -10002 | all 42 |
| `ERROR_ACTION_LOCKED` | -10003 | all 42 |
| `ERROR_ACTION_TIMEOUT` | -10004 | all 42 |
| `PARAM_ERROR` | -10005 | all 42 |
| `OPERATION_FAILED` | -10006 | all 42 |
| `BAD_REQUEST` | -10007 | all 42 |

Other plugin-level codes: `-10002` = access denied (the status poll treats it as "invalid connection"); `PluginNeedsUpdate` (−1) and `Unknown` (−999) for map fetch failures; `LoadMapDuplicated` (−100) and `DeviceNotAvaliable` (−101) in the multi-floor page.

## See also

- [Status fields](status-fields.md)
- [States](states.md)
