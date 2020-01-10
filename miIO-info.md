# Mi IO Info

This command gets device and network details.
It seems to be generic/applicable to all Xiaomi devices

# Get Info
## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `miIO.info` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
`'method': 'miIO.info', 'id': 7840`

## response
|  Key  | Example | Description |
| ------------ |------ |------------------------------ |
| `partner_id` |  _40_ | Unknown where this is used for |
| `id` |  _7840_ | Returned ID from request |
| `code` |  _0_ | Unknown where this is used for |
| `message` |  _ok_ |   |
| `result` |    | Response to the command |
| `hw_ver` |  _Linux_ |   |
| `fw_ver` |  _3.3.6_003061_ | Full firmware version  |
| `ap` |    |  Wifi details |
| `ssid` |  _mylocalwifi_ |  wifi ssid |
| `bssid` |  _F2:9F:C2:AA:AA:AA_ |  wifi basestation |
| `rssi` |  _-63_ |  wifi signal strenght |
| `netif` |  __ | Network details  |
| `localIp` |  _192.168.9.199_ | Ip for the MiIO device  |
| `mask` |  _255.255.255.0_ | net mask  |
| `gw` |  _192.168.9.1_ | gateway  |
| `model` |  _rockrobo.vacuum.v1_ |  Type of MiIO device |
| `mac` |  _28:6C:07:AA:AA:AA_ | Device MAC address  |
| `token` |  _4474746a612345678905612345678900_ |  Token for this device |
| `life` |  _62848_ | life in minutes? |


## Response Example

```
{"partner_id":"",
  "id":7840,
   "code":0,
   "message":"ok",
   "result":{ 
        "hw_ver":"Linux",
        "fw_ver":"3.3.6_003061",
        "ap":{
             "ssid":"mylocalwifi",
             "bssid":"F2:9F:C2:AA:AA:AA",
             "rssi":-63
             },
        "netif":{
                  "localIp":"192.168.9.199",
                  "mask":"255.255.255.0",
                  "gw":"192.168.9.1"
                  },
        "model":"rockrobo.vacuum.v1",
        "mac":"28:6C:07:AA:AA:AA",
        "token":"4474746a612345678905612345678900",
        "life":62848}}
}
```
