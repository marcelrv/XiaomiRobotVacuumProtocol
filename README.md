# Xiaomi Robot Vacuum Protocol

Attempt to describe the Xiaomi Robot Vacuum Protocol.

These commands are send using the Xiaomi [mi-home protocol](Protocol.md). (For decoding of the vacuum map see [RR Map File](RRMapFile))

Applications implementing this protocol:

* [Openhab](https://github.com/openhab/openhab-addons/tree/2.5.x/bundles/org.openhab.binding.miio) (Java)
* [mirobo](https://github.com/rytilahti/python-miio)  (Python)
* [iobroker](https://github.com/iobroker-community-adapters/ioBroker.mihome-vacuum) /  [iobroker roborock](https://github.com/copystring/ioBroker.roborock/) (javascript)

Supported vacuum devices:

| Model                 | Name / aliases                                               | 
| --------------------- | ------------------------------------------------------------ | 
| rockrobo.vacuum.v1    | Mi Robot Vacuum                                              | 
| roborock.vacuum.a01   | Roborock E Series                                            | 
| roborock.vacuum.a08   | Roborock S6 Pure                                             | 
| roborock.vacuum.a09   | Roborock T7 Pro                                              | 
| roborock.vacuum.a10   | Roborock S6 MaxV                                             | 
| roborock.vacuum.a11   | Roborock T7                                                  | 
| roborock.vacuum.a14   | Roborock T7S                                                 | 
| roborock.vacuum.a15   | Roborock S7                                                  | 
| roborock.vacuum.a19   | Roborock S4 Max                                              | 
| roborock.vacuum.a23   | Roborock T7S Plus                                            | 
| roborock.vacuum.c1    | Xiaowa C1                                                    | 
| roborock.vacuum.e2    | Roborock Xiaowa E Series                                     |
| roborock.vacuum.m1s   | Mi Robot Vacuum 1S                                           | 
| roborock.vacuum.p5    | Roborock P5                                                  | 
| roborock.vacuum.s4    | Roborock S4                                                  | 
| roborock.vacuum.s5    | Mi Robot Vacuum v2 / Roborock Vacuum S5 / Roborock Vacuum S50 | 
| roborock.vacuum.s5e   | Roborock S5 Max                                              | 
| roborock.vacuum.s6    | Roborock S6                                                  | 
| roborock.vacuum.t4    | Roborock T4                                                  | 
| roborock.vacuum.t6    | Roborock T6                                                  | 
| roborock.vacuum.t7    | Roborock Vacuum T7                                           | 


See [supported robots and capability matrix here](fw_features.md) (based on get_fw_features command)

## Vacuum Commands

:warning: Depending on the model and firmware version, not all commands might be available.  
The last columns show for which models the commands are available (assumed the latest firmware is installed).  
If there is no entry, the command is available for each device.  

| Type                     | Command                   | Documentation                                                                                                       | Only available for |
| ------------------------ | ------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------ |
| APPSTAT                  | app_stat                  |                                                                                                                     |                    |
| CARPET_MODE_GET          | get_carpet_mode           | \-                                                                                                                  | s5e                |
| CARPET_MODE_SET          | set_carpet_mode           | \-                                                                                                                  | s5e                |
| CHARGE                   | app_charge                | [Basic Operations](basic.md)                                                                                        |                    |
| CLEAN_RECORD_DEL         | del_clean_record          | \-                                                                                                                  | s5e                |
| CLEAN_RECORD_GET         | get_clean_record          | [Clean Summary](clean_summary+record.md)                                                                            |                    |
| CLEAN_RECORD_MAP_GET     | get_clean_record_map      | [Clean Summary](clean_summary+record.md)                                                                            |                    |
| CLEAN_SUMMARY_GET        | get_clean_summary         | [Clean Summary](clean_summary+record.md)                                                                            |                    |
| CONSUMABLES_GET          | get_consumable            | [Consumable](consumable.md)                                                                                         |                    |
| CONSUMABLES_RESET        | reset_consumable          | [Consumable](consumable.md)                                                                                         |                    |
| CUSTOM_MODE_GET          | get_custom_mode           | [Custom Mode](custom_mode.md)                                                                                       |                    |
| CUSTOM_MODE_SET          | set_custom_mode           | [Custom Mode](custom_mode.md)                                                                                       |                    |
| CUSTOM_MODE_WATERBOX_GET | get_water_box_custom_mode | [Water Box Custom Mode](water_box_custom_mode.md)                                                                   | s5e                |
| CUSTOM_MODE_WATERBOX_SET | set_water_box_custom_mode | [Water Box Custom Mode](water_box_custom_mode.md)                                                                   | s5e, s6            |
| DELETESELECTMAP          | del_map                   |                                                                                                                     |                    |
| DND_CLOSE                | close_dnd_timer           | [Do Not Disturb](dnd_timer.md)                                                                                      |                    |
| DND_GET                  | get_dnd_timer             | [Do Not Disturb](dnd_timer.md)                                                                                      |                    |
| DND_SET                  | set_dnd_timer             | [Do Not Disturb](dnd_timer.md)                                                                                      |                    |
| FIND_ME                  | find_me                   | [Find Robot](find_me.md)                                                                                            |                    |
| GETCLEANRECORDMAPV2      | get_clean_record_map_v2   |                                                                                                                     |                    |
| GETCUSTOMCLEANMODE       | get_customize_clean_mode  |                                                                                                                     |                    |
| GETFRESHMAP              | get_fresh_map             |                                                                                                                     |                    |
| GETLEDSTATUS             | get_led_status            |                                                                                                                     |                    |
| GETMAP                   | get_map                   |                                                                                                                     |                    |
| GETMAPV2                 | get_map_v2                |                                                                                                                     |                    |
| GETMULTIMAP              | get_multi_map             |                                                                                                                     |                    |
| GETPERSISTMAP            | get_persist_map           |                                                                                                                     |                    |
| GETPROP                  | get_prop                  |                                                                                                                     |                    |
| GETSERVERTIMER           | get_server_timer          |                                                                                                                     |                    |
| GETSTATUS                | app_get_status            |                                                                                                                     |                    |
| GET_FW_FEATURES          | get_fw_features           | [Firmware Features](fw_features.md)                                                                                 | s5e                |
| GET_INIT_STATUS          | app_get_init_status       | [Initial Status](init_status.md)                                                                                    | s5e                |
| GET_LOCALE               | app_get_locale            | [Locale Information](locale.md)                                                                                     | s5e                |
| GET_NETWORK_INFO         | get_network_info          | [Netwotk info](network_info.md)                                                                                     | s5e, s5, s7, s6    |
| GET_SERIAL_NUMBER        | get_serial_number         | [Serial Number](serial_number.md)                                                                                   |                    |
| GET_STATUS               | get_status                | [Status Message](status.md)                                                                                         |                    |
| GOTOTARGETSTOP           | stop_goto_target          |                                                                                                                     |                    |
| GOTO_TARGET              | app_goto_target           | [Goto Target](goto_target.md)                                                                                       | v1, s5, s6, s5e    |
| LOADMULTIMAP             | load_multi_map}           |                                                                                                                     |                    |
| LOG_UPLOAD_ENABLE        | enable_log_upload         | \-                                                                                                                  |                    |
| LOG_UPLOAD_GET           | get_log_upload_status     | [Log Upload](log_upload.md)                                                                                         |                    |
| LOG_UPLOAD_USER          | user_upload_log           | \-                                                                                                                  | s5e                |
| MANUALSEGMENTMAP         | manual_segment_map        |                                                                                                                     |                    |
| MAPS_GET_MULTI_MAPS      | get_multi_maps_list       | [Multimap](multimap.md)                                                                                             | s5e, s7, s6        |
| MAPS_LOAD_MULTI_MAP      | load_multi_map            | [Multimap](multimap.md)                                                                                             | s5e, s7, s6        |
| MAPS_RECOVER_GET         | get_recover_maps          | \-                                                                                                                  | s5e                |
| MAP_EDIT_END             | end_edit_map              | \-                                                                                                                  | s5e                |
| MAP_EDIT_START           | start_edit_map            | \-                                                                                                                  | s5e                |
| MAP_RECOVER              | recover_map               | \-                                                                                                                  | s5e                |
| MAP_RECOVER_GET          | get_recover_map           | \-                                                                                                                  | s5e                |
| MAP_RESET                | reset_map                 | \-                                                                                                                  | s5e                |
| MAP_SAVE                 | save_map                  | [Map](map.md)                                                                                                       | s5, s6, s5e        |
| MAP_STATUS_GET           | get_map_status            | \-                                                                                                                  | s5e                |
| MAP_USE_NEW              | use_new_map               | \-                                                                                                                  | s5e                |
| MAP_USE_OLD              | use_old_map               | \-                                                                                                                  | s5e                |
| MAP_V1_FRESH_GET         | get_fresh_map_v1          | \-                                                                                                                  | s5e                |
| MAP_V1_GET               | get_map_v1                | [Map V1](map_v1.md)                                                                                                 |                    |
| MAP_V1_PERSIST_GET       | get_persist_map_v1        | \-                                                                                                                  | s5e                |
| NAMEMULTIMAP             | name_multi_map            |                                                                                                                     |                    |
| PAUSE                    | app_pause                 | [Basic Operations](basic.md)                                                                                        |                    |
| RECOVERMULTIMAP          | recover_multi_map         |                                                                                                                     |                    |
| REMOTE_END               | app_rc_end                | [Remote Control](rc.md)                                                                                             |                    |
| REMOTE_MOVE              | app_rc_move               | [Remote Control](rc.md)                                                                                             |                    |
| REMOTE_START             | app_rc_start              | [Remote Control](rc.md)                                                                                             |                    |
| ROOM_MAPPING_GET         | get_room_mapping          | [Room Mapping](room_mapping.md)                                                                                     | s5e, m1s           |
| SEGMENT_CLEAN_RESUME     | resume_segment_clean      | [Segment Cleaning](segment_clean.md)                                                                                | s5e                |
| SEGMENT_CLEAN_START      | app_segment_clean         | [Segment Cleaning](segment_clean.md)                                                                                | s5, s5e, m1s       |
| SEGMENT_CLEAN_STOP       | stop_segment_clean        | [Segment Cleaning](segment_clean.md)                                                                                | s5e                |
| SEGMENT_MERGE            | merge_segment             | \-                                                                                                                  | s5e                |
| SEGMENT_NAME             | name_segment              | \-                                                                                                                  | s5e                |
| SEGMENT_SPLIT            | split_segment             | \-                                                                                                                  | s5e                |
| SEGMENT_STATUS_GET       | get_segment_status        | \-                                                                                                                  | s5e                |
| SETAPPTIMEZONE           | set_app_timezone          |                                                                                                                     |                    |
| SETCUSTOMCLEANMODE       | set_customize_clean_mode  |                                                                                                                     |                    |
| SETFDSENDPOINT           | set_fds_endpoint          |                                                                                                                     |                    |
| SETLEDSTATUS             | set_led_status            |                                                                                                                     |                    |
| SETSWITCHMAPMODE         | set_switch_map_mode       |                                                                                                                     |                    |
| SET_LAB_STATUS           | set_lab_status            | [Lab Status](lab_status.md)                                                                                         | s5, s6, s5e        |
| SOUND_CURRENT_GET        | get_current_sound         | [Current Sound](current_sound.md)                                                                                   |                    |
| SOUND_INSTALL            | dnld_install_sound        | [Voice Pack Installation](install_sound.md)                                                                         |                    |
| SOUND_PROGRESS_GET       | get_sound_progress        | [Voice Pack Installation](install_sound.md)                                                                         | s5e                |
| SOUND_VOLUME_CHANGE      | change_sound_volume       | [Sound Volume](sound_volume.md)                                                                                     | s5e                |
| SOUND_VOLUME_GET         | get_sound_volume          | [Sound Volume](sound_volume.md)                                                                                     |                    |
| SOUND_VOLUME_TEST        | test_sound_volume         | [Sound Volume](sound_volume.md)                                                                                     | s5e                |
| START_SPOT               | app_spot                  | [Basic Operations](basic.md)                                                                                        |                    |
| START_VACUUM             | app_start                 | [Basic Operations](basic.md)                                                                                        |                    |
| STOP_VACUUM              | app_stop                  | [Basic Operations](basic.md)                                                                                        |                    |
| TIMERSTART               | start_clean               |                                                                                                                     |                    |
| TIMER_DEL                | del_timer                 | [Cleaning Timer](timer.md)                                                                                          |                    |
| TIMER_GET                | get_timer                 | [Cleaning Timer](timer.md)                                                                                          |                    |
| TIMER_SERVER_DEL         | del_server_timer          | [Cleaning Timer](timer.md)                                                                                          | s5e                |
| TIMER_SERVER_GET         | get_server_timer          | [Cleaning Timer](timer.md)                                                                                          | s5e                |
| TIMER_SERVER_SET         | set_server_timer          | [Cleaning Timer](timer.md)                                                                                          | s5e                |
| TIMER_SERVER_UPDATE      | upd_server_timer          | [Cleaning Timer](timer.md)                                                                                          | s5e                |
| TIMER_SET                | set_timer                 | [Cleaning Timer](timer.md)                                                                                          |                    |
| TIMER_UPDATE             | upd_timer                 | [Cleaning Timer](timer.md)                                                                                          |                    |
| TIMEZONE_GET             | get_timezone              | [Timezone](timezone.md)                                                                                             |                    |
| TIMEZONE_SET             | set_timezone              | [Timezone](timezone.md)                                                                                             |                    |
| WAKEUP_ROBOT             | app_wakeup_robot          |                                                                                                                     | s5e                |
| ZONED_CLEAN_RESUME       | resume_zoned_clean        | [Zone Cleaning](zoned_clean.md)                                                                                     | s5e                |
| ZONED_CLEAN_START        | app_zoned_clean           | [Zone Cleaning](zoned_clean.md)                                                                                     | v1, s5, s6, s5e    |
| ZONED_CLEAN_STOP         | stop_zoned_clean          | [Zone Cleaning](zoned_clean.md)                                                                                     | s5e                |

## Generic MiIO Commands

:information_source: These commands appear to be shared amongs all(?) Xiaomi Mi Io devices.

| Type       | Command                 | Documentation                           |
| ---------- | ----------------------- | --------------------------------------- |
| INFO       | `miIO.info`             | [Info](miIO-info.md)                    |
| ROUTER     | `miIO.config_router`    | -                                       |
| OTA        | `miIO.ota`              | [Update Firmware Over Air](miIO-ota.md) |
| OTA_PROG   | `miIO.get_ota_progress` | -                                       |
| OTA_STATE  | `miIO.get_ota_state`    | -                                       |
| WIFI_STATE | `miIO.wifi_assoc_state` | [Wifi Status](miIO-wifi_assoc_state.md) |

## Ruby variant commands

There are few models that take the same commands but preponed with `user.`  
Below are the known ones:

| Type                    | Command                      |
| ----------------------- | ---------------------------- |
| GETMAP                  | user.app_get_map             |
| APPCHARGE               | user.app_home                |
| APPPAUSE                | user.app_pause               |
| APPREMOTECONTROLEND     | user.app_rc_end              |
| APPREMOTECONTROLMOVE    | user.app_rc_move             |
| APPREMOTECONTROLSTART   | user.app_rc_start            |
| APPSPOT                 | user.app_spot                |
| APPSTART                | user.app_start               |
| APPWAKEUPROBOT          | user.app_wakeup_robot        |
| CLOSEDNDTIMER           | user.close_dnd_timer         |
| DELTIMER                | user.del_timer               |
| ENABLELOGUPLOAD         | user.enable_log_upload       |
| FINDME                  | user.find_me                 |
| GETCARPETMODE           | user.get_carpet_mode         |
| GETCLEANRECORD          | user.get_clean_record        |
| GETCLEANRECORDMAP       | user.get_clean_record_map    |
| GETCLEANRECORDMAPV2     | user.get_clean_record_map_v2 |
| GETCLEANSUMMARY         | user.get_clean_summary       |
| GETCURRENTSOUNDPACKAGE  | user.get_current_sound       |
| GETCUSTOMMODE           | user.get_custom_mode         |
| GETDNDTIMER             | user.get_dnd_timer           |
| GETLOGUPLOADSTATUS      | user.get_log_upload_status   |
| GETMAPANDROID           | user.get_map_v1              |
| GETMAPV2                | user.get_map_v2              |
| GETSERIALNUMBER         | user.get_serial_number       |
| GETSOUNDPACKAGEPROGRESS | user.get_sound_progress      |
| GETSOUNDVOLUME          | user.get_sound_volume        |
| GETSUPPLIES             | user.get_consumable          |
| GETTIMER                | user.get_timer               |
| GETTIMEZONE             | user.get_timezone            |
| GOTOTARGET              | user.app_goto_target         |
| GOTOTARGETSTOP          | user.stop_goto_target        |
| RESETSUPPLIES           | user.reset_consumable        |
| RESUMEZONEDCLEAN        | user.app_resume_zoned_clean  |
| SETCARPETMODE           | user.set_carpet_mode         |
| SETCUSTOMMODE           | user.set_custom_mode         |
| SETDNDTIMER             | user.set_dnd_timer           |
| SETSOUNDPACKAGE         | user.dnld_install_sound      |
| SETSOUNDVOLUME          | user.change_sound_volume     |
| SETTIMER                | user.set_timer               |
| SETTIMEZONE             | user.set_timezone            |
| STARTZONEDCLEAN         | user.app_zoned_clean         |
| STOPZONEDCLEAN          | user.stop_zoned_clean        |
| TESTSOUNDVOLUME         | user.test_sound_volume       |
| TIMERSTART              | user.start_clean             |
| UPDTIMER                | user.upd_timer               |


:exclamation: Suggestions & improvements very welcome!
