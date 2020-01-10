# Xiaomi Robot Vacuum Protocol

Attempt to describe the Xiaomi Robot Vacuum Protocol.

These commands are send using the Xiaomi [mi-home protocol](Protocol.md).

Applications implementing this protocol:

* [Openhab](https://github.com/openhab/openhab-addons/tree/2.5.x/bundles/org.openhab.binding.miio) (Java)
* [mirobo](https://github.com/rytilahti/python-miio)  (Python)
* [iobroker](https://github.com/iobroker-community-adapters/ioBroker.mihome-vacuum)

## Vacuum Commands

:warning: Depending on the model and firmware version, not all commands might be available.

| Type                     | Command                     | Description                                         |
| ------------------------ | --------------------------- | --------------------------------------------------- |
| START_VACUUM             | `app_start`                 | Start vacuuming                                     |
| STOP_VACUUM              | `app_stop`                  | Stop vacuuming                                      |
| START_SPOT               | `app_spot`                  | Start spot cleaning                                 |
| ZONED_CLEAN_START        | `app_zoned_clean`           | [Start zone vacuum](zoned_clean.md)                 |
| ZONED_CLEAN_RESUME       | `resume_zoned_clean`        | -                                                   |
| ZONED_CLEAN_STOP         | `stop_zoned_clean`          | -                                                   |
| SEGMENT_CLEAN_START      | `app_segment_clean`         | Start segment vacuum                                |
| SEGMENT_CLEAN_RESUME     | `resume_segment_clean`      | -                                                   |
| SEGMENT_CLEAN_STOP       | `stop_segment_clean`        | -                                                   |
| GOTO_TARGET              | `app_goto_target`           | [Send vacuum to coordinates](goto_target.md)        |
| PAUSE                    | `app_pause`                 | Pause cleaning                                      |
| CHARGE                   | `app_charge`                | Start charging                                      |
| WAKEUP_ROBOT             | `app_wakeup_robot`          | -                                                   |
| GET_LOCALE               | `app_get_locale`            | -                                                   |
| GET_INIT_STATUS          | `app_get_init_status`       | -                                                   |
| GET_STATUS               | `get_status`                | [Get Status information](status.md)                 |
| GET_FW_FEATURES          | `get_fw_features`           | -                                                   |
| GET_SERIAL_NUMBER        | `get_serial_number`         | [Get Serial #](serial_number.md)                    |
| SET_LAB_STATUS           | `set_lab_status`            | -                                                   |
| REMOTE_START             | `app_rc_start`              | [Start remote control](rc.md)                       |
| REMOTE_END               | `app_rc_end`                | [End remote control](rc.md)                         |
| REMOTE_MOVE              | `app_rc_move`               | [Remote control move command](rc.md)                |
| FIND_ME                  | `find_me`                   | Send findme                                         |
| CONSUMABLES_GET          | `get_consumable`            | [Get consumables status](consumable.md)             |
| CONSUMABLES_RESET        | `reset_consumable`          | Reset consumables                                   |
| CLEAN_SUMMARY_GET        | `get_clean_summary`         | [Cleaning details](clean_summary+record.md)         |
| CLEAN_RECORD_GET         | `get_clean_record`          | [Cleaning details](clean_summary+record.md)         |
| CLEAN_RECORD_DEL         | `del_clean_record`          | -                                                   |
| CLEAN_RECORD_MAP_GET     | `get_clean_record_map`      | Get the map reference of a historical cleaning      |
| MAP_V1_GET               | `get_map_v1`                | [Get Map](map_v1.md)                                |
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
| TIMER_GET                | `get_timer`                 | [Get Timers](timer.md)                              |
| TIMER_SET                | `set_timer`                 | [Add a timer](timer.md)                             |
| TIMER_UPDATE             | `upd_timer`                 | [Activate/deactivate a timer](timer.md)             |
| TIMER_DEL                | `del_timer`                 | [Remove a timer](timer.md)                          |
| TIMER_SERVER_GET         | `get_server_timer`          | -                                                   |
| TIMER_SERVER_SET         | `set_server_timer`          | -                                                   |
| TIMER_SERVER_UPDATE      | `upd_server_timer`          | -                                                   |
| TIMER_SERVER_DEL         | `del_server_timer`          | -                                                   |
| TIMEZONE_GET             | `get_timezone`              | [Get timezone](timezone.md)                         |
| TIMEZONE_SET             | `set_timezone`              | [Set timezone](timezone.md)                         |
| SOUND_INSTALL            | `dnld_install_sound`        | [Voice pack installation](install_sound.md)         |
| SOUND_CURRENT_GET        | `get_current_sound`         | [Current voice](current_sound.md)                   |
| SOUND_PROGRESS_GET       | `get_sound_progress`        | -                                                   |
| SOUND_VOLUME_GET         | `get_sound_volume`          | -                                                   |
| SOUND_VOLUME_CHANGE      | `change_sound_volume`       | -                                                   |
| SOUND_VOLUME_TEST        | `test_sound_volume`         | -                                                   |
| LOG_UPLOAD_GET           | `get_log_upload_status`     | [Log Upload](log_upload.md)                         |
| LOG_UPLOAD_ENABLE        | `enable_log_upload`         | -                                                   |
| LOG_UPLOAD_USER          | `user_upload_log`           | -                                                   |
| CUSTOM_MODE_GET          | `get_custom_mode`           | [Get the vacuum level](custom_mode.md)              |
| CUSTOM_MODE_SET          | `set_custom_mode`           | [Set the vacuum level](custom_mode.md)              |
| CUSTOM_MODE_WATERBOX_GET | `get_water_box_custom_mode` | -                                                   |
| CUSTOM_MODE_WATERBOX_SET | `set_water_box_custom_mode` | -                                                   |
| CARPET_MODE_GET          | `get_carpet_mode`           | -                                                   |
| CARPET_MODE_SET          | `set_carpet_mode`           | -                                                   |
| SEGMENT_STATUS_GET       | `get_segment_status`        | -                                                   |
| SEGMENT_NAME             | `name_segment`              | -                                                   |
| SEGMENT_MERGE            | `merge_segment`             | -                                                   |
| SEGMENT_SPLIT            | `split_segment`             | -                                                   |

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
