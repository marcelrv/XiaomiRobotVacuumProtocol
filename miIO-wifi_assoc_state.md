# Mi IO Generic - Wifi Status

Gets wifi details and statistics.

## Get Wifi status

### Command

| Key    | Value                     | Comment                                                                             |
| ------ | ------------------------- | ----------------------------------------------------------------------------------- |
| method | `"miIO.wifi_assoc_state"` |                                                                                     |
| id     | `id`                      | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "miIO.wifi_assoc_state",
    "id": 37
}
```

### Response

| Key                  | Example  | Description                    |
| -------------------- | -------- | ------------------------------ |
| `id`                 | _37_     | Returned ID from request       |
| `code`               | _0_      | Unknown where this is used for |
| `message`            | _ok_     |                                |
| `result`             |          | Response to the command        |
| `state`              | _ONLINE_ |                                |
| `auth_fail_count`    | _0_      | Authentication failed          |
| `conn_success_count` | _1_      | connection success count       |
| `conn_fail_count`    | _0_      | connection fail count          |
| `dhcp_fail_count`    | _0_      | dhcp request failed count      |

#### Example

```json
{
    "id": 37,
    "code": 0,
    "message": "ok",
    "result": {
        "state": "ONLINE",
        "auth_fail_count": 0,
        "conn_success_count": 1,
        "conn_fail_count": 0,
        "dhcp_fail_count": 0
    }
}
```
