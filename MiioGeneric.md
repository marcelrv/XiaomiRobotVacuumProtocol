# Mi Io Generic commands

These commands appear to be shared amngs all(?) Xiaomi Mi Io devices.

# Get Wifi status
## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `miIO.wifi_assoc_state` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
`'method': 'miIO.wifi_assoc_state', 'id': 7840`

## response
|  Key  | Example | Description |
| ------------ |------ |------------------------------ |
| `id` |  _37_ | Returned ID from request |
| `code` |  _0_ | Unknown where this is used for |
| `message` |  _ok_ |   |
| `result` |    | Response to the command |
| `state` |  _ONLINE_ |   |
| `auth_fail_count` |  _0_ | Authentication failed  |
| `conn_success_count` |   _1_  |  connection success count |
| `conn_fail_count` |   _0_ |  connection fail count |
| `dhcp_fail_count` |   _0_ |  dhcp request failed count |

## Response Example

```
{ "id":37,
   "code":0,
   "message":"ok",
   "result": {"state":"ONLINE",
              "auth_fail_count":0,
              "conn_success_count":1,
              "conn_fail_count":0,
              "dhcp_fail_count":0}
 }
```


## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `miIO.ota` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
miIO.ota '{"mode":"normal", "install":"1", "app_url":"http://IP/v11_#version#.pkg", "file_md5":"#md5#","proc":"dnld install"}'
