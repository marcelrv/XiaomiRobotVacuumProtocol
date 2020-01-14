# Do Not Disturb

This describes the information you see in the DND configuration page in the MiHome App.
The actual DND status comes from the status message.

## Get DND Timer

### Command

| Key    | Value             | Comment                                                                             |
| ------ | ----------------- | ----------------------------------------------------------------------------------- |
| method | `"get_dnd_timer"` |                                                                                     |
| id     | `id`              | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_dnd_timer",
    "id": 67
}
```

### Response

| Key            | Example | Description                                          |
| -------------- | ------- | ---------------------------------------------------- |
| `enabled`      | _1_     | Is DND functionality enabled (0=disabled, 1=enabled) |
| `end_hour`     | _8_     | End Time DND (hour part)                             |
| `end_minute`   | _0_     | End Time DND (minute part)                           |
| `start_hour`   | _22_    | Start Time DND (hour part)                           |
| `start_minute` | _0_     | Start Time DND (minute part)                         |

#### Example

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

## Set DND Timer

### Command

 | Key    | Value                                                | Comment                                                                             |
 | ------ | ---------------------------------------------------- | ----------------------------------------------------------------------------------- |
 | method | `"set_dnd_timer"`                                    |                                                                                     |
 | params | `[start_hour, start_minutes, end_hour, end_minutes]` | 24 hour notation, not using am/pm                                                   |
 | id     | `id`                                                 | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "set_dnd_timer",
    "params": [22, 0, 8, 0],
    "id": 2346
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 2346
}
```
