# Xiaomi Robot Vacuum Protocol

Attempt to describe the Xiaomi Robot Vacuum Protocol

These commands are send using the Xiaomi [mi-home protocol](Protocol.md)

Applications implementing this protocol

* [Openhab](https://github.com/openhab/openhab-addons/tree/2.5.x/bundles/org.openhab.binding.miio) (Java)
* [mirobo](https://github.com/rytilahti/python-miio)  (Python)
* [iobroker](https://github.com/iobroker-community-adapters/ioBroker.mihome-vacuum)

## Vacuum Commands

| Type                     | Command                     | Description                                         |
| ------------------------ | --------------------------- | --------------------------------------------------- |
| START_VACUUM             | `app_start`                 | Start vacuuming                                     |
| STOP_VACUUM              | `app_stop`                  | Stop vacuuming                                      |
| START_SPOT               | `app_spot`                  | Start spot cleaning                                 |
| ZONED_CLEAN_START        | `app_zoned_clean`           | [Start zone vacuum](app_zoned_clean.md)             |
| ZONED_CLEAN_RESUME       | `resume_zoned_clean`        | -                                                   |
| ZONED_CLEAN_STOP         | `stop_zoned_clean`          | -                                                   |
| SEGMENT_CLEAN_START      | `app_segment_clean`         | Start segment vacuum                                |
| SEGMENT_CLEAN_RESUME     | `resume_segment_clean`      | -                                                   |
| SEGMENT_CLEAN_STOP       | `stop_segment_clean`        | -                                                   |
| GOTO_TARGET              | `app_goto_target`           | [Send vacuum to coordinates](app_goto_target.md)    |
| PAUSE                    | `app_pause`                 | Pause cleaning                                      |
| CHARGE                   | `app_charge`                | Start charging                                      |
| WAKEUP_ROBOT             | `app_wakeup_robot`          | -                                                   |
| GET_LOCALE               | `app_get_locale`            | -                                                   |
| GET_INIT_STATUS          | `app_get_init_status`       | -                                                   |
| GET_STATUS               | `get_status`                | [Get Status information](StatusMessage.md)          |
| GET_FW_FEATURES          | `get_fw_features`           | -                                                   |
| GET_SERIAL_NUMBER        | `get_serial_number`         | [Get Serial #](getSerial.md)                        |
| SET_LAB_STATUS           | `set_lab_status`            | -                                                   |
| REMOTE_START             | `app_rc_start`              | [Start remote control](remote_control.md)           |
| REMOTE_END               | `app_rc_end`                | [End remote control](remote_control.md)             |
| REMOTE_MOVE              | `app_rc_move`               | [Remote control move command](remote_control.md)    |
| FIND_ME                  | `find_me`                   | Send findme                                         |
| CONSUMABLES_GET          | `get_consumable`            | Get consumables status                              |
| CONSUMABLES_RESET        | `reset_consumable`          | Reset consumables                                   |
| CLEAN_SUMMARY_GET        | `get_clean_summary`         | [Cleaning details](cleanSummary+detail.md)          |
| CLEAN_RECORD_GET         | `get_clean_record`          | [Cleaning details](cleanSummary+detail.md)          |
| CLEAN_RECORD_DEL         | `del_clean_record`          | -                                                   |
| CLEAN_RECORD_MAP_GET     | `get_clean_record_map`      | Get the map reference of a historical cleaning      |
| MAP_V1_GET               | `get_map_v1`                | [Get Map](getMap.md)                                |
| MAP_V1_FRESH_GET         | `get_fresh_map_v1`          | -                                                   |
| MAP_V1_PERSIST_GET       | `get_persist_map_v1`        | -                                                   |
| MAP_RECOVER              | `recover_map`               | -                                                   |
| MAP_RESET                | `reset_map`                 | -                                                   |
| MAP_SAVE                 | `save_map`                  | -                                                   |
| MAP_EDIT_START           | `start_edit_map`            | -                                                   |
| MAP_EDIT_END             | `end_edit_map`              | -                                                   |
| MAP_USE_NEW              | `use_new_map`               | -                                                   |
| MAP_USE_OLD              | `use_old_map`               | -                                                   |
| MAP_STATUS_GET           | `get_map_status`            | -                                                   |
| MAP_RECOVER_GET          | `get_recover_map`           | -                                                   |
| MAPS_RECOVER_GET         | `get_recover_maps`          | -                                                   |
| DND_GET                  | `get_dnd_timer`             | [Do Not Disturb Settings](dnd_timer.md)             |
| DND_SET                  | `set_dnd_timer`             | [Set the do not disturb timings](dnd_timer.md)      |
| DND_CLOSE                | `close_dnd_timer`           | [Disable the do not disturb function](dnd_timer.md) |
| TIMER_GET                | `get_timer`                 | [Get Timers](Timer.md)                              |
| TIMER_SET                | `set_timer`                 | [Add a timer](Timer.md)                             |
| TIMER_UPDATE             | `upd_timer`                 | [Activate/deactivate a timer](Timer.md)             |
| TIMER_DEL                | `del_timer`                 | [Remove a timer](Timer.md)                          |
| TIMER_SERVER_GET         | `get_server_timer`          | -                                                   |
| TIMER_SERVER_SET         | `set_server_timer`          | -                                                   |
| TIMER_SERVER_UPDATE      | `upd_server_timer`          | -                                                   |
| TIMER_SERVER_DEL         | `del_server_timer`          | -                                                   |
| TIMEZONE_GET             | `get_timezone`              | [Get timezone](Timezone.md)                         |
| TIMEZONE_SET             | `set_timezone`              | [Set timezone](Timezone.md)                         |
| SOUND_INSTALL            | `dnld_install_sound`        | [Voice pack installation](install_sound.md)         |
| SOUND_CURRENT_GET        | `get_current_sound`         | [Current voice](CurrentVoice.md)                    |
| SOUND_PROGRESS_GET       | `get_sound_progress`        | -                                                   |
| SOUND_VOLUME_GET         | `get_sound_volume`          | -                                                   |
| SOUND_VOLUME_CHANGE      | `change_sound_volume`       | -                                                   |
| SOUND_VOLUME_TEST        | `test_sound_volume`         | -                                                   |
| LOG_UPLOAD_GET           | `get_log_upload_status`     | -                                                   |
| LOG_UPLOAD_ENABLE        | `enable_log_upload`         | -                                                   |
| LOG_UPLOAD_USER          | `user_upload_log`           | -                                                   |
| CUSTOM_MODE_GET          | `get_custom_mode`           | [Get the vacuum level](FanPower.md)                 |
| CUSTOM_MODE_SET          | `set_custom_mode`           | [Set the vacuum level](FanPower.md)                 |
| CUSTOM_MODE_WATERBOX_GET | `get_water_box_custom_mode` | -                                                   |
| CUSTOM_MODE_WATERBOX_SET | `set_water_box_custom_mode` | -                                                   |
| CARPET_MODE_GET          | `get_carpet_mode`           | -                                                   |
| CARPET_MODE_SET          | `set_carpet_mode`           | -                                                   |
| SEGMENT_STATUS_GET       | `get_segment_status`        | -                                                   |
| SEGMENT_NAME             | `name_segment`              | -                                                   |
| SEGMENT_MERGE            | `merge_segment`             | -                                                   |
| SEGMENT_SPLIT            | `split_segment`             | -                                                   |

:warning: Depending on the model and firmware version, not all commands might be available.

## Generic MiIO Commands

| Type       | Command                 | Description                                      |
| ---------- | ----------------------- | ------------------------------------------------ |
| INFO       | `miIO.info`             | [Get device info](miIOinfo.md)                   |
| ROUTER     | `miIO.config_router`    | Set Wifi settings of the device                  |
| OTA        | `miIO.ota`              | [Update firmware over air](miIOinfo.md)          |
| OTA_PROG   | `miIO.get_ota_progress` | [Update firmware over air Progress](miIOinfo.md) |
| OTA_STATE  | `miIO.get_ota_state`    | [Update firmware over air Status](miIOinfo.md)   |
| WIFI_STATE | `miIO.wifi_assoc_state` | -                                                |

Suggestions & improvements very welcome!
