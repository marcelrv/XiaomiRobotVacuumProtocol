# roborock.vacuum.m1s

[Home](../../README.md) / [Devices](index.md) / m1s

| | |
|---|---|
| Model id | `roborock.vacuum.m1s` |
| Marketing name | Mi Robot Vacuum 1S (CN) — *Mi Home cloud device catalog* |
| openHAB binding name | Mi Robot Vacuum 1S — 🔶 openHAB |
| Legacy repo name | Mi Robot Vacuum 1S — ⚪ Legacy |
| Plugin generation | A (model groups) |
| Product code name (own bundle) | — |
| Product code name (newest bundle's model table) | `RUBY2` (series `m1s`, from `a74`) |
| Revision-suffixed ids (`<model>v2` ... the plugin treats as the same model) | — |
| Other models in the same plugin series | — |
| Speaker volume range (plugin model table) | ❓ Unknown (no range in this plugin) |
| Plugin version / SDK / build | 1.0.34 / 10034 / 2020-04-14 |
| Bundle file | `signed_10034_1001012_26_ANDROID_bundle_63599f008aa1f791dcf31176354d9bcc.zip` |
| Bundle format | plain-js, 678 modules |
| Code family | `F24` — identical bundle code: none (unique code) |
| Regions with this build | CN |
| `project.json` `models` field | absent |

## Regional builds

One bundle hash in all regions where this model was found (CN): no regional differences.

## Commands the plugin can send

Counts of method strings per category: **called** (call site found) / wrapper-only or declared-only / not present. Details per command are in the [command reference](../commands/index.md).

| Category | Called | Wrapper / declared only | Not present | App gates for the category (class for this model) |
|---|---:|---:|---:|---|
| [Cleaning control](../commands/cleaning-control.md) | 13 | 3 | 5 |  |
| [Remote control](../commands/remote-control.md) | 4 | 0 | 0 |  |
| [Status, properties and capabilities](../commands/status.md) | 5 | 2 | 2 |  |
| [Fan power, water flow and mop modes](../commands/cleaning-modes.md) | 5 | 1 | 25 |  |
| [Maps and multi-floor maps](../commands/maps.md) | 14 | 8 | 14 |  |
| [Rooms, zones and map objects](../commands/rooms-and-areas.md) | 4 | 2 | 17 |  |
| [Carpet handling](../commands/carpet.md) | 2 | 0 | 5 |  |
| [Timers and Do-Not-Disturb](../commands/timers.md) | 11 | 0 | 6 |  |
| [Consumables](../commands/consumables.md) | 2 | 0 | 0 |  |
| [Cleaning history](../commands/clean-history.md) | 4 | 1 | 2 |  |
| [Sound, voice packs and voice features](../commands/sound.md) | 6 | 0 | 5 |  |
| [Dock (auto-empty, mop washing and drying)](../commands/dock.md) | 0 | 0 | 30 |  |
| [Device settings](../commands/device-settings.md) | 2 | 0 | 6 |  |
| [Camera, live view and home security](../commands/camera.md) | 0 | 0 | 16 |  |
| [Network, time, firmware and logs](../commands/system.md) | 7 | 1 | 4 |  |
| [Diagnostic, test and internal commands](../commands/diagnostic.md) | 0 | 0 | 13 |  |
| **Total** | **79** | **18** | | |

"App gates" are the `FeatureManager` predicates that the app pages for the category test, evaluated for this model ([classes](#feature-gates-featuremanager-predicates)). A category whose gates all evaluate `N` or `RA` is present in the shared plugin code but never opened by its UI gates for this model (evaluation, not a robot test): none for this model.

<details><summary>All called method strings</summary>

- **Cleaning control**: [`app_start`](../commands/cleaning-control.md#app_start), [`app_stop`](../commands/cleaning-control.md#app_stop), [`app_pause`](../commands/cleaning-control.md#app_pause), [`app_charge`](../commands/cleaning-control.md#app_charge), [`app_spot`](../commands/cleaning-control.md#app_spot), [`app_wakeup_robot`](../commands/cleaning-control.md#app_wakeup_robot), [`app_zoned_clean`](../commands/cleaning-control.md#app_zoned_clean), [`resume_zoned_clean`](../commands/cleaning-control.md#resume_zoned_clean), [`app_segment_clean`](../commands/cleaning-control.md#app_segment_clean), [`resume_segment_clean`](../commands/cleaning-control.md#resume_segment_clean), [`app_goto_target`](../commands/cleaning-control.md#app_goto_target), [`stop_goto_target`](../commands/cleaning-control.md#stop_goto_target), [`find_me`](../commands/cleaning-control.md#find_me)
- **Remote control**: [`app_rc_start`](../commands/remote-control.md#app_rc_start), [`app_rc_move`](../commands/remote-control.md#app_rc_move), [`app_rc_end`](../commands/remote-control.md#app_rc_end), [`app_rc_stop`](../commands/remote-control.md#app_rc_stop)
- **Status, properties and capabilities**: [`get_prop`](../commands/status.md#get_prop), [`app_get_init_status`](../commands/status.md#app_get_init_status), [`get_serial_number`](../commands/status.md#get_serial_number), [`app_get_locale`](../commands/status.md#app_get_locale), [`app_stat`](../commands/status.md#app_stat)
- **Fan power, water flow and mop modes**: [`get_custom_mode`](../commands/cleaning-modes.md#get_custom_mode), [`set_custom_mode`](../commands/cleaning-modes.md#set_custom_mode), [`set_water_box_custom_mode`](../commands/cleaning-modes.md#set_water_box_custom_mode), [`get_customize_clean_mode`](../commands/cleaning-modes.md#get_customize_clean_mode), [`set_customize_clean_mode`](../commands/cleaning-modes.md#set_customize_clean_mode)
- **Maps and multi-floor maps**: [`get_map_v1`](../commands/maps.md#get_map_v1), [`get_multi_map`](../commands/maps.md#get_multi_map), [`get_multi_maps_list`](../commands/maps.md#get_multi_maps_list), [`load_multi_map`](../commands/maps.md#load_multi_map), [`name_multi_map`](../commands/maps.md#name_multi_map), [`save_map`](../commands/maps.md#save_map), [`reset_map`](../commands/maps.md#reset_map), [`start_edit_map`](../commands/maps.md#start_edit_map), [`end_edit_map`](../commands/maps.md#end_edit_map), [`get_recover_map`](../commands/maps.md#get_recover_map), [`get_recover_maps`](../commands/maps.md#get_recover_maps), [`recover_map`](../commands/maps.md#recover_map), [`del_map`](../commands/maps.md#del_map), [`set_lab_status`](../commands/maps.md#set_lab_status)
- **Rooms, zones and map objects**: [`get_room_mapping`](../commands/rooms-and-areas.md#get_room_mapping), [`merge_segment`](../commands/rooms-and-areas.md#merge_segment), [`split_segment`](../commands/rooms-and-areas.md#split_segment), [`name_segment`](../commands/rooms-and-areas.md#name_segment)
- **Carpet handling**: [`get_carpet_mode`](../commands/carpet.md#get_carpet_mode), [`set_carpet_mode`](../commands/carpet.md#set_carpet_mode)
- **Timers and Do-Not-Disturb**: [`get_timer`](../commands/timers.md#get_timer), [`set_timer`](../commands/timers.md#set_timer), [`del_timer`](../commands/timers.md#del_timer), [`upd_timer`](../commands/timers.md#upd_timer), [`get_server_timer`](../commands/timers.md#get_server_timer), [`set_server_timer`](../commands/timers.md#set_server_timer), [`del_server_timer`](../commands/timers.md#del_server_timer), [`upd_server_timer`](../commands/timers.md#upd_server_timer), [`get_dnd_timer`](../commands/timers.md#get_dnd_timer), [`set_dnd_timer`](../commands/timers.md#set_dnd_timer), [`close_dnd_timer`](../commands/timers.md#close_dnd_timer)
- **Consumables**: [`get_consumable`](../commands/consumables.md#get_consumable), [`reset_consumable`](../commands/consumables.md#reset_consumable)
- **Cleaning history**: [`get_clean_summary`](../commands/clean-history.md#get_clean_summary), [`get_clean_record`](../commands/clean-history.md#get_clean_record), [`get_clean_record_map`](../commands/clean-history.md#get_clean_record_map), [`del_clean_record`](../commands/clean-history.md#del_clean_record)
- **Sound, voice packs and voice features**: [`get_sound_volume`](../commands/sound.md#get_sound_volume), [`change_sound_volume`](../commands/sound.md#change_sound_volume), [`test_sound_volume`](../commands/sound.md#test_sound_volume), [`get_current_sound`](../commands/sound.md#get_current_sound), [`dnld_install_sound`](../commands/sound.md#dnld_install_sound), [`get_sound_progress`](../commands/sound.md#get_sound_progress)
- **Device settings**: [`get_led_status`](../commands/device-settings.md#get_led_status), [`set_led_status`](../commands/device-settings.md#set_led_status)
- **Network, time, firmware and logs**: [`get_network_info`](../commands/system.md#get_network_info), [`get_timezone`](../commands/system.md#get_timezone), [`set_timezone`](../commands/system.md#set_timezone), [`set_app_timezone`](../commands/system.md#set_app_timezone), [`enable_log_upload`](../commands/system.md#enable_log_upload), [`user_upload_log`](../commands/system.md#user_upload_log), [`set_fds_endpoint`](../commands/system.md#set_fds_endpoint)

</details>

## Feature gates (FeatureManager predicates)

Result of executing the plugin's own `FeatureManager` for this model id under six runtime situations (location cn/us/de × firmware flags none/all), with the plugin running inside Mi Home (`isMiApp = true`; a second pass with `false` finds the Roborock-app-only gates). Method: [feature flags](../concepts/feature-flags.md#how-the-gates-were-evaluated). Classes (letter used in the [feature matrix](matrix-features.md)): `Y` (Y) enabled regardless of firmware; `FW` (F) enabled only if the robot reports the firmware flag; `REG` (R) depends on the robot location; `RT` (r) depends on app runtime state; `N` (-) never enabled in the scenarios; `INV` (i) enabled only while the robot does not report the flag; `RA` (a) off inside Mi Home, on in the Roborock app (the predicate tests `!isMiApp`); `ERR` (e) the predicate threw in the sandbox.

| Class | Count | Predicates |
|---|---:|---|
| Y | 2 | `isMapSegmentSupported`, `isSoftCleanModeSupported` |
| N | 2 | `isElectronicWaterBoxSupported`, `isMultiFloorSupported` |

## Status parser

The status parser of this bundle reads 18 distinct status fields (of 59 seen across bundles): see [status fields](../reference/status-fields.md).

## Method table selection

Active `Methods` table: `default`. Table sizes in the bundle: default 96, saphire 55. Tables not selected for this model: saphire.

## See also

- [Devices index](index.md)
- [Feature matrix](matrix-features.md)
- [Command matrix](matrix-commands.md)
- [Methodology](../methodology.md)
