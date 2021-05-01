# Network - Info

Gets network details.

## Get Info

### Command

| Key    | Value                | Comment                                                                             |
| ------ | -------------        | ----------------------------------------------------------------------------------- |
| method | `"get_network_info"` |                                                                                     |
| id     | `id`                 | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_network_info",
    "id": 7840
}
```
### Response

| Key          | Example                            | Description                    |
| ------------ | ---------------------------------- | ------------------------------ |
| `id`         | _7840_                             | Returned ID from request       |
| `result`     |                                    | Response to the command        |
| `ssid`       | _mylocalwifi_                      | wifi ssid                      |
| `bssid`      | _F2:9F:C2:AA:AA:AA_                | wifi basestation               |
| `rssi`       | _-63_                              | wifi signal strenght           |
| `localIp`    | _192.168.9.199_                    | Ip for the MiIO device         |
| `mac`        | _28:6C:07:AA:AA:AA_                | Device MAC address             |

#### Example

```json
{
    "id": 7840,
    "result": {
        "ssid": "iot",
        "ip": "192.168.178.99",
        "mac": "b0:4a:33:04:f6:5f",
        "bssid": "2a:b8:29:e4:cb:45",
        "rssi": -52
    }
}
```
