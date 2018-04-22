# Goto Target

This command sends the robot to target coordinates. (works for robot v2 and v1
with firmware versions `3.3.9_003194` or newer)

## Command

| Key     | Value                    | Comment                                                                             |
| ------- | -----------              | -------                                                                             |
| method  | `app_goto_target`        |                                                                                     |
| params  | `[x Integer, y Integer]` | Coordinates to goto.                                                                |
| id      | `[Integer]`              | Random integer which is returned in the response used to link request and response. |

### Example

```json
{
  "id": 25736111,
  "method": "app_goto_target",
  "params": [24200,20200]
}
```
