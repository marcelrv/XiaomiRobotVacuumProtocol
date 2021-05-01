# Log Upload

Retreives the log upload status.

## Get Log Upload

### Command

| Key    | Value                     | Comment                                                                             |
| ------ | ------------------------- | ----------------------------------------------------------------------------------- |
| method | `"get_log_upload_status"` |                                                                                     |
| id     | `id`                      | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_log_upload_status",
    "id": 8357
}
```

### Response

| Key                 | Example | Description       |
| ------------------- | ------- | ----------------- |
| `log_upload_status` | _3_     | Log upload status |

#### Example

```json
{
    "result": [{
            "log_upload_status": 3
        }
    ],
    "id": 8357
}
```
