# Status message

## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `get_status` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example

`{'method': 'get_status', 'id': 2}`

## Response



|  Key  | Example | Description |
| ------------ |------ |------------------------------ |
| `battery` |  _100_ | Battery level |
| `clean_area`|  _22902500_ |  total area (in cm2) |
| `clean_time` | _1468_ |  Total cleaning time in sec |
|  `dnd_enabled` | _0_ | Is Do Not Disturb enabled (0=disabled) |
| `error_code` | _0_ | Error code (0=no error. see list below) |
| `fan_power`| _60_ | Fan power |
| `in_cleaning`|  _0_ | Is device cleaning |
| `map_present`  | _0_ | Is map present |
| `msg_seq` | _37_ | Message sequence increments with each request |
| `msg_ver` | _4_ | Message version (seems always 4) |
| `state` | _8_ | Status code (see list below) |


### Example Response
```
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

### Status Codes
| Code | Description |
| --- | ------------ |
|  0 | Unknown |
| 1 | Initiating |
| 2 | Sleeping |
| 3 | Waiting |
| 4 | ? |
| 5 | Cleaning |
| 6 | Back to home |
| 7 | ? |
| 8 | Charging |
| 9 | Charging Error |
| 10 | Pause | 
| 11| Spot Cleaning |
| 12 | In Error |
| 13 | Shutting down |
| 14 | Updating |
| 15 | Docking |
| 100 | Full |
