# Status Message

## Command

| Key    | Value        | Comment                                                                    |
| ------ | ------------ | -------------------------------------------------------------------------- |
| method | `get_status` |                                                                            |
| id     | [Integer]    | is returned in the response used to link the send message to the response. |

### Example Command

`{'method': 'get_status', 'id': 2}`

## Response

| Key                         | Example  | Description                                         |
| --------------------------- | -------- | --------------------------------------------------- |
| `battery`                   | _100_    | Battery level (in %)                                |
| `clean_area`                | _140000_ | Total area (in cm²)                                 |
| `clean_time`                | _15_     | Total cleaning time (in s)                          |
| `dnd_enabled`               | _0_      | Is 'Do Not Disturb' enabled (0=disabled, 1=enabled) |
| `error_code`                | _0_      | Error code (see [list](#error-codes) below)         |
| `fan_power`                 | _102_    | Fan power                                           |
| `in_cleaning`               | _0_      | Is device cleaning                                  |
| `in_fresh_state`            | _1_      | ?                                                   |
| `in_returning`              | _0_      | Is returning to dock (0=no, 1=yes)                  |
| `is_locating`               | _0_      | ?                                                   |
| `lab_status`                | _1_      | ?                                                   |
| `lock_status`               | _0_      | ?                                                   |
| `map_present`               | _1_      | Is map present                                      |
| `map_status`                | _3_      | ?                                                   |
| `mop_forbidden_enable`      | _0_      | ?                                                   |
| `msg_seq`                   | _52_     | Message sequence increments with each request       |
| `msg_ver`                   | _2_      | Message version (seems always 4 and 2 for s6)       |
| `state`                     | _8_      | Status code (see [list](#status-codes) below)       |
| `water_box_carriage_status` | _0_      | ?                                                   |
| `water_box_mode`            | _204_    | ?                                                   |
| `water_box_status`          | _1_      | Is water tank mounted (0=no, 1=yes)                 |

### Example Response

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
```

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
| 254  | Bin full                      |
| 255  | Internal error                |
| -1   | Unknown Error                 |
