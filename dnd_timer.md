# Get DND timing

Note. This describes the information you see in the DND configuration page in the MiHome App.
The actual DND status comes from the status message

## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `get_dnd_timer` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
`{'method': 'get_dnd_timer', 'id': 2}`

## Result

## Response



|  Key  | Example | Description |
| ------------ |------ |------------------------------ |
| `enabled` |  _1_ | Is DND functionality Enabled (1=True) |
| `end_hour` |  _8_ |  End Time DND (hour part) |
| `end_minute` | _0_ |  End Time DND (minute part) |
|  `start_hour` | _22_ | Start Time DND (hour part) |
| `start_minute` | _0_ | Start Time DND (minute part |

### Example Response

```
{
    "id": 2,
    "result": [
        {
            "enabled": 1,
            "end_hour": 8,
            "end_minute": 0,
            "start_hour": 22,
            "start_minute": 0
        }
    ]
}
```
