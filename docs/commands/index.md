# Command index

[Home](../../README.md) / Commands

Every RPC method string that the 42 analysed Mi Home plugin bundles (one per model) can send to the robot, with the evidence found in the bundles. Generated from [`data/commands.json`](../../data/commands.json).

- **Called** = the plugin code contains a call site (directly, through a `Protocol.Methods.<Key>` reference or through a `RobotApi` wrapper that is used).
- **Wrapper only / declared only** = the string is wrapped or listed but no call site was found.
- A call site proves that the app *can send* the call; it does not prove that a particular firmware answers it. See [methodology](../methodology.md#what-a-bundle-does-and-does-not-prove).

## Cleaning control

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`app_start`](cleaning-control.md#app_start) | Starts a whole-map clean; also used to resume an interrupted global clean and to start building a new floor… | all 42 | — |
| [`app_stop`](cleaning-control.md#app_stop) | Ends the running job (the robot stays where it is). | all 42 | — |
| [`app_pause`](cleaning-control.md#app_pause) | Pauses the running clean or spot clean so that it can be resumed. | all 42 | — |
| [`app_charge`](cleaning-control.md#app_charge) | Sends the robot back to the charging dock. | all 42 | — |
| [`app_spot`](cleaning-control.md#app_spot) | Cleans the area around the robot's current position. | all 42 | — |
| [`app_wakeup_robot`](cleaning-control.md#app_wakeup_robot) | Wakes a sleeping robot so that it accepts commands. | all 42 | — |
| [`app_zoned_clean`](cleaning-control.md#app_zoned_clean) | Cleans one or more rectangles of the map, each with its own repeat count. | all 42 | — |
| [`stop_zoned_clean`](cleaning-control.md#stop_zoned_clean) | Wrapped for every newer bundle; the only call site found is in the s5 bundle. | 2 | 40 / 0 |
| [`resume_zoned_clean`](cleaning-control.md#resume_zoned_clean) | Resumes an interrupted zone clean. | all 42 | — |
| [`app_segment_clean`](cleaning-control.md#app_segment_clean) | Cleans the selected rooms; newer firmware also accepts repeat count, clean method and order. | all 42 | — |
| [`stop_segment_clean`](cleaning-control.md#stop_segment_clean) | Wrapped in all bundles; no call site found (the app uses `app_stop`). | 0 | 42 / 0 |
| [`resume_segment_clean`](cleaning-control.md#resume_segment_clean) | Resumes an interrupted room clean. | all 42 | — |
| [`app_goto_target`](cleaning-control.md#app_goto_target) | Sends the robot to map coordinates. | all 42 | — |
| [`stop_goto_target`](cleaning-control.md#stop_goto_target) | Cancels a running go-to. | all 42 | — |
| [`find_me`](cleaning-control.md#find_me) | Makes the robot emit a locator sound. | all 42 | — |
| [`start_clean`](cleaning-control.md#start_clean) | Listed in the Methods tables (`TimerStart`) of every bundle but never called by the plugin. | 0 | 0 / 42 |
| [`start_wash_then_charge`](cleaning-control.md#start_wash_then_charge) | Dock action offered when finishing a clean on a washing dock. | 22 | — |
| [`app_start_build_map`](cleaning-control.md#app_start_build_map) | Starts a quick-mapping run ("Mapping" state 29). | 22 | — |
| [`app_resume_build_map`](cleaning-control.md#app_resume_build_map) | Resumes an interrupted quick-mapping run. | 22 | — |
| [`app_skip_current_cleaning_area`](cleaning-control.md#app_skip_current_cleaning_area) | Skips the room or zone that is being cleaned. | 13 | — |
| [`app_start_replenish_clean_area`](cleaning-control.md#app_start_replenish_clean_area) | Sends the robot to clean extra zones that the user marked on the live map. | 10 | — |

## Remote control

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`app_rc_start`](remote-control.md#app_rc_start) | Puts the robot into manual mode. | all 42 | — |
| [`app_rc_move`](remote-control.md#app_rc_move) | Sets linear and angular velocity for a limited time; must be repeated to keep moving. | all 42 | — |
| [`app_rc_end`](remote-control.md#app_rc_end) | Ends manual mode. | all 42 | — |
| [`app_rc_stop`](remote-control.md#app_rc_stop) | Sent when the user releases the control. | 39 | — |

## Status, properties and capabilities

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`get_prop`](status.md#get_prop) | The plugin calls it only as `get_prop ["get_status"]`; the reply's first array element is the status object. | all 42 | — |
| [`get_status`](status.md#get_status) | Listed in the Methods tables; in the plugin it is the *argument* of `get_prop`, never a method. | 0 | — |
| [`app_get_status`](status.md#app_get_status) | The `GetStatus` entry of the alternate (`saphire`) table; not active for any shipped bundle. | 0 | — |
| [`app_get_init_status`](status.md#app_get_init_status) | Called once when the plugin starts; delivers the robot location and the capability lists. | 38 | 4 / 0 |
| [`get_fw_features`](status.md#get_fw_features) | Returns the array of firmware feature codes; called only by the a01, c1, e2, s5 and v1 bundles. | 5 | 37 / 0 |
| [`get_serial_number`](status.md#get_serial_number) | Returns the robot serial number. | all 42 | — |
| [`app_get_locale`](status.md#app_get_locale) | Returns the location, language, time zone and related profile fields. | all 42 | — |
| [`get_testid`](status.md#get_testid) | Debug-page query returning `testid` and `vnid`. | 36 | — |
| [`app_stat`](status.md#app_stat) | Sends batches of UI-usage counters to the robot. | 41 | — |
| [`get_dock_info`](status.md#get_dock_info) | Reads dock details; used on debug and settings pages for dock type O4. | 16 | — |

## Fan power, water flow and mop modes

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`get_custom_mode`](cleaning-modes.md#get_custom_mode) | Returns the current fan power value. | 20 | 22 / 0 |
| [`set_custom_mode`](cleaning-modes.md#set_custom_mode) | Sets the fan power code. | all 42 | — |
| [`get_water_box_custom_mode`](cleaning-modes.md#get_water_box_custom_mode) | Returns the water box mode. | 4 | 38 / 0 |
| [`set_water_box_custom_mode`](cleaning-modes.md#set_water_box_custom_mode) | Sets the water box mode. | all 42 | — |
| [`get_clean_motor_mode`](cleaning-modes.md#get_clean_motor_mode) | Wrapped in 32 bundles (a08 a09 a10 a14 … a76, s4 s5e s6); no call site found. | 0 | 32 / 0 |
| [`set_clean_motor_mode`](cleaning-modes.md#set_clean_motor_mode) | Sets fan power and water mode (and mop mode) in one call. | 37 | — |
| [`set_mop_mode`](cleaning-modes.md#set_mop_mode) | Sets the mop mode code (`300`, `301`, `303`, `304`). | 32 | — |
| [`get_customize_clean_mode`](cleaning-modes.md#get_customize_clean_mode) | Returns the list of per-room ("customize clean mode") settings. | 38 | — |
| [`set_customize_clean_mode`](cleaning-modes.md#set_customize_clean_mode) | Writes the whole per-room list in one call. | 38 | — |
| [`get_custom_clean_time`](cleaning-modes.md#get_custom_clean_time) | Reads the maximum clean time setting; only in the oldest plugin generation. | 3 | — |
| [`set_custom_clean_time`](cleaning-modes.md#set_custom_clean_time) | Sets the maximum clean time in seconds. | 3 | — |
| [`set_clean_sequence`](cleaning-modes.md#set_clean_sequence) | Stores a custom order of room ids. | 34 | 1 / 0 |
| [`get_clean_sequence`](cleaning-modes.md#get_clean_sequence) | Returns the stored room order. | 34 | 1 / 0 |
| [`add_mop_template_params`](cleaning-modes.md#add_mop_template_params) | Adds a user-defined mop template (dock mop-washing parameters). | 22 | — |
| [`update_mop_template_params`](cleaning-modes.md#update_mop_template_params) | Replaces the parameters of an existing template. | 22 | — |
| [`del_mop_template_params`](cleaning-modes.md#del_mop_template_params) | Deletes a template by id. | 22 | — |
| [`sort_mop_template_params`](cleaning-modes.md#sort_mop_template_params) | Sets the display order of templates. | 22 | — |
| [`get_mop_template_params_by_id`](cleaning-modes.md#get_mop_template_params_by_id) | Returns the full parameters of one template. | 22 | — |
| [`get_mop_template_params_summary`](cleaning-modes.md#get_mop_template_params_summary) | Returns the template list. | 9 | 13 / 0 |
| [`set_mop_template_id`](cleaning-modes.md#set_mop_template_id) | Makes a template the active one. | 22 | — |
| [`set_water_box_distance_off`](cleaning-modes.md#set_water_box_distance_off) | Sets the custom water level used with water mode 207. | 22 | — |
| [`set_corner_clean_mode`](cleaning-modes.md#set_corner_clean_mode) | Switches the corner-cleaning option. | 10 | — |
| [`get_mop_motor_status`](cleaning-modes.md#get_mop_motor_status) | Reads the "layer mode" of the mop motor. | 4 | 21 / 0 |
| [`set_mop_motor_status`](cleaning-modes.md#set_mop_motor_status) | Sets the mop motor "layer mode". | 4 | 21 / 0 |
| [`get_mop_reverse_pwm_values`](cleaning-modes.md#get_mop_reverse_pwm_values) | Reads a debug parameter page value. | 13 | — |
| [`set_mop_reverse_pwm_values`](cleaning-modes.md#set_mop_reverse_pwm_values) | Writes the debug value. | 13 | — |
| [`set_fan_motor_work_timeout`](cleaning-modes.md#set_fan_motor_work_timeout) | Sets the fan "air drying" timeout in minutes (0 disables). | 25 | — |
| [`get_fan_motor_work_timeout`](cleaning-modes.md#get_fan_motor_work_timeout) | Reads the configured timeout. | 25 | — |
| [`stop_fan_motor_work`](cleaning-modes.md#stop_fan_motor_work) | Stops a running air-dry (also wrapped as `stopAirdryMop`). | 22 | — |
| [`set_clean_follow_ground_material_status`](cleaning-modes.md#set_clean_follow_ground_material_status) | Switches "follow floor material direction" cleaning. | 16 | — |
| [`get_clean_follow_ground_material_status`](cleaning-modes.md#get_clean_follow_ground_material_status) | Reads the switch. | 16 | — |

## Maps and multi-floor maps

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`get_map`](maps.md#get_map) | Raw map request used by the newest plugin generation through an encrypted/compressed path. | 22 | 0 / 17 |
| [`get_map_v1`](maps.md#get_map_v1) | The standard map request; the reply names the file to download. | 39 | 0 / 3 |
| [`get_map_v2`](maps.md#get_map_v2) | Listed in every Methods table; never called. | 0 | 0 / 42 |
| [`app_get_map`](maps.md#app_get_map) | The `GetMap` entry of the `saphire`/`tanos` table; no call site. | 0 | 0 / 3 |
| [`get_fresh_map`](maps.md#get_fresh_map) | Declared in 41 bundles; never called (the s5 bundle calls the `_v1` variant). | 0 | 0 / 41 |
| [`get_fresh_map_v1`](maps.md#get_fresh_map_v1) | Map request for the "new map" candidate; only the s5 bundle contains the call. | 2 | — |
| [`get_persist_map`](maps.md#get_persist_map) | Declared in 41 bundles; never called. | 0 | 0 / 41 |
| [`get_persist_map_v1`](maps.md#get_persist_map_v1) | Saved-map request; only the s5 bundle contains the call. | 2 | — |
| [`get_photo`](maps.md#get_photo) | Fetches a photo taken by the robot (obstacle recognition). | 33 | — |
| [`get_random_pkey`](maps.md#get_random_pkey) | Returns a public key used for encrypted record data. | 32 | — |
| [`get_multi_map`](maps.md#get_multi_map) | Downloads one saved map of a multi-floor setup. | 38 | — |
| [`get_multi_maps_list`](maps.md#get_multi_maps_list) | Returns the saved maps and the maximum number of floors. | 38 | — |
| [`load_multi_map`](maps.md#load_multi_map) | Makes a saved map the active one. | 38 | — |
| [`name_multi_map`](maps.md#name_multi_map) | Sets the name of a saved map. | 38 | — |
| [`recover_multi_map`](maps.md#recover_multi_map) | Restores a saved floor map from its backup copy. | 22 | 0 / 16 |
| [`save_map`](maps.md#save_map) | Writes map edits: virtual walls, forbidden zones and, with multi-floor, the target map. | all 42 | — |
| [`reset_map`](maps.md#reset_map) | Deletes the current map on the robot. | all 42 | — |
| [`start_edit_map`](maps.md#start_edit_map) | Tells the robot that the app edits the map. | all 42 | — |
| [`end_edit_map`](maps.md#end_edit_map) | Ends the session (also called when leaving without saving). | all 42 | — |
| [`use_new_map`](maps.md#use_new_map) | s5-generation "new map / old map" choice: keep the new map. | 2 | 0 / 40 |
| [`use_old_map`](maps.md#use_old_map) | Counterpart of `use_new_map`. | 2 | 0 / 40 |
| [`get_recover_map`](maps.md#get_recover_map) | Downloads the map of a backup entry for preview. | all 42 | — |
| [`get_recover_maps`](maps.md#get_recover_maps) | Returns the restorable map versions. | all 42 | — |
| [`recover_map`](maps.md#recover_map) | Restores the chosen backup entry. | all 42 | — |
| [`del_map`](maps.md#del_map) | Deletes a saved floor map. | all 42 | — |
| [`get_map_status`](maps.md#get_map_status) | Wrapped in every newer bundle; no call site. The map status is taken from the status field `map_status`. | 0 | 42 / 0 |
| [`set_switch_map_mode`](maps.md#set_switch_map_mode) | Turns automatic switching between saved maps on or off. | 22 | — |
| [`manual_bak_map`](maps.md#manual_bak_map) | Creates a manual backup of a saved floor map. | 22 | — |
| [`app_update_unsave_map`](maps.md#app_update_unsave_map) | Tells the robot what to do with a map it did not save. | 22 | — |
| [`get_dynamic_map_diff`](maps.md#get_dynamic_map_diff) | Asks which map layers changed since a nonce. | 16 | — |
| [`get_dynamic_data`](maps.md#get_dynamic_data) | Fetches the changed data of one map layer. | 16 | — |
| [`get_offline_map_status`](maps.md#get_offline_map_status) | Wrapped; no call site (the app keeps the state locally). | 0 | 16 / 0 |
| [`set_offline_map_status`](maps.md#set_offline_map_status) | Enables or disables offline map storage. | 16 | — |
| [`set_lab_status`](maps.md#set_lab_status) | Turns map saving (and multi-floor maps) on or off. | all 42 | — |
| [`set_map_beautification_status`](maps.md#set_map_beautification_status) | Writes a bit mask of experimental map-display options. | 25 | — |
| [`get_map_beautification_status`](maps.md#get_map_beautification_status) | Reads the mask. | 25 | — |

## Rooms, zones and map objects

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`get_room_mapping`](rooms-and-areas.md#get_room_mapping) | Returns, per room, the segment number and the room id of the cloud/IoT room it is assigned to. | all 42 | — |
| [`merge_segment`](rooms-and-areas.md#merge_segment) | Merges the selected rooms into one. | all 42 | — |
| [`split_segment`](rooms-and-areas.md#split_segment) | Splits a room along a line drawn in the editor. | all 42 | — |
| [`name_segment`](rooms-and-areas.md#name_segment) | Writes the room names (via room tags) to the robot. | all 42 | — |
| [`manual_segment_map`](rooms-and-areas.md#manual_segment_map) | Turns the automatic room division of a map into a manual (editable) one. | 40 | 2 / 0 |
| [`get_segment_status`](rooms-and-areas.md#get_segment_status) | Wrapped in every bundle; no call site. | 0 | 42 / 0 |
| [`set_scenes_segments`](rooms-and-areas.md#set_scenes_segments) | Registers a smart-scene task for rooms. | 22 | — |
| [`set_scenes_zones`](rooms-and-areas.md#set_scenes_zones) | Registers a smart-scene task for rectangular zones. | 22 | — |
| [`get_scenes_valid_tids`](rooms-and-areas.md#get_scenes_valid_tids) | Returns the task ids the robot knows. | 22 | — |
| [`reunion_scenes`](rooms-and-areas.md#reunion_scenes) | Tells the robot which task ids are valid on the cloud side. | 22 | — |
| [`save_furnitures`](rooms-and-areas.md#save_furnitures) | Writes the edited furniture list of a map. | 22 | — |
| [`set_identify_furniture_status`](rooms-and-areas.md#set_identify_furniture_status) | Turns furniture recognition on or off. | 22 | — |
| [`get_identify_furniture_status`](rooms-and-areas.md#get_identify_furniture_status) | Reads the switch. | 22 | — |
| [`set_segment_ground_material`](rooms-and-areas.md#set_segment_ground_material) | Stores the floor type per room. | 22 | — |
| [`set_identify_ground_material_status`](rooms-and-areas.md#set_identify_ground_material_status) | Turns floor-material recognition on or off. | 22 | — |
| [`get_identify_ground_material_status`](rooms-and-areas.md#get_identify_ground_material_status) | Reads the switch. | 22 | — |
| [`set_ignore_identify_area`](rooms-and-areas.md#set_ignore_identify_area) | Marks recognised obstacles as ignored. | 34 | — |
| [`set_carpet_area`](rooms-and-areas.md#set_carpet_area) | Saves user-added carpet zones. | 22 | — |
| [`set_ignore_carpet_zone`](rooms-and-areas.md#set_ignore_carpet_zone) | Saves zones where carpet detection is ignored. | 32 | — |
| [`app_set_door_sill_blocks`](rooms-and-areas.md#app_set_door_sill_blocks) | Saves manual door-sill (threshold) blocks. | 16 | — |
| [`app_set_smart_door_sill`](rooms-and-areas.md#app_set_smart_door_sill) | Saves the automatic door-sill areas. | 16 | — |
| [`app_set_ignore_stuck_point`](rooms-and-areas.md#app_set_ignore_stuck_point) | Saves points where the robot's stuck detection is ignored. | 16 | — |
| [`app_set_smart_cliff_forbidden`](rooms-and-areas.md#app_set_smart_cliff_forbidden) | Saves areas treated as cliff-forbidden. | 16 | — |

## Carpet handling

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`get_carpet_mode`](carpet.md#get_carpet_mode) | Returns the carpet-detection (pressurize) switch and thresholds. | all 42 | — |
| [`set_carpet_mode`](carpet.md#set_carpet_mode) | Switches carpet detection and writes its current thresholds. | all 42 | — |
| [`get_carpet_clean_mode`](carpet.md#get_carpet_clean_mode) | Returns the carpet behaviour mode. | 32 | — |
| [`set_carpet_clean_mode`](carpet.md#set_carpet_clean_mode) | Chooses what the robot does on carpets. | 32 | — |
| [`app_get_carpet_deep_clean_status`](carpet.md#app_get_carpet_deep_clean_status) | Reads the "carpet deep clean" switch. | 16 | — |
| [`app_set_carpet_deep_clean_status`](carpet.md#app_set_carpet_deep_clean_status) | Switches deep cleaning of carpets. | 16 | — |
| [`app_set_priority_carpet_cleaning_status`](carpet.md#app_set_priority_carpet_cleaning_status) | Switches "carpet first" ordering; the status field `switch_status` bit 3 reports it. | 13 | — |

## Timers and Do-Not-Disturb

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`get_timer`](timers.md#get_timer) | Returns all robot timers with their schedule and command. | all 42 | — |
| [`set_timer`](timers.md#set_timer) | Creates a timer that starts a clean. | all 42 | — |
| [`del_timer`](timers.md#del_timer) | Removes a timer by name. | all 42 | — |
| [`upd_timer`](timers.md#upd_timer) | Switches a timer on or off. | all 42 | — |
| [`get_server_timer`](timers.md#get_server_timer) | Returns the timers kept in the server store. | all 42 | — |
| [`set_server_timer`](timers.md#set_server_timer) | Creates a timer in the server store (used for FCC state 1). | 39 | 3 / 0 |
| [`del_server_timer`](timers.md#del_server_timer) | Deletes server timers by name. | all 42 | — |
| [`upd_server_timer`](timers.md#upd_server_timer) | Switches a server timer. | 39 | 3 / 0 |
| [`get_timer_summary`](timers.md#get_timer_summary) | Returns the names of all robot timers. | 37 | — |
| [`get_timer_detail`](timers.md#get_timer_detail) | Returns the full entry of a timer. | 37 | — |
| [`get_dnd_timer`](timers.md#get_dnd_timer) | Returns the DND window and, on newer firmware, its actions. | all 42 | — |
| [`set_dnd_timer`](timers.md#set_dnd_timer) | Sets and enables the DND window. | all 42 | — |
| [`close_dnd_timer`](timers.md#close_dnd_timer) | Disables DND. | all 42 | — |
| [`set_dnd_timer_actions`](timers.md#set_dnd_timer_actions) | Chooses what is suppressed or resumed during DND. | 21 | — |
| [`get_valley_electricity_timer`](timers.md#get_valley_electricity_timer) | Returns the "valley electricity" charging window. | 22 | — |
| [`set_valley_electricity_timer`](timers.md#set_valley_electricity_timer) | Sets the window. | 22 | — |
| [`close_valley_electricity_timer`](timers.md#close_valley_electricity_timer) | Disables the window. | 22 | — |

## Consumables

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`get_consumable`](consumables.md#get_consumable) | Returns the wear counters of brushes, filters and sensors. | all 42 | — |
| [`reset_consumable`](consumables.md#reset_consumable) | Resets the counter named by the parameter. | all 42 | — |

## Cleaning history

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`get_clean_summary`](clean-history.md#get_clean_summary) | Returns the lifetime totals and the ids of the stored records. | all 42 | — |
| [`get_clean_record`](clean-history.md#get_clean_record) | Returns the details of the run that started at the given time. | all 42 | — |
| [`get_clean_record_map`](clean-history.md#get_clean_record_map) | Downloads the map and path of a record (same file mechanism as the live map). | all 42 | — |
| [`get_clean_record_map_v2`](clean-history.md#get_clean_record_map_v2) | Declared in every Methods table; never called. | 0 | 0 / 42 |
| [`del_clean_record`](clean-history.md#del_clean_record) | Deletes the record with the given start time. | all 42 | — |
| [`clear_clean_records`](clean-history.md#clear_clean_records) | Deletes the whole history; only the a01-family bundles (a01, c1, e2) call it. | 3 | — |
| [`app_get_clean_estimate_info`](clean-history.md#app_get_clean_estimate_info) | Polled every 5 s by the "clean estimate" page. | 21 | — |

## Sound, voice packs and voice features

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`get_sound_volume`](sound.md#get_sound_volume) | Returns the current speaker volume. | all 42 | — |
| [`change_sound_volume`](sound.md#change_sound_volume) | Sets the speaker volume. | all 42 | — |
| [`test_sound_volume`](sound.md#test_sound_volume) | Makes the robot play a sound at the current volume. | all 42 | — |
| [`get_current_sound`](sound.md#get_current_sound) | Returns which voice pack is installed. | all 42 | — |
| [`dnld_install_sound`](sound.md#dnld_install_sound) | Orders the robot to download and install a pack. | 39 | — |
| [`get_sound_progress`](sound.md#get_sound_progress) | Polled every second during an installation. | all 42 | — |
| [`play_audio`](sound.md#play_audio) | Sends an audio clip to be played by the robot. | 32 | — |
| [`set_voice_chat_volume`](sound.md#set_voice_chat_volume) | Sets the volume used during a call. | 21 | — |
| [`start_voice_chat`](sound.md#start_voice_chat) | Opens the robot audio channel for a call. | 22 | — |
| [`stop_voice_chat`](sound.md#stop_voice_chat) | Closes the audio channel. | 22 | — |
| [`enable_homesec_voice`](sound.md#enable_homesec_voice) | Turns the robot microphone on or off for the monitoring feature. | 22 | — |

## Dock (auto-empty, mop washing and drying)

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`app_start_wash`](dock.md#app_start_wash) | Starts the mop-washing routine at the dock. | 22 | — |
| [`app_stop_wash`](dock.md#app_stop_wash) | Stops a running wash. | 22 | — |
| [`app_start_collect_dust`](dock.md#app_start_collect_dust) | Starts auto-empty. | 32 | — |
| [`app_stop_collect_dust`](dock.md#app_stop_collect_dust) | Stops auto-empty. | 32 | — |
| [`get_dust_collection_mode`](dock.md#get_dust_collection_mode) | Returns the auto-empty mode. | 25 | — |
| [`set_dust_collection_mode`](dock.md#set_dust_collection_mode) | Sets the auto-empty mode. | 25 | — |
| [`get_dust_collection_switch_status`](dock.md#get_dust_collection_switch_status) | Returns whether automatic emptying is on. | 25 | — |
| [`set_dust_collection_switch_status`](dock.md#set_dust_collection_switch_status) | Turns automatic emptying on or off. | 25 | — |
| [`get_wash_towel_mode`](dock.md#get_wash_towel_mode) | Returns the dock mop-wash mode. | 22 | — |
| [`set_wash_towel_mode`](dock.md#set_wash_towel_mode) | Sets the mop-wash mode. | 22 | — |
| [`get_wash_towel_params`](dock.md#get_wash_towel_params) | Older variant of the mop-wash settings page (`getWashTowel`). | 1 | 21 / 0 |
| [`set_wash_towel_params`](dock.md#set_wash_towel_params) | Sets the mode, status or interval of the older wash page. | 1 | 21 / 0 |
| [`get_smart_wash_params`](dock.md#get_smart_wash_params) | Returns the smart mid-clean wash setting. | 22 | — |
| [`set_smart_wash_params`](dock.md#set_smart_wash_params) | Turns "smart" mid-clean mop washing on/off and sets the interval. | 22 | — |
| [`app_get_dryer_setting`](dock.md#app_get_dryer_setting) | Returns the dryer configuration. | 22 | — |
| [`app_set_dryer_setting`](dock.md#app_set_dryer_setting) | Sets the drying time and status. | 22 | — |
| [`app_set_dryer_status`](dock.md#app_set_dryer_status) | Starts or stops mop drying immediately. | 22 | — |
| [`set_airdry_hours`](dock.md#set_airdry_hours) | Wrapper `setAirdryDuration`; no call site found. | 0 | 32 / 0 |
| [`stop_airdry_mop`](dock.md#stop_airdry_mop) | Wrapped as `stopAirdryMop` in 10 bundles (a08 a09 a10 a14 a15 a19 a23 s4 s5e s6); newer bundles name the same… | 0 | 10 / 0 |
| [`app_amethyst_self_check`](dock.md#app_amethyst_self_check) | Runs the dock self-diagnosis. | 21 | — |
| [`app_amethyst_drain_all_water`](dock.md#app_amethyst_drain_all_water) | Drains the dock water tanks. | 13 | — |
| [`app_empty_inbuilt_water_tank`](dock.md#app_empty_inbuilt_water_tank) | Drains the robot-side tank at the dock (wrapper `appAmethystDrainLeftWater`). | 13 | — |
| [`app_get_amethyst_status`](dock.md#app_get_amethyst_status) | Reads the "smart change water" switch. | 1 | 19 / 0 |
| [`app_set_amethyst_status`](dock.md#app_set_amethyst_status) | Sets the switch. | 1 | 19 / 0 |
| [`update_dock`](dock.md#update_dock) | Orders a dock firmware update. | 16 | — |
| [`get_wash_debug_params`](dock.md#get_wash_debug_params) | Wrapper only; no call site. | 0 | 22 / 0 |
| [`set_wash_debug_params`](dock.md#set_wash_debug_params) | Wrapper only; four separate wrappers set one key each. | 0 | 22 / 0 |
| [`get_auto_delivery_cleaning_fluid`](dock.md#get_auto_delivery_cleaning_fluid) | Reads the switch. | 16 | — |
| [`set_auto_delivery_cleaning_fluid`](dock.md#set_auto_delivery_cleaning_fluid) | Turns automatic dosing on or off. | 16 | — |
| [`clean_roller`](dock.md#clean_roller) | Starts or stops the mop-roller cleaning (the older name of the wash action). | 10 | — |

## Device settings

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`get_led_status`](device-settings.md#get_led_status) | Reads the LED switch. | all 42 | — |
| [`set_led_status`](device-settings.md#set_led_status) | Switches the robot status LED. | all 42 | — |
| [`get_flow_led_status`](device-settings.md#get_flow_led_status) | Reads the "flow" LED switch. | 25 | — |
| [`set_flow_led_status`](device-settings.md#set_flow_led_status) | Switches the flow LED. | 25 | — |
| [`get_child_lock_status`](device-settings.md#get_child_lock_status) | Reads the child-lock switch (status field `lock_status` also reports it). | 32 | — |
| [`set_child_lock_status`](device-settings.md#set_child_lock_status) | Switches the child lock. | 32 | — |
| [`get_collision_avoid_status`](device-settings.md#get_collision_avoid_status) | Reads the "avoid collision" (bumper-sensor) switch. | 25 | — |
| [`set_collision_avoid_status`](device-settings.md#set_collision_avoid_status) | Switches the setting. | 25 | — |

## Camera, live view and home security

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`get_camera_status`](camera.md#get_camera_status) | Returns a bit field with the camera-related switches. | 37 | — |
| [`set_camera_status`](camera.md#set_camera_status) | Writes the whole bit field. | 37 | — |
| [`start_camera_preview`](camera.md#start_camera_preview) | Starts the camera stream on the robot. | 34 | — |
| [`stop_camera_preview`](camera.md#stop_camera_preview) | Stops the stream. | 34 | — |
| [`get_turn_server`](camera.md#get_turn_server) | Returns relay information for the live view. | 34 | — |
| [`send_sdp_to_robot`](camera.md#send_sdp_to_robot) | Sends the app side session description. | 34 | — |
| [`send_ice_to_robot`](camera.md#send_ice_to_robot) | Sends one candidate. | 34 | — |
| [`get_device_sdp`](camera.md#get_device_sdp) | Polled every 500 ms (default) until the robot has answered. | 34 | — |
| [`get_device_ice`](camera.md#get_device_ice) | Polled every 500 ms (default). | 34 | — |
| [`switch_video_quality`](camera.md#switch_video_quality) | Chooses the stream definition. | 34 | — |
| [`switch_water_mark`](camera.md#switch_water_mark) | Turns the watermark on or off. | 22 | — |
| [`set_homesec_password`](camera.md#set_homesec_password) | Enables, changes or disables the gesture password protecting the live view. | 34 | — |
| [`reset_homesec_password`](camera.md#reset_homesec_password) | Removes the password. | 34 | — |
| [`check_homesec_password`](camera.md#check_homesec_password) | Checks a password. | 34 | — |
| [`get_homesec_connect_status`](camera.md#get_homesec_connect_status) | Returns the client id of the current monitoring session. | 32 | 1 / 0 |
| [`upload_photo`](camera.md#upload_photo) | Sends the user's classification of a robot photo back to the robot/cloud. | 32 | — |

## Network, time, firmware and logs

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`get_network_info`](system.md#get_network_info) | Returns SSID, signal strength, IP and MAC address. | all 42 | — |
| [`app_get_wifi_list`](system.md#app_get_wifi_list) | Returns the networks stored on the robot. | 16 | — |
| [`app_delete_wifi`](system.md#app_delete_wifi) | Deletes a stored network. | 16 | — |
| [`get_timezone`](system.md#get_timezone) | Returns the robot's time zone name. | all 42 | — |
| [`set_timezone`](system.md#set_timezone) | Sets the robot's time zone. | all 42 | — |
| [`set_app_timezone`](system.md#set_app_timezone) | Sent at start-up so that the robot knows the phone's time zone and mobile country code. | all 42 | — |
| [`miIO.ota`](system.md#miIO.ota) | Starts an OTA with an explicit URL; only used by a debug page. | 3 | 22 / 0 |
| [`enable_log_upload`](system.md#enable_log_upload) | Tells the robot how much logging it may upload; sent when the privacy agreement is accepted. | all 42 | — |
| [`get_log_upload_status`](system.md#get_log_upload_status) | In every Methods table; no call site. | 0 | 0 / 42 |
| [`user_upload_log`](system.md#user_upload_log) | Asks the robot to upload its logs (the "report a problem" button). | 38 | 0 / 4 |
| [`upload_data_for_debug_mode`](system.md#upload_data_for_debug_mode) | Starts a debug data upload from the debug page. | 25 | — |
| [`set_fds_endpoint`](system.md#set_fds_endpoint) | Tells the robot which file-storage host to use for uploads (maps, logs). | all 42 | — |

## Diagnostic, test and internal commands

| Method | Summary | Called by | Wrapper / declared only |
|---|---|---|---|
| [`retry_request`](diagnostic.md#retry_request) | Used by the plugin's retry protocol to ask whether a deferred call has completed. | 0 | 25 / 0 |
| [`resolve_error`](diagnostic.md#resolve_error) | Tells the robot that the user has resolved an error condition (mostly dock errors). | 22 | — |
| [`set_ces_action`](diagnostic.md#set_ces_action) | Sends a demo `type` / `action` pair (name refers to CES 2022). | 13 | — |
| [`app_keep_easter_egg`](diagnostic.md#app_keep_easter_egg) | Periodic keep-alive of the easter-egg mode. | 22 | — |
| [`app_start_easter_egg`](diagnostic.md#app_start_easter_egg) | Starts the "egg attack" feature (state 30, text "scanning"). | 22 | — |
| [`app_set_dynamic_config`](diagnostic.md#app_set_dynamic_config) | Debug page: points the robot to a configuration file for testing. | 21 | — |
| [`test_do_speak`](diagnostic.md#test_do_speak) | Triggers a speech test (a72, a73 only). | 2 | — |
| [`test_get_enable_wakeup`](diagnostic.md#test_get_enable_wakeup) | Reads the wake-word switch. | 2 | — |
| [`test_set_enable_wakeup`](diagnostic.md#test_set_enable_wakeup) | Switches the wake-word. | 2 | — |
| [`test_get_move_in_place`](diagnostic.md#test_get_move_in_place) | Reads the switch. | 2 | — |
| [`test_set_move_in_place`](diagnostic.md#test_set_move_in_place) | Switches turning in place on voice commands. | 2 | — |
| [`test_get_voice_keep_seconds`](diagnostic.md#test_get_voice_keep_seconds) | Reads the duration the robot stays awake after the wake word. | 2 | — |
| [`test_set_voice_keep_seconds`](diagnostic.md#test_set_voice_keep_seconds) | Sets the duration. | 2 | — |

## Alternate (`user.*`) table

47 method strings with the `user.` prefix exist in the bundles; see [alternate table](alternate-table.md).
