# Xiaomi Robot Vacuum Protocol

Attempt to describe the Xiaomi Robot Vacuum Protocol.

These commands are send using the Xiaomi [mi-home protocol](Protocol.md).

Applications implementing this protocol:

* [Openhab](https://github.com/openhab/openhab-addons/tree/2.5.x/bundles/org.openhab.binding.miio) (Java)
* [mirobo](https://github.com/rytilahti/python-miio)  (Python)
* [iobroker](https://github.com/iobroker-community-adapters/ioBroker.mihome-vacuum)

## Vacuum Commands

:warning: Depending on the model and firmware version, not all commands might be available.
The last columns indicate for which models the commands are available:

 1. All Mi Robot / Roborock Vacuum
 2. Mi Robot Vacuum (v1) and Mi Robot Vacuum v2 (s5) with firmware versions `3.3.9_003194` or newer
 3. Roborock Vacuum S5 Max (s5e)

| Type                     | Command                     | Description                                  |       :one:        |       :two:        |      :three:       |
| ------------------------ | --------------------------- | -------------------------------------------- | :----------------: | :----------------: | :----------------: |
| START_VACUUM             | `app_start`                 | Start vacuuming                              | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| STOP_VACUUM              | `app_stop`                  | Stop vacuuming                               | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| START_SPOT               | `app_spot`                  | Start spot cleaning                          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| ZONED_CLEAN_START        | `app_zoned_clean`           | [Start zone cleaning](zoned_clean.md)        |        :x:         | :heavy_check_mark: | :heavy_check_mark: |
| ZONED_CLEAN_RESUME       | `resume_zoned_clean`        | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| ZONED_CLEAN_STOP         | `stop_zoned_clean`          | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| SEGMENT_CLEAN_START      | `app_segment_clean`         | Start segment vacuum                         |        :x:         |        :x:         | :heavy_check_mark: |
| SEGMENT_CLEAN_RESUME     | `resume_segment_clean`      | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| SEGMENT_CLEAN_STOP       | `stop_segment_clean`        | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| GOTO_TARGET              | `app_goto_target`           | [Send vacuum to coordinates](goto_target.md) |        :x:         | :heavy_check_mark: | :heavy_check_mark: |
| PAUSE                    | `app_pause`                 | Pause cleaning                               | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| CHARGE                   | `app_charge`                | Start charging                               | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| WAKEUP_ROBOT             | `app_wakeup_robot`          | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| GET_LOCALE               | `app_get_locale`            | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| GET_INIT_STATUS          | `app_get_init_status`       | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| GET_STATUS               | `get_status`                | [Get status informations](status.md)         | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| GET_FW_FEATURES          | `get_fw_features`           | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| GET_SERIAL_NUMBER        | `get_serial_number`         | [Get serial number](serial_number.md)        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| SET_LAB_STATUS           | `set_lab_status`            | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| REMOTE_START             | `app_rc_start`              | [Start remote control](rc.md)                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| REMOTE_END               | `app_rc_end`                | [End remote control](rc.md)                  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| REMOTE_MOVE              | `app_rc_move`               | [Remote control move command](rc.md)         | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| FIND_ME                  | `find_me`                   | Send findme                                  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| CONSUMABLES_GET          | `get_consumable`            | [Get consumables status](consumable.md)      | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| CONSUMABLES_RESET        | `reset_consumable`          | [Reset consumables status](consumable.md)    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| CLEAN_SUMMARY_GET        | `get_clean_summary`         | [Cleaning details](clean_summary+record.md)  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| CLEAN_RECORD_GET         | `get_clean_record`          | [Cleaning details](clean_summary+record.md)  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| CLEAN_RECORD_DEL         | `del_clean_record`          | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| CLEAN_RECORD_MAP_GET     | `get_clean_record_map`      | Get map of a historical cleaning             | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| MAP_V1_GET               | `get_map_v1`                | [Get Map](map_v1.md)                         | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| MAP_V1_FRESH_GET         | `get_fresh_map_v1`          | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| MAP_V1_PERSIST_GET       | `get_persist_map_v1`        | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| MAP_RECOVER              | `recover_map`               | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| MAP_RESET                | `reset_map`                 | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| MAP_SAVE                 | `save_map`                  | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| MAP_EDIT_START           | `start_edit_map`            | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| MAP_EDIT_END             | `end_edit_map`              | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| MAP_USE_NEW              | `use_new_map`               | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| MAP_USE_OLD              | `use_old_map`               | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| MAP_STATUS_GET           | `get_map_status`            | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| MAP_RECOVER_GET          | `get_recover_map`           | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| MAPS_RECOVER_GET         | `get_recover_maps`          | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| DND_GET                  | `get_dnd_timer`             | [Do not disturb settings](dnd_timer.md)      | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| DND_SET                  | `set_dnd_timer`             | [Set DND timings](dnd_timer.md)              | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| DND_CLOSE                | `close_dnd_timer`           | [Disable DND function](dnd_timer.md)         | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| TIMER_GET                | `get_timer`                 | [Get timers](timer.md)                       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| TIMER_SET                | `set_timer`                 | [Add a timer](timer.md)                      | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| TIMER_UPDATE             | `upd_timer`                 | [De/activate a timer](timer.md)              | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| TIMER_DEL                | `del_timer`                 | [Remove a timer](timer.md)                   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| TIMER_SERVER_GET         | `get_server_timer`          | [Get timers](timer.md)                       |        :x:         |        :x:         | :heavy_check_mark: |
| TIMER_SERVER_SET         | `set_server_timer`          | [Add a timer](timer.md)                      |        :x:         |        :x:         | :heavy_check_mark: |
| TIMER_SERVER_UPDATE      | `upd_server_timer`          | [De/activate a timer](timer.md)              |        :x:         |        :x:         | :heavy_check_mark: |
| TIMER_SERVER_DEL         | `del_server_timer`          | [Remove a timer](timer.md)                   |        :x:         |        :x:         | :heavy_check_mark: |
| TIMEZONE_GET             | `get_timezone`              | [Get timezone](timezone.md)                  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| TIMEZONE_SET             | `set_timezone`              | [Set timezone](timezone.md)                  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| SOUND_INSTALL            | `dnld_install_sound`        | [Voice pack installation](install_sound.md)  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| SOUND_CURRENT_GET        | `get_current_sound`         | [Get current voice](current_sound.md)        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| SOUND_PROGRESS_GET       | `get_sound_progress`        | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| SOUND_VOLUME_GET         | `get_sound_volume`          | -                                            | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| SOUND_VOLUME_CHANGE      | `change_sound_volume`       | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| SOUND_VOLUME_TEST        | `test_sound_volume`         | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| LOG_UPLOAD_GET           | `get_log_upload_status`     | [Log upload](log_upload.md)                  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| LOG_UPLOAD_ENABLE        | `enable_log_upload`         | -                                            | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| LOG_UPLOAD_USER          | `user_upload_log`           | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| CUSTOM_MODE_GET          | `get_custom_mode`           | [Get vacuum level](custom_mode.md)           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| CUSTOM_MODE_SET          | `set_custom_mode`           | [Set vacuum level](custom_mode.md)           | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| CUSTOM_MODE_WATERBOX_GET | `get_water_box_custom_mode` | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| CUSTOM_MODE_WATERBOX_SET | `set_water_box_custom_mode` | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| CARPET_MODE_GET          | `get_carpet_mode`           | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| CARPET_MODE_SET          | `set_carpet_mode`           | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| SEGMENT_STATUS_GET       | `get_segment_status`        | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| SEGMENT_NAME             | `name_segment`              | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| SEGMENT_MERGE            | `merge_segment`             | -                                            |        :x:         |        :x:         | :heavy_check_mark: |
| SEGMENT_SPLIT            | `split_segment`             | -                                            |        :x:         |        :x:         | :heavy_check_mark: |

## Generic MiIO Commands

:information_source: These commands appear to be shared amngs all(?) Xiaomi Mi Io devices.

| Type       | Command                 | Description                                 |
| ---------- | ----------------------- | ------------------------------------------- |
| INFO       | `miIO.info`             | [Get device info](miIO-info.md)             |
| ROUTER     | `miIO.config_router`    | Set Wifi settings of the device             |
| OTA        | `miIO.ota`              | [Update firmware over air](miIO-ota.md)     |
| OTA_PROG   | `miIO.get_ota_progress` | Update firmware over air Progress           |
| OTA_STATE  | `miIO.get_ota_state`    | Update firmware over air Status             |
| WIFI_STATE | `miIO.wifi_assoc_state` | [Get Wifi status](miIO-wifi_assoc_state.md) |

:exclamation: Suggestions & improvements very welcome!
