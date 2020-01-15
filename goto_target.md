# Goto Target

Sends the robot to target coordinates.

## Start Goto Target

### Command

| Key    | Value               | Comment                                                                             |
| ------ | ------------------- | ----------------------------------------------------------------------------------- |
| method | `"app_goto_target"` |                                                                                     |
| params | `[x, y]`            | Coordinate intergers where to goto.                                                 |
| id     | `id`                | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "app_goto_target",
    "params": [24200, 20200],
    "id": 12150
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 12150
}
```
