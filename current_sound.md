# Current Sound

Retreives the current active voice and which is being installed.

## Get Current Sound

### Command

| Key    | Value                 | Comment                                                                             |
| ------ | --------------------- | ----------------------------------------------------------------------------------- |
| method | `"get_current_sound"` |                                                                                     |
| id     | `id`                  | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_current_sound",
    "id": 1
}
```

### Response

| Key               | Example | Description                                   |
| ----------------- | ------- | --------------------------------------------- |
| `sid_in_use`      | _3_     | Active voice (English = 3)                    |
| `sid_in_progress` | _0_     | Voice in progress of being installed (0=none) |

#### Example

```json
{
    "result": [{
            "sid_in_use": 3,
            "sid_in_progress": 0
        }
    ],
    "id": 1
}
```
