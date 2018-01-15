# Xiaomi Robot Vacuum Protocol
Attempt to describe the Xiaomi Robot Vacuum Protocol

These commands are send using the Xiaomi [mi-home protocol](Protocol.md)

Applications implementing this protocol

* [Openhab](https://github.com/marcelrv/openhab2/tree/xiaomi-vacuum) (Java)
* [mirobo](https://github.com/rytilahti/python-mirobo)  (Python) 
* [iobroker](https://github.com/ioBroker/ioBroker.mihome-vacuum/blob/master/README.md]) 


## Vacuum Commands

| Type | Command | Description |
| ------ | --------- | -----------| 
|    START_VACUUM | `app_start`| Start vacuuming | 
|    STOP_VACUUM | `app_stop`| Stop vacuuming | 
|    START_SPOT | `app_spot`| Start spot cleaning | 
|    PAUSE | `app_pause`| Pause cleaning | 
|    CHARGE | `app_charge`| Start charging | 
|    FIND_ME | `find_me`| Send findme | 
|    CONSUMABLES_GET | `get_consumable`| Get consumables status | 
|    CONSUMABLES_RESET | `reset_consumable`| Reset consumables | 
|    CLEAN_SUMMARY_GET | `get_clean_summary`| [Cleaning details](cleanSummary+detail.md) | 
|    CLEAN_RECORD_GET | `get_clean_record`| [Cleaning details](cleanSummary+detail.md) | 
|    CLEAN_RECORD_MAP_GET | `get_clean_record_map`| Get the map reference of a historical cleaning | 
|    GET_MAP | `get_map_v1`| [Get Map](getMap.md) | 
|    GET_STATUS | `get_status`| [Get Status information](StatusMessage.md) | 
|    GET_SERIAL_NUMBER | `get_serial_number`| [Get Serial #](getSerial.md) | 
|    DND_GET | `get_dnd_timer`| [Do Not Disturb Settings](dnd_timer.md) | 
|    DND_SET | `set_dnd_timer`| [Set the do not disturb timings](dnd_timer.md) | 
|    DND_CLOSE | `close_dnd_timer`| [Disable the do not disturb function](dnd_timer.md)  | 
|    TIMER_SET | `set_timer`| [Add a timer](Timer.md) | 
|    TIMER_UPDATE | `upd_timer`| [Activate/deactivate a timer](Timer.md) | 
|    TIMER_GET | `get_timer`| [Get Timers](Timer.md) | 
|    TIMER_DEL | `del_timer`| [Remove a timer](Timer.md) | 
|    TIMERZONE_GET | `get_timezone`| [Get timezone](Timezone.md) | 
|    TIMERZONE_SET | `set_timezone`| [Set timezone](Timezone.md) | 
|    SOUND_INSTALL | `dnld_install_sound`| [Voice pack installation](install_sound.md) | 
|    SOUND_GET_CURRENT | `get_current_sound` | [Current voice](CurrentVoice.md) | 
|    SOUND_GET_VOLUME | `get_sound_volume` | - |
|    LOG_UPLOAD_GET | `get_log_upload_status`| - | 
|    LOG_UPLOAD_ENABLE | `enable_log_upload`| - | 
|    SET_MODE | `set_custom_mode`| [Set the vacuum level](FanPower.md) | 
|    GET_MODE | `get_custom_mode`| [Get the vacuum level](FanPower.md) | 
|    REMOTE_START | `app_rc_start`| [Start remote control](remote_control.md)| 
|    REMOTE_END | `app_rc_end`| [End remote control](remote_control.md) | 
|    REMOTE_MOVE | `app_rc_move`| [Remote control move command](remote_control.md) | 
|    GET_GATEWAY | `get_gateway`| [Get current gatway](MiscCmds.md) | 


Robo Vacuum 2

| Type | Command | Description |
| ------ | --------- | -----------| 
|    START_ZONE | `app_zoned_clean`| [Start zone vacuum](app_zoned_clean.md) | 


## Generic MiIO Commands
| Type | Command | Description |
| ------ | --------- | -----------| 
|    INFO | `miIO.info`| [Get device info](miIOinfo.md) | 
|    ROUTER | `miIO.config_router`| Set Wifi settings of the device | 
|    OTA | `miIO.ota`| [Update firmware over air](miIOinfo.md)| 
|    OTA_PROG | `miIO.get_ota_progress`| [Update firmware over air Progress](miIOinfo.md)| 
|    OTA_STATE | `miIO.get_ota_state`| [Update firmware over air Status](miIOinfo.md) | 

Suggestions & improvements very welcome!
