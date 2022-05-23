# Status Message

Retrieves the status informations of the device.

## Get Status Message

### Command

| Key    | Value          | Comment                                                                             |
| ------ | -------------- | ----------------------------------------------------------------------------------- |
| method | `"get_status"` |                                                                                     |
| id     | `id`           | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_status",
    "id": 96
}
```

### Response

| Key                         | Example  | Description                                                                                                                                         | Only available for |
| --------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| `battery`                   | _100_    | Battery level (in %)                                                                                                                                |                    |
| `clean_area`                | _140000_ | Total area (in mm²)                                                                                                                                 |                    |
| `clean_time`                | _15_     | Total cleaning time (in s)                                                                                                                          |                    |
| `dnd_enabled`               | _0_      | Is 'Do Not Disturb' enabled (0=disabled, 1=enabled)                                                                                                 |                    |
| `error_code`                | _0_      | Error code (see [list](#error-codes) below)                                                                                                         |                    |
| `fan_power`                 | _102_    | Fan power, corresponds to the values in [Custom Mode](custom_mode.md) (see [list](custom_mode.md#regular-modes))                                    |                    |
| `in_cleaning`               | _0_      | Is device cleaning                                                                                                                                  |                    |
| `in_fresh_state`            | _1_      | ?                                                                                                                                                   | s5, s6, s5e        |
| `in_returning`              | _0_      | Is returning to dock (0=no, 1=yes)                                                                                                                  | s5, s6, s5e        |
| `is_locating`               | _0_      | ?                                                                                                                                                   | s5e                |
| `lab_status`                | _1_      | ?                                                                                                                                                   | s5, s6, s5e        |
| `lock_status`               | _0_      | ?                                                                                                                                                   | s5, s6, s5e        |
| `map_present`               | _1_      | Is map present                                                                                                                                      |                    |
| `map_status`                | _3_      | ?                                                                                                                                                   | s5, s6, s5e        |
| `mop_forbidden_enable`      | _0_      | ?                                                                                                                                                   | s5e                |
| `msg_seq`                   | _52_     | Message sequence increments with each request                                                                                                       |                    |
| `msg_ver`                   | _2_      | Message version (seems always 4 and 2 for s6) see below for other examples                                                                                                        |                    |
| `state`                     | _8_      | Status code (see [list](#status-codes) below)                                                                                                       |                    |
| `water_box_carriage_status` | _0_      | Is carriage mounted (0=no, 1=yes)                                                                                                                   | s5e                |
| `water_box_mode`            | _204_    | Water quantity control, corresponds to the values in [Water Box Custom Mode](water_box_custom_mode.md) (see [list](water_box_custom_mode.md#modes)) | s5e                |
| `water_box_status`          | _1_      | Is water tank mounted (0=no, 1=yes)                                                                                                                 | s5, s6, s5e        |

#### Example

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

## Codes

### Status Codes

| Code | Description    |
| ---- | -------------- |
| 0    | Unknown        |
| 1    | Initiating     |
| 2    | Sleeping       |
| 3    | Idle           |
| 4    | Remote Control |
| 5    | Cleaning       |
| 6    | Returning Dock |
| 7    | Manual Mode    |
| 8    | Charging       |
| 9    | Charging Error |
| 10   | Paused         |
| 11   | Spot Cleaning  |
| 12   | In Error       |
| 13   | Shutting Down  |
| 14   | Updating       |
| 15   | Docking        |
| 16   | Go To          |
| 17   | Zone Clean     |
| 18   | Room Clean     |
| 100  | Fully Charged  |

### Error Codes

| Code | Description                   |
| ---- | ----------------------------- |
| 0    | No error                      |
| 1    | Laser sensor fault            |
| 2    | Collision sensor fault        |
| 3    | Wheel floating                |
| 4    | Cliff sensor fault            |
| 5    | Main brush blocked            |
| 6    | Side brush blocked            |
| 7    | Wheel blocked                 |
| 8    | Device stuck                  |
| 9    | Dust bin missing              |
| 10   | Filter blocked                |
| 11   | Magnetic field detected       |
| 12   | Low battery                   |
| 13   | Charging problem              |
| 14   | Battery failure               |
| 15   | Wall sensor fault             |
| 16   | Uneven surface                |
| 17   | Side brush failure            |
| 18   | Suction fan failure           |
| 19   | Unpowered charging station    |
| 20   | Unknown Error                 |
| 21   | Laser pressure sensor problem |
| 22   | Charge sensor problem         |
| 23   | Dock problem                  |
| 24   | No-go zone or invisible wall detected |                  |
| 254  | Bin full                      |
| 255  | Internal error                |
| -1   | Unknown Error                 |
