#Status message

## Command
`{'method': 'get_status', 'id': 2}`

## Response

clean_time in seconds
clean_area in cm2

states
8 - ?

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
