# Status message

## Command

| Key    | Value        | Comment                                                                    |
| ------ | ------------ | -------------------------------------------------------------------------- |
| method | `get_status` |                                                                            |
| id     | [Integer]    | is returned in the response used to link the send message to the response. |

### Example

`{'method': 'get_status', 'id': 2}`

## Response

| Key                | Example    | Description                                   |
| ------------------ | ---------- | --------------------------------------------- |
| `battery`          | _100_      | Battery level                                 |
| `clean_area`       | _22902500_ | Total area (in cm2)                           |
| `clean_time`       | _1468_     | Total cleaning time in sec                    |
| `dnd_enabled`      | _0_        | Is Do Not Disturb enabled (0=disabled)        |
| `error_code`       | _0_        | Error code (0=no error. see list below)       |
| `fan_power`        | _60_       | Fan power                                     |
| `in_cleaning`      | _0_        | Is device cleaning                            |
| `in_fresh_state`   | _0_        | ?                                             |
| `in_returning`     | _1_        | Is returning to dock (0=no, 1=yes)            |
| `lab_status`       | _1_        | ?                                             |
| `lock_status`      | _0_        | ?                                             |
| `map_present`      | _0_        | Is map present                                |
| `map_status`       | _3_        | ?                                             |
| `msg_seq`          | _37_       | Message sequence increments with each request |
| `msg_ver`          | _4_        | Message version (seems always 4 and 2 for s6) |
| `state`            | _8_        | Status code (see list below)                  |
| `water_box_status` | _1_        | Is water tank mounted (0=no, 1=yes)           |

### Example Response

```json
{
    "id": 2,
    "result": [
        {
            "battery": 100,
            "clean_area": 22902500,
            "clean_time": 1468,
            "dnd_enabled": 0,
            "error_code": 0,
            "fan_power": 60,
            "in_cleaning": 0,
            "map_present": 0,
            "msg_seq": 37,
            "msg_ver": 4,
            "state": 8
        }
    ]
}
```

### Example Response for s6

```json
{
    "result": [
        {
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
            "lock_status": 0
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
