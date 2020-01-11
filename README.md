# Xiaomi Robot Vacuum Protocol

Attempt to describe the Xiaomi Robot Vacuum Protocol.

These commands are send using the Xiaomi [mi-home protocol](Protocol.md).

Applications implementing this protocol:

* [Openhab](https://github.com/openhab/openhab-addons/tree/2.5.x/bundles/org.openhab.binding.miio) (Java)
* [mirobo](https://github.com/rytilahti/python-miio)  (Python)
* [iobroker](https://github.com/iobroker-community-adapters/ioBroker.mihome-vacuum)

Supported vacuum devices:

| Abb. | Names / aliases                                               |
| ---- | ------------------------------------------------------------- |
| c1   | Mi Xiaowa Vacuum c1                                           |
| m1s  | Mi Robot Vacuum 1S                                            |
| v1   | Mi Robot Vacuum                                               |
| s5   | Mi Robot Vacuum v2 / Roborock Vacuum S5 / Roborock Vacuum S50 |
| s6   | Roborock Vacuum S6                                            |
| s5e  | Roborock Vacuum S5 Max                                        |

## Vacuum Commands

:warning: Depending on the model and firmware version, not all commands might be available.
The last columns show for which models the commands are available (assumed the latest firmware is installed).
If there is no entry, the command is available for each device.

| Type                     | Command                     | Description                                  | Only available for |
| ------------------------ | --------------------------- | -------------------------------------------- | ------------------ |
| START_VACUUM             | `app_start`                 | Start vacuuming                              |                    |
| STOP_VACUUM              | `app_stop`                  | Stop vacuuming                               |                    |
| START_SPOT               | `app_spot`                  | Start spot cleaning                          |                    |
| ZONED_CLEAN_START        | `app_zoned_clean`           | [Start zone cleaning](zoned_clean.md)        | v1, s5, s6, s5e    |
| ZONED_CLEAN_RESUME       | `resume_zoned_clean`        | -                                            | s5e                |
| ZONED_CLEAN_STOP         | `stop_zoned_clean`          | -                                            | s5e                |
| SEGMENT_CLEAN_START      | `app_segment_clean`         | Start segment vacuum                         | s5e                |
| SEGMENT_CLEAN_RESUME     | `resume_segment_clean`      | -                                            | s5e                |
| SEGMENT_CLEAN_STOP       | `stop_segment_clean`        | -                                            | s5e                |
| GOTO_TARGET              | `app_goto_target`           | [Send vacuum to coordinates](goto_target.md) | v1, s5, s6, s5e    |
| PAUSE                    | `app_pause`                 | Pause cleaning                               |                    |
| CHARGE                   | `app_charge`                | Start charging                               |                    |
| WAKEUP_ROBOT             | `app_wakeup_robot`          | -                                            | s5e                |
| GET_LOCALE               | `app_get_locale`            | -                                            | s5e                |
| GET_INIT_STATUS          | `app_get_init_status`       | -                                            | s5e                |
| GET_STATUS               | `get_status`                | [Get status informations](status.md)         |                    |
| GET_FW_FEATURES          | `get_fw_features`           | -                                            | s5e                |
| GET_SERIAL_NUMBER        | `get_serial_number`         | [Get serial number](serial_number.md)        |                    |
| SET_LAB_STATUS           | `set_lab_status`            | -                                            | s5e                |
| REMOTE_START             | `app_rc_start`              | [Start remote control](rc.md)                |                    |
| REMOTE_END               | `app_rc_end`                | [End remote control](rc.md)                  |                    |
| REMOTE_MOVE              | `app_rc_move`               | [Remote control move command](rc.md)         |                    |
| FIND_ME                  | `find_me`                   | Send findme                                  |                    |
| CONSUMABLES_GET          | `get_consumable`            | [Get consumables status](consumable.md)      |                    |
| CONSUMABLES_RESET        | `reset_consumable`          | [Reset consumables status](consumable.md)    |                    |
| CLEAN_SUMMARY_GET        | `get_clean_summary`         | [Cleaning details](clean_summary+record.md)  |                    |
| CLEAN_RECORD_GET         | `get_clean_record`          | [Cleaning details](clean_summary+record.md)  |                    |
| CLEAN_RECORD_DEL         | `del_clean_record`          | -                                            | s5e                |
| CLEAN_RECORD_MAP_GET     | `get_clean_record_map`      | Get map of a historical cleaning             |                    |
| MAP_V1_GET               | `get_map_v1`                | [Get Map](map_v1.md)                         |                    |
| MAP_V1_FRESH_GET         | `get_fresh_map_v1`          | -                                            | s5e                |
| MAP_V1_PERSIST_GET       | `get_persist_map_v1`        | -                                            | s5e                |
| MAP_RECOVER              | `recover_map`               | -                                            | s5e                |
| MAP_RESET                | `reset_map`                 | -                                            | s5e                |
| MAP_SAVE                 | `save_map`                  | -                                            | s5e                |
| MAP_EDIT_START           | `start_edit_map`            | -                                            | s5e                |
| MAP_EDIT_END             | `end_edit_map`              | -                                            | s5e                |
| MAP_USE_NEW              | `use_new_map`               | -                                            | s5e                |
| MAP_USE_OLD              | `use_old_map`               | -                                            | s5e                |
| MAP_STATUS_GET           | `get_map_status`            | -                                            | s5e                |
| MAP_RECOVER_GET          | `get_recover_map`           | -                                            | s5e                |
| MAPS_RECOVER_GET         | `get_recover_maps`          | -                                            | s5e                |
| DND_GET                  | `get_dnd_timer`             | [Do not disturb settings](dnd_timer.md)      |                    |
| DND_SET                  | `set_dnd_timer`             | [Set DND timings](dnd_timer.md)              |                    |
| DND_CLOSE                | `close_dnd_timer`           | [Disable DND function](dnd_timer.md)         |                    |
| TIMER_GET                | `get_timer`                 | [Get timers](timer.md)                       |                    |
| TIMER_SET                | `set_timer`                 | [Add a timer](timer.md)                      |                    |
| TIMER_UPDATE             | `upd_timer`                 | [De/activate a timer](timer.md)              |                    |
| TIMER_DEL                | `del_timer`                 | [Remove a timer](timer.md)                   |                    |
| TIMER_SERVER_GET         | `get_server_timer`          | [Get timers](timer.md)                       | s5e                |
| TIMER_SERVER_SET         | `set_server_timer`          | [Add a timer](timer.md)                      | s5e                |
| TIMER_SERVER_UPDATE      | `upd_server_timer`          | [De/activate a timer](timer.md)              | s5e                |
| TIMER_SERVER_DEL         | `del_server_timer`          | [Remove a timer](timer.md)                   | s5e                |
| TIMEZONE_GET             | `get_timezone`              | [Get timezone](timezone.md)                  |                    |
| TIMEZONE_SET             | `set_timezone`              | [Set timezone](timezone.md)                  |                    |
| SOUND_INSTALL            | `dnld_install_sound`        | [Voice pack installation](install_sound.md)  |                    |
| SOUND_CURRENT_GET        | `get_current_sound`         | [Get current voice](current_sound.md)        |                    |
| SOUND_PROGRESS_GET       | `get_sound_progress`        | -                                            | s5e                |
| SOUND_VOLUME_GET         | `get_sound_volume`          | -                                            |                    |
| SOUND_VOLUME_CHANGE      | `change_sound_volume`       | -                                            | s5e                |
| SOUND_VOLUME_TEST        | `test_sound_volume`         | -                                            | s5e                |
| LOG_UPLOAD_GET           | `get_log_upload_status`     | [Log upload](log_upload.md)                  |                    |
| LOG_UPLOAD_ENABLE        | `enable_log_upload`         | -                                            |                    |
| LOG_UPLOAD_USER          | `user_upload_log`           | -                                            | s5e                |
| CUSTOM_MODE_GET          | `get_custom_mode`           | [Get vacuum level](custom_mode.md)           |                    |
| CUSTOM_MODE_SET          | `set_custom_mode`           | [Set vacuum level](custom_mode.md)           |                    |
| CUSTOM_MODE_WATERBOX_GET | `get_water_box_custom_mode` | -                                            | s5e                |
| CUSTOM_MODE_WATERBOX_SET | `set_water_box_custom_mode` | -                                            | s5e                |
| CARPET_MODE_GET          | `get_carpet_mode`           | -                                            | s5e                |
| CARPET_MODE_SET          | `set_carpet_mode`           | -                                            | s5e                |
| SEGMENT_STATUS_GET       | `get_segment_status`        | -                                            | s5e                |
| SEGMENT_NAME             | `name_segment`              | -                                            | s5e                |
| SEGMENT_MERGE            | `merge_segment`             | -                                            | s5e                |
| SEGMENT_SPLIT            | `split_segment`             | -                                            | s5e                |

## Generic MiIO Commands

:information_source: These commands appear to be shared amongs all(?) Xiaomi Mi Io devices.

| Type       | Command                 | Description                                 |
| ---------- | ----------------------- | ------------------------------------------- |
| INFO       | `miIO.info`             | [Get device info](miIO-info.md)             |
| ROUTER     | `miIO.config_router`    | Set Wifi settings of the device             |
| OTA        | `miIO.ota`              | [Update firmware over air](miIO-ota.md)     |
| OTA_PROG   | `miIO.get_ota_progress` | Update firmware over air Progress           |
| OTA_STATE  | `miIO.get_ota_state`    | Update firmware over air Status             |
| WIFI_STATE | `miIO.wifi_assoc_state` | [Get Wifi status](miIO-wifi_assoc_state.md) |

:exclamation: Suggestions & improvements very welcome!
