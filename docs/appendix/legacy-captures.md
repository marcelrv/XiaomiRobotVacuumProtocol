# Legacy captures

[Home](../../README.md) / [Appendix](index.md) / Legacy captures

The request and reply examples of the pre-existing pages of this repository (commit `be636c7`), kept as **legacy captures (unverified)**: no bundle contains robot replies, so these are the only real-device samples. Device token, MAC addresses, IP addresses, Wi-Fi names, room ids and serial numbers were replaced by placeholders. The current reference for every call is linked in the heading; where a legacy example differs from what the app code shows, the command page says so.

## Basic Operations

Now documented in [docs/commands/cleaning-control.md](../../docs/commands/cleaning-control.md) (old page: [`basic.md`](../../basic.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "app_start",
    "id": 6340
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 6340
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "app_stop",
    "id": 12363
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 12363
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "app_spot",
    "id": 63362
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 63362
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "app_pause",
    "id": 633
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 633
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "app_charge",
    "id": 45334
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 45334
}
```

## Clean Summary

Now documented in [docs/commands/clean-history.md](../../docs/commands/clean-history.md) (old page: [`clean_summary+record.md`](../../clean_summary+record.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_clean_summary",
    "id": 2
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [16414, 252165000, 9, [1497139200, 1496966400, 1496620800, 1496534400, 1496448000, 1496361600]],
    "id": 2
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "get_clean_summary",
    "id": 2
}
```

**Example — legacy capture (unverified)**

```json
{ "id":5018,
   "result":{"clean_time":38629,"clean_area":650425000,"clean_count":68,"dust_collection_count":0,"records": 
              [1626292843,1626260657,1626255012,1626206412,1626174164,1626168621,1626036597,1626036415,1626035701,1626035555,1626033643,1626028227,1626021936,1626021732,1626021575,1626020891,1626020332,1626019286,1626019207,1626019147]
            },
   "exe_time":100
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "get_clean_record",
    "params": [1497139200],
    "id": 263
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [[1497163727, 1497165195, 1468, 22902500, 0, 1]],
    "id": 263
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [[1497163727, 1497165195, 1468, 22902500, 0, 1, 2, 2, 60]],
    "id": 263
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "get_clean_record_map",
    "params": [1497139200],
    "id": 263
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["roboroommap%22<id>%2F1"],
    "id": 2475
}
```

## Consumable

Now documented in [docs/commands/consumables.md](../../docs/commands/consumables.md) (old page: [`consumable.md`](../../consumable.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_consumable",
    "id": 3457
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [{
            "main_brush_work_time": 32030,
            "side_brush_work_time": 32030,
            "filter_work_time": 32030,
            "filter_element_work_time": 7037,
            "sensor_dirty_time": 34922
        }
    ],
    "id": 3457
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "reset_consumable",
    "params": ["filter_work_time"],
    "id": 8756
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 8756
}
```

## Current Sound

Now documented in [docs/commands/sound.md#get_current_sound](../../docs/commands/sound.md#get_current_sound) (old page: [`current_sound.md`](../../current_sound.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_current_sound",
    "id": 184
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [{
            "sid_in_use": 3,
            "sid_in_progress": 0
        }
    ],
    "id": 184
}
```

## Custom Mode

Now documented in [docs/commands/cleaning-modes.md](../../docs/commands/cleaning-modes.md) (old page: [`custom_mode.md`](../../custom_mode.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_custom_mode",
    "id": 17735
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [40],
    "id": 17735
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "set_custom_mode",
    "params": [40],
    "id": 17694
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 17694
}
```

## Do Not Disturb

Now documented in [docs/commands/timers.md](../../docs/commands/timers.md) (old page: [`dnd_timer.md`](../../dnd_timer.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_dnd_timer",
    "id": 67
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [{
            "enabled": 1,
            "end_hour": 8,
            "end_minute": 0,
            "start_hour": 22,
            "start_minute": 0
        }
    ],
    "id": 67
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "set_dnd_timer",
    "params": [22, 0, 8, 0],
    "id": 2346
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 2346
}
```

## Find Robot

Now documented in [docs/commands/cleaning-control.md#find_me](../../docs/commands/cleaning-control.md#find_me) (old page: [`find_me.md`](../../find_me.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "find_me",
    "id": 12394
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 12394
}
```

## Firmware Features

Now documented in [docs/concepts/feature-flags.md](../../docs/concepts/feature-flags.md) (old page: [`fw_features.md`](../../fw_features.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_fw_features",
    "id": 7177
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [111, 112, 113, 114, 115, 116, 117, 118, 119, 122, 125],
    "id": 7177
}
```

## Goto Target

Now documented in [docs/commands/cleaning-control.md#app_goto_target](../../docs/commands/cleaning-control.md#app_goto_target) (old page: [`goto_target.md`](../../goto_target.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "app_goto_target",
    "params": [24200, 20200],
    "id": 12150
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 12150
}
```

## Initial Status

Now documented in [docs/commands/status.md#app_get_init_status](../../docs/commands/status.md#app_get_init_status) (old page: [`init_status.md`](../../init_status.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "app_get_init_status",
    "id": 5879
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [{
            "local_info": {
                "name": "custom_A.03.0070_CE",
                "bom": "A.03.0070",
                "location": "de",
                "language": "en",
                "wifiplan": "",
                "timezone": "Europe/Berlin",
                "logserver": "awsde0.fds.api.xiaomi.com",
                "featureset": 1
            },
            "feature_info": [111, 112, 113, 114, 115, 116, 117, 118, 119, 122, 125],
            "status_info": {
                "state": 8,
                "battery": 100,
                "clean_time": 2496,
                "clean_area": 34912500,
                "error_code": 0,
                "in_cleaning": 0,
                "in_returning": 0,
                "in_fresh_state": 1,
                "lab_status": 1,
                "water_box_status": 1,
                "map_status": 3,
                "is_locating": 0,
                "lock_status": 0,
                "water_box_mode": 204,
                "water_box_carriage_status": 1,
                "mop_forbidden_enable": 1
            }
        }
    ],
    "id": 6652
}
```

## Voice Pack Installation

Now documented in [docs/commands/sound.md](../../docs/commands/sound.md) (old page: [`install_sound.md`](../../install_sound.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "dnld_install_sound",
    "params": {
        "md5": "#MD5#",
        "sid": 1005,
        "url": "http://PATH TO SERVER/FILE.pkg",
        "sver": 2
    },
    "id": 1794
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 1794
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "get_sound_progress",
    "id": 5172
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [{
            "sid_in_progress": 0,
            "progress": 0,
            "state": 0,
            "error": 0
        }
    ],
    "id": 5172
}
```

## Lab Status

Now documented in [docs/commands/maps.md#set_lab_status](../../docs/commands/maps.md#set_lab_status) (old page: [`lab_status.md`](../../lab_status.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "set_lab_status",
    "params": [1],
    "id": 3563
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 3563
}
```

## Locale Information

Now documented in [docs/commands/status.md#app_get_locale](../../docs/commands/status.md#app_get_locale) (old page: [`locale.md`](../../locale.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "app_get_locale",
    "id": 5879
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [{
            "name": "custom_A.03.0070_CE",
            "bom": "A.03.0070",
            "location": "de",
            "language": "en",
            "wifiplan": "",
            "timezone": "Europe/Berlin",
            "logserver": "awsde0.fds.api.xiaomi.com",
            "featureset": 1
        }
    ],
    "id": 5879
}
```

## Log Upload

Now documented in [docs/commands/system.md](../../docs/commands/system.md) (old page: [`log_upload.md`](../../log_upload.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_log_upload_status",
    "id": 8357
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [{
            "log_upload_status": 3
        }
    ],
    "id": 8357
}
```

## Map

Now documented in [docs/commands/maps.md#save_map](../../docs/commands/maps.md#save_map) (old page: [`map.md`](../../map.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "save_map",
    "params": [
        [0, 27000, 32000, 30750, 32000, 30750, 30250, 27000, 30250], // no-go zone
        [1, 33800, 27850, 34900, 28700] // barrier
    ],
    "id": 263
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 263
}
```

## Map V1

Now documented in [docs/commands/maps.md#get_map_v1](../../docs/commands/maps.md#get_map_v1) (old page: [`map_v1.md`](../../map_v1.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_map_v1",
    "id": 2475
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["roboroommap%22<id>%2F1"],
    "id": 2475
}
```

## Mi IO Generic - Info

Now documented in [docs/concepts/miio-protocol.md#generic-methods](../../docs/concepts/miio-protocol.md#generic-methods) (old page: [`miIO-info.md`](../../miIO-info.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "miIO.info",
    "id": 7840
}
```

**Example — legacy capture (unverified)**

```json
{
    "partner_id": "",
    "id": 7840,
    "code": 0,
    "message": "ok",
    "result": {
        "hw_ver": "Linux",
        "fw_ver": "3.3.6_003061",
        "ap": {
            "ssid": "<SSID>",
            "bssid": "<MAC address>",
            "rssi": -63
        },
        "netif": {
            "localIp": "<IP address>",
            "mask": "<IP address>",
            "gw": "<IP address>"
        },
        "model": "rockrobo.vacuum.v1",
        "mac": "<MAC address>",
        "token": "<32 hex digits>",
        "life": 62848
    }
}
```

## Mi IO Generic - Update Firmware Over Air

Now documented in [docs/concepts/miio-protocol.md#generic-methods](../../docs/concepts/miio-protocol.md#generic-methods) (old page: [`miIO-ota.md`](../../miIO-ota.md)).

**Example — legacy capture (unverified)**

```json
{
    "mode": "normal",
    "install": "1",
    "app_url": "http://IP/v11_#version#.pkg",
    "file_md5": "#md5#",
    "proc": "dnld install"
}
```

## Mi IO Generic - Wifi Status

Now documented in [docs/concepts/miio-protocol.md#generic-methods](../../docs/concepts/miio-protocol.md#generic-methods) (old page: [`miIO-wifi_assoc_state.md`](../../miIO-wifi_assoc_state.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "miIO.wifi_assoc_state",
    "id": 37
}
```

**Example — legacy capture (unverified)**

```json
{
    "id": 37,
    "code": 0,
    "message": "ok",
    "result": {
        "state": "ONLINE",
        "auth_fail_count": 0,
        "conn_success_count": 1,
        "conn_fail_count": 0,
        "dhcp_fail_count": 0
    }
}
```

## Multimap

Now documented in [docs/commands/maps.md#get_multi_maps_list](../../docs/commands/maps.md#get_multi_maps_list) (old page: [`multimap.md`](../../multimap.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_multi_maps_list",
    "id": 7840
}
```

**Example — legacy capture (unverified)**

```json
{
  "id": 36,
  "result": [
    {
      "max_multi_map": 4,
      "max_bak_map": 0,
      "multi_map_count": 3,
      "map_info": [
        {
          "mapFlag": 0,
          "add_time": 1619719086,
          "length": 11,
          "name": "Erdgeschoss",
          "bak_maps": []
        },
        {
          "mapFlag": 1,
          "add_time": 1619709702,
          "length": 5,
          "name": "TEST3",
          "bak_maps": []
        },
        {
          "mapFlag": 2,
          "add_time": 1619721286,
          "length": 0,
          "name": "",
          "bak_maps": []
        }
      ]
    }
  ],
  "exe_time": 100
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "load_multi_map",
    "params": [
        [1], // Mapnumber
    ],
    "id": 7840
}
```

## Network - Info

Now documented in [docs/commands/system.md#get_network_info](../../docs/commands/system.md#get_network_info) (old page: [`network_info.md`](../../network_info.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_network_info",
    "id": 7840
}
```

**Example — legacy capture (unverified)**

```json
{
    "id": 7840,
    "result": {
        "ssid": "<SSID>",
        "ip": "<IP address>",
        "mac": "<MAC address>",
        "bssid": "<MAC address>",
        "rssi": -52
    }
}
```

## Remote Control

Now documented in [docs/commands/remote-control.md](../../docs/commands/remote-control.md) (old page: [`rc.md`](../../rc.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "app_rc_start",
    "id": 1756
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 1756
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "app_rc_end",
    "id": 64346
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 64346
}
```

**Example — legacy capture (unverified)**

```json
{
    "id": 353,
    "method": "app_rc_move",
    "params": [[{
                "omega": 0.5712,
                "velocity": 0,
                "seqnum": 19,
                "duration": 1500
            }
        ]]
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 353
}
```

## Room Mapping

Now documented in [docs/commands/rooms-and-areas.md#get_room_mapping](../../docs/commands/rooms-and-areas.md#get_room_mapping) (old page: [`room_mapping.md`](../../room_mapping.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_room_mapping",
    "id": 14837
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [[16, "<room id>"], [17, "<room id>"], [18, "<room id>"], [19, "<room id>"]],
    "id": 14837
}
```

## Segment Cleaning

Now documented in [docs/commands/cleaning-control.md#app_segment_clean](../../docs/commands/cleaning-control.md#app_segment_clean) (old page: [`segment_clean.md`](../../segment_clean.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "app_segment_clean",
    "params": [16, 17, 18],
    "id": 6764
}
or
{
    "method": "app_segment_clean",
    "params": [{"segments": [16, 17, 18],"repeat": 2}],
    "id": 6764
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 3453
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "stop_segment_clean",
    "id": 3453
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 3453
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "resume_segment_clean",
    "id": 342
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 342
}
```

## Serial Number

Now documented in [docs/commands/status.md#get_serial_number](../../docs/commands/status.md#get_serial_number) (old page: [`serial_number.md`](../../serial_number.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_serial_number",
    "id": 1
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [{
            "serial_number": "<serial number>"
        }
    ],
    "id": 1
}
```

## Sound Volume

Now documented in [docs/commands/sound.md](../../docs/commands/sound.md) (old page: [`sound_volume.md`](../../sound_volume.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_sound_volume",
    "id": 657
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [100],
    "id": 657
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "change_sound_volume",
    "params": [55],
    "id": 624
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 624
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "test_sound_volume",
    "id": 546
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 546
}
```

## Status Message

Now documented in [docs/commands/status.md#get_status](../../docs/commands/status.md#get_status) (old page: [`status.md`](../../status.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_status",
    "id": 96
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [{
            "msg_ver": 2,
            "msg_seq": 52,
            "state": 8,
            "battery": 100,
            "clean_time": 15,
            "clean_area": 140000,
            "error_code": 0,
            "map_present": 1,
            "in_cleaning": 0,
            "in_returning": 0,
            "in_fresh_state": 1,
            "lab_status": 1,
            "water_box_status": 1,
            "fan_power": 102,
            "dnd_enabled": 0,
            "map_status": 3,
            "is_locating": 0,
            "lock_status": 0,
            "water_box_mode": 204,
            "water_box_carriage_status": 0,
            "mop_forbidden_enable": 0
        }
    ],
    "id": 96
}

Other message examples

msg_ver 1:
{"result":[{"msg_ver":1,"msg_seq":3032,"state":8,"battery":100,"clean_time":30,"clean_area":0,"error_code":0,"map_present":1,"in_cleaning":0,"in_returning":0,"in_fresh_state":1,"lab_status":1,"fan_power":102,"dnd_enabled":0,"map_status":3}],"id":3111}

msg_ver 2:
{"result":[{"msg_ver":2,"msg_seq":2569,"state":8,"battery":72,"clean_time":72,"clean_area":1977500,"error_code":0,"map_present":1,"in_cleaning":0,"in_returning":0,"in_fresh_state":1,"lab_status":1,"fan_power":60,"dnd_enabled":0}],"id":8745}

msg_ver 3:
{"clean_time": 9, "msg_ver": 3, "fan_power": 104, "msg_seq": 387, "lock_status": 0, "dnd_enabled": 0, "clean_area": 0, "map_present": 1, "error_code": 0, "map_status": 3, "battery": 100, "water_box_status": 0, "state": 8, "in_returning": 0, "lab_status": 1, "in_cleaning": 0, "in_fresh_state": 1}

msg_ver 4:
{ "result": [ { "msg_ver": 4, "msg_seq": 238, "state": 6, "battery": 100, "clean_time": 21, "clean_area": 240000, "error_code": 0, "map_present": 1, "in_cleaning": 0, "fan_power": 60, "dnd_enabled": 1 } ], "id": 10026 }

msg_ver 5:
{'result': [{'error_code': 0, 'battery': 100, 'dnd_enabled': 1, 'map_present': 0, 'state': 8, 'clean_time': 0, 'msg_seq': 594, 'fan_power': 77, 'msg_ver': 5, 'in_cleaning': 0, 'clean_area': 502500}], 'id': 9455}

msg_ver 6:
{"result":[{"msg_ver":6,"msg_seq":2004,"state":8,"battery":100,"clean_time":2839,"clean_area":48287500,"error_code":0,"map_present":0,"in_cleaning":0,"fan_power":77,"dnd_enabled":0}],"id":21}


msg_ver 7:
[{"msg_ver":8,"msg_seq":3,"state":2,"battery":93,"clean_mode":0,"fan_power":68,"error_code":0,"map_present":1,"in_cleaning":0,"dnd_enabled":0,"begin_time":0,"clean_time":8305,"clean_area":116122500,"clean_trigger":0,"back_trigger":0,"completed":0,"clean_strategy":0}],"id":993}
```

## Cleaning Timer

Now documented in [docs/commands/timers.md](../../docs/commands/timers.md) (old page: [`timer.md`](../../timer.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_timer",
    "id": 173
}
```

**Example — legacy capture (unverified)** — Response

```txt
   ┌───────────── minute (0 - 59)
   │ ┌───────────── hour (0 - 23)
   │ │ ┌───────────── day of month (1 - 31)
   │ │ │ ┌───────────── month (1 - 12)
   │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday,
   │ │ │ │ │                                       7 is also Sunday)
   │ │ │ │ │
   │ │ │ │ │
   * * * * *      command to execute + parameter
 ["1 5 * * 0,6", ["start_clean", ""]]]
```

**Example — legacy capture (unverified)**

```json
{
    "result": [
        ["<room id>", "on", ["38 10 * * 0,6", ["start_clean", ""]]],
        ["<room id>", "on", ["38 5 * * 1,2,3,4,5", ["start_clean", ""]]],
        ["<room id>", "on", ["38 9 28 6 *", ["start_clean", ""]]]
    ],
    "id": 173
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "set_timer",
    "params": [["<room id>", ["30 12 * * 1,2,3,4,5", ["start_clean", ""]]]],
    "id": 1734
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 1734
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "upd_timer",
    "params": ["<room id>", "off"],
    "id": 634
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 634
}
```

## Timezone

Now documented in [docs/commands/system.md#get_timezone](../../docs/commands/system.md#get_timezone) (old page: [`timezone.md`](../../timezone.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_timezone",
    "id": 30
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["Europe/Amsterdam"],
    "id": 30
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "set_timezone",
    "params": ["Europe/Amsterdam"],
    "id": 31
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 31
}
```

## Water Box Custom Mode

Now documented in [docs/commands/cleaning-modes.md#set_water_box_custom_mode](../../docs/commands/cleaning-modes.md#set_water_box_custom_mode) (old page: [`water_box_custom_mode.md`](../../water_box_custom_mode.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "get_water_box_custom_mode",
    "id": 17735
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": [201],
    "id": 17735
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": {"water_box_mode": 207, "distance_off": 60},
    "id": 17735
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "set_water_box_custom_mode",
    "params": [202],
    "id": 17694
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "set_water_box_custom_mode",
    "params": {"water_box_mode": 207, "distance_off": 60},
    "id": 17694
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 17694
}
```

## Zone Cleaning

Now documented in [docs/commands/cleaning-control.md#app_zoned_clean](../../docs/commands/cleaning-control.md#app_zoned_clean) (old page: [`zoned_clean.md`](../../zoned_clean.md)).

**Example — legacy capture (unverified)**

```json
{
    "method": "app_zoned_clean",
    "params": [
        [26234, 26042, 27284, 26642, 1], // zone A should be cleaned once
        [26232, 25304, 27282, 25804, 2], // zone B should be cleaned twice
        [26246, 24189, 27296, 25139, 3]  // zone C should be cleaned 3 times
    ],
    "id": 8338
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 8338
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "stop_zoned_clean",
    "id": 6341
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 6341
}
```

**Example — legacy capture (unverified)**

```json
{
    "method": "resume_zoned_clean",
    "id": 12363
}
```

**Example — legacy capture (unverified)**

```json
{
    "result": ["ok"],
    "id": 12363
}
```

## See also

- [Corrections](corrections.md)
- [Command index](../commands/index.md)
