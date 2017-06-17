# XiaomiRobotVacuumProtocol
Attempt to describe the Xiaomi Robot Vacuum Protocol

These commands are send using the Xiaomi [mi-home protocol](Protocol.md)

Applications implementing this protocol

* [Openhab](https://github.com/marcelrv/openhab2/tree/xiaomi-vacuum) (Java)
* [mirobo](https://github.com/rytilahti/python-mirobo)  (Python) 


## Commands

| Type | Command | Description |
| ------ | --------- | -----------| 
|    START_VACUUM | `app_start`| - | 
|    STOP_VACUUM | `app_stop`| - | 
|    START_SPOT | `app_spot`| - | 
|    PAUSE | `app_pause`| - | 
|    CHARGE | `app_charge`| - | 
|    FIND_ME | `find_me`| - | 
|    CONSUMABLES_GET | `get_consumable`| - | 
|    CONSUMABLES_RESET | `reset_consumable`| - | 
|    CLEAN_SUMMARY_GET | `get_clean_summary`| [Cleaning details](cleanSummary+detail.md) | 
|    CLEAN_RECORD_GET | `get_clean_record`| [Cleaning details](cleanSummary+detail.md) | 
|    CLEAN_RECORD_MAP_GET | `get_clean_record_map`| - | 
|    GET_MAP | `get_map_v1`| - | 
|    GET_STATUS | `get_status`| - | 
|    GET_SERIAL_NUMBER | `get_serial_number`| - | 
|    DND_GET | `get_dnd_timer`| - | 
|    DND_SET | `set_dnd_timer`| - | 
|    DND_CLOSE | `close_dnd_timer`| - | 
|    TIMER_SET | `set_timer`| - | 
|    TIMER_UPDATE | `upd_timer`| - | 
|    TIMER_GET | `get_timer`| - | 
|    TIMER_DEL | `del_timer`| - | 
|    SOUND_INSTALL | `dnld_install_sound`| - | 
|    SOUND_GET_CURRENT | `get_current_sound`| - | 
|    LOG_UPLOAD_GET | `get_log_upload_status`| - | 
|    LOG_UPLOAD_ENABLE | `enable_log_upload`| - | 
|    SET_MODE | `set_custom_mode`| - | 
|    GET_MODE | `get_custom_mode`| - | 


Suggestions & improvements very welcome!
