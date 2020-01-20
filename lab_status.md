# Lab Status

Enable persistent maps and software barriers.

This is required to use `start_edit_map`, `end_edit_map`, `save_map`, etc. commands.

## Set Lab Status

### Command

| Key    | Value              | Comment                                                                             |
| ------ | ------------------ | ----------------------------------------------------------------------------------- |
| method | `"set_lab_status"` |                                                                                     |
| params | `[state]`          | State to be set (0=disabled, 1=enabled).                                            |
| id     | `id`               | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "set_lab_status",
    "params": [1],
    "id": 3563
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 3563
}
```
