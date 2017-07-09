# Xiaomi Robot Vacuum Protocol
Attempt to describe the Xiaomi Robot Vacuum Protocol

These commands are send using the Xiaomi [mi-home protocol](Protocol.md)

Applications implementing this protocol

* [Openhab](https://github.com/marcelrv/openhab2/tree/xiaomi-vacuum) (Java)
* [mirobo](https://github.com/rytilahti/python-mirobo)  (Python) 


## Commands

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
|    DND_SET | `set_dnd_timer`| Set the do not disturb timings | 
|    DND_CLOSE | `close_dnd_timer`| Disable the do not disturb function  | 
|    TIMER_SET | `set_timer`| Add a timer | 
|    TIMER_UPDATE | `upd_timer`| Activate/deactivate a timer | 
|    TIMER_GET | `get_timer`| [Get Timers](Get_timer.md) | 
|    TIMER_DEL | `del_timer`| Remove a timer | 
|    SOUND_INSTALL | `dnld_install_sound`| - | 
|    SOUND_GET_CURRENT | `get_current_sound`| [Current voice](CurrentVoice.md) | 
|    LOG_UPLOAD_GET | `get_log_upload_status`| - | 
|    LOG_UPLOAD_ENABLE | `enable_log_upload`| - | 
|    SET_MODE | `set_custom_mode`| set the vacuum level | 
|    GET_MODE | `get_custom_mode`| get the vacuum level | 
|    REMOTE_START | `app_rc_start`| Start remote control | 
|    REMOTE_END | `app_rc_end`| End remote control | 
|    REMOTE_MOVE | `app_rc_move`| Remote control move command | 



Suggestions & improvements very welcome!
