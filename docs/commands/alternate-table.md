# The `user.*` method table

[Home](../../README.md) / [Commands](index.md) / Alternate table

Every bundle contains a second `Methods` table in which most method strings carry the prefix `user.` (and two differ otherwise: `app_home` instead of `app_charge`, `app_get_status` instead of `get_status`). The plugin selects it when the device model is in `saphireModelList`. The list read from the bundles (20 of 42 carry a readable list; the others were not matched) names the Xiaowa / Sapphire robots: `roborock.vacuum.e2`, `roborock.sweeper.e2v2`, `roborock.sweeper.e2v3`, `roborock.vacuum.c1`, `roborock.sweeper.c1v2`, `roborock.sweeper.c1v3`, and in the a01-family bundles also `a01`, `a01v2`, `a01v3`, `a04`, `a04v2`, `a04v3`. In the bundles outside the a01 family that were read (for example s5 and a15) the selection is `modelType == 'rubys' ? rubyMethods : saphireMethods`, so the `user.*` table is the table of that robot line. No analysed bundle is built for a model that activates it: the bundles of a01, c1 and e2 select a third table (`tanosMethods`) instead.

<!-- evidence on selection logic is written in concepts/transports.md -->

| Alternate method | Equivalent in default table | Active for a shipped bundle? |
|---|---|---|
| <a id="user.app_get_map"></a>`user.app_get_map` | `get_map / app_get_map` | no |
| <a id="user.app_goto_target"></a>`user.app_goto_target` | `app_goto_target` | no |
| <a id="user.app_home"></a>`user.app_home` | `app_charge` | no |
| <a id="user.app_pause"></a>`user.app_pause` | `app_pause` | no |
| <a id="user.app_rc_end"></a>`user.app_rc_end` | `app_rc_end` | no |
| <a id="user.app_rc_move"></a>`user.app_rc_move` | `app_rc_move` | no |
| <a id="user.app_rc_start"></a>`user.app_rc_start` | `app_rc_start` | no |
| <a id="user.app_resume_zoned_clean"></a>`user.app_resume_zoned_clean` | `resume_zoned_clean` | no |
| <a id="user.app_spot"></a>`user.app_spot` | `app_spot` | no |
| <a id="user.app_start"></a>`user.app_start` | `app_start` | no |
| <a id="user.app_wakeup_robot"></a>`user.app_wakeup_robot` | `app_wakeup_robot` | no |
| <a id="user.app_zoned_clean"></a>`user.app_zoned_clean` | `app_zoned_clean` | no |
| <a id="user.change_sound_volume"></a>`user.change_sound_volume` | `change_sound_volume` | no |
| <a id="user.close_dnd_timer"></a>`user.close_dnd_timer` | `close_dnd_timer` | no |
| <a id="user.del_timer"></a>`user.del_timer` | `del_timer` | no |
| <a id="user.dnld_install_sound"></a>`user.dnld_install_sound` | `dnld_install_sound` | yes (a01, c1, e2) |
| <a id="user.enable_log_upload"></a>`user.enable_log_upload` | `enable_log_upload` | no |
| <a id="user.find_me"></a>`user.find_me` | `find_me` | no |
| <a id="user.get_carpet_mode"></a>`user.get_carpet_mode` | `get_carpet_mode` | no |
| <a id="user.get_clean_record"></a>`user.get_clean_record` | `get_clean_record` | no |
| <a id="user.get_clean_record_map"></a>`user.get_clean_record_map` | `get_clean_record_map` | no |
| <a id="user.get_clean_record_map_v2"></a>`user.get_clean_record_map_v2` | `get_clean_record_map_v2` | no |
| <a id="user.get_clean_summary"></a>`user.get_clean_summary` | `get_clean_summary` | no |
| <a id="user.get_consumable"></a>`user.get_consumable` | `get_consumable` | no |
| <a id="user.get_current_sound"></a>`user.get_current_sound` | `get_current_sound` | no |
| <a id="user.get_custom_mode"></a>`user.get_custom_mode` | `get_custom_mode` | no |
| <a id="user.get_dnd_timer"></a>`user.get_dnd_timer` | `get_dnd_timer` | no |
| <a id="user.get_log_upload_status"></a>`user.get_log_upload_status` | `get_log_upload_status` | no |
| <a id="user.get_map_v1"></a>`user.get_map_v1` | `get_map_v1` | no |
| <a id="user.get_map_v2"></a>`user.get_map_v2` | `get_map_v2` | no |
| <a id="user.get_prop"></a>`user.get_prop` | `get_prop` | no |
| <a id="user.get_serial_number"></a>`user.get_serial_number` | `get_serial_number` | no |
| <a id="user.get_sound_progress"></a>`user.get_sound_progress` | `get_sound_progress` | no |
| <a id="user.get_sound_volume"></a>`user.get_sound_volume` | `get_sound_volume` | no |
| <a id="user.get_timer"></a>`user.get_timer` | `get_timer` | no |
| <a id="user.get_timezone"></a>`user.get_timezone` | `get_timezone` | no |
| <a id="user.reset_consumable"></a>`user.reset_consumable` | `reset_consumable` | no |
| <a id="user.set_carpet_mode"></a>`user.set_carpet_mode` | `set_carpet_mode` | no |
| <a id="user.set_custom_mode"></a>`user.set_custom_mode` | `set_custom_mode` | no |
| <a id="user.set_dnd_timer"></a>`user.set_dnd_timer` | `set_dnd_timer` | no |
| <a id="user.set_timer"></a>`user.set_timer` | `set_timer` | no |
| <a id="user.set_timezone"></a>`user.set_timezone` | `set_timezone` | no |
| <a id="user.start_clean"></a>`user.start_clean` | `start_clean` | no |
| <a id="user.stop_goto_target"></a>`user.stop_goto_target` | `stop_goto_target` | no |
| <a id="user.stop_zoned_clean"></a>`user.stop_zoned_clean` | `stop_zoned_clean` | no |
| <a id="user.test_sound_volume"></a>`user.test_sound_volume` | `test_sound_volume` | no |
| <a id="user.upd_timer"></a>`user.upd_timer` | `upd_timer` | no |

## See also

- [Transports and dispatch](../concepts/transports.md)
