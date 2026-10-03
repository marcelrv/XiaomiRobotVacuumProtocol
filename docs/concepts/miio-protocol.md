# Xiaomi Mi Home Binary Protocol

[Home](../../README.md) / Concepts / miIO protocol

> **Evidence level.** The packet layout, handshake and encryption below are third-party documentation (copied from the [Open Mi Home Project](https://github.com/OpenMiHome/mihome-binary-protocol/blob/master/doc/PROTOCOL.md), authors in the appendix) and are kept as they were. They describe the **device side** of the transport, which the Mi Home plugin bundles never show: the bundles hand a method name and parameters to the host SDK ([transports](transports.md)). Statements here are therefore ⚪ Legacy / external, not ✅ Bundle. What the bundles do show is in [JSON-RPC envelope](json-rpc-envelope.md) and [generic methods](#generic-methods) below.

The **Mi Home Binary Protocol** is used to configure & control smart home devices made by Xiaomi.

It is an encrypted, binary protocol, based on UDP. The designated port is 54321.

## Packet format

     0                   1                   2                   3   
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | Magic number = 0x2131         | Packet Length (incl. header)  |
    |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
    | Unknown1                                                      |
    |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
    | Device ID ("did")                                             |
    |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
    | Stamp                                                         |
    |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
    | MD5 checksum                                                  |
    | ... or Device Token in response to the "Hello" packet         |
    |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
    | optional variable-sized data (encrypted)                      |
    |...............................................................|
    
                    Mi Home Binary Protocol header
           Note that one tick mark represents one bit position.
     
     Magic number: 16 bits
         Always 0x2131
         
     Packet length: 16 bits unsigned int
         Length in bytes of the whole packet, including the header.
      
     Unknown1: 32 bits
         This value is always 0,
         except in the "Hello" packet, when it's 0xFFFFFFFF
         
     Device ID: 32 bits
         Unique number. Possibly derived from the MAC address.
         except in the "Hello" packet, when it's 0xFFFFFFFF
 
     Stamp: 32 bit unsigned int
         continously increasing counter
         
     MD5 checksum:
         calculated for the whole packet including the MD5 field itself,
         which must be initialized with 0.
         
         In the special case of the response to the "Hello" packet,
         this field contains the 128-bit device token instead.
     
     optional variable-sized data:
         encrypted with AES-128: see below.
         length = packet_length - 0x20
          

## Initial handshake ("SmartConnect")

1. Client → Device

	This is what I call the "Hello packet". The client can send it as often as 
	they want and they will always get the same reply:
	
         0                   1                   2                   3   
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        | 0x2131                        | 0x0020                        |
        |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
        | 0xffffffff                                                    |
        |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
        | 0xffffffff                                                    |
        |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
        | 0xffffffff                                                    |
        |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
        | 0xffffffffffffffffffffffffffffffff                            |
        |                                                               |
        |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
      

2. Device → Client

         0                   1                   2                   3   
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        | 0x2131                        | 0x0020                        |
        |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
        | 0x00000000                                                    |
        |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
        | 0x12345678                                                    |
        |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
        | Stamp                                                         |
        |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
        | Token (128-bit)                                               |
        | All subsequent encryption is based on this number.            |
        |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-|
       
	The 128-bit token is used to identify the device and, more importantly, to 
	encrypt all further communication.

*Update 2017-02-23:* Xiaomi updated the device firmwares and only 
uninitialized devices reveal their token now. 

## Encryption
The variable-sized data payload is encrypted with the Advanced Encryption 
Standard (AES). A 128-bit key and Initialization Vector are both derived from 
the Token as follows:

    Key = MD5(Token)
    IV  = MD5(MD5(Key) + Token)
    
PKCS#7 padding is used prior to encryption.

The mode of operation is Cipher Block Chaining (CBC).

## Payloads
Most payloads are JSON commands, documented in the "Yeelight Inter-Operation 
Spec".

One critical exception is the transmission of the user's WiFi credentials:

    {
      'id': XXX, 
      'method': 'miIO.config_router',
      'params': {
        'ssid': 'WiFi network',
        'passwd': 'WiFi password',
        'uid': YYY
      }
    }

* `id` is a UNIX timestamp.
* `uid` identifies the device owner. The device will phone home and report this to Xiaomi.



<a id="generic-methods"></a>
## Generic methods

Besides the vacuum-specific calls in the [command reference](../commands/index.md), miIO devices answer a set of generic `miIO.*` methods. **Evidence:** the plugin bundles never send these, with one exception (`miIO.ota`, [system commands](../commands/system.md#miIO.ota)). The table is ⚪ Legacy (earlier versions of this repository, from device captures); nothing here could be confirmed or contradicted from the bundles.

| Method | Purpose (legacy) | Evidence |
|---|---|---|
| `miIO.info` | device and network details (`model`, `fw_ver`, `hw_ver`, `mac`, `ap`, `netif`, `life`) | ⚪ Legacy |
| `miIO.config_router` | provisions Wi-Fi credentials (see "Payloads" above) | ⚪ Legacy |
| `miIO.ota` | starts a firmware update from a URL | ✅ Bundle (a14, a15, a23 debug page) and ⚪ Legacy |
| `miIO.get_ota_progress` | firmware download progress | ⚪ Legacy (named, not described) |
| `miIO.get_ota_state` | firmware update state | ⚪ Legacy (named, not described) |
| `miIO.wifi_assoc_state` | Wi-Fi association state and counters | ⚪ Legacy |

### `miIO.info`

No parameters. Reply (legacy capture of a `rockrobo.vacuum.v1`, firmware 3.3.6_003061; values anonymised in the legacy text):

```json
{"partner_id": "", "id": 7840, "code": 0, "message": "ok",
 "result": {"hw_ver": "Linux", "fw_ver": "3.3.6_003061",
            "ap": {"ssid": "<SSID>", "bssid": "<MAC address>", "rssi": -63},
            "netif": {"localIp": "<IP address>", "mask": "<netmask>", "gw": "<IP address>"},
            "model": "rockrobo.vacuum.v1", "mac": "<MAC address>", "token": "<32 hex digits>", "life": 62848}}
```

Legacy field notes: `partner_id` and `code` unknown; `life` "life in minutes?"; `token` is the device token (the legacy example value is replaced by a placeholder here). On firmware from 2017 onwards the token is only revealed by uninitialised devices (see "Initial handshake").

### `miIO.wifi_assoc_state`

No parameters. Legacy capture:

```json
{"id": 37, "code": 0, "message": "ok",
 "result": {"state": "ONLINE", "auth_fail_count": 0, "conn_success_count": 1, "conn_fail_count": 0, "dhcp_fail_count": 0}}
```

### `miIO.ota`

Parameters (legacy; the bundles send the same keys, ✅ Bundle · a15 m13298):

```json
{"mode": "normal", "install": "1", "app_url": "http://<host>/<firmware>.pkg", "file_md5": "<md5 of the file>", "proc": "dnld install"}
```

Other firmware-related calls found in the bundles are in [system commands](../commands/system.md).

## See also

- [Transports and dispatch](transports.md)
- [JSON-RPC envelope](json-rpc-envelope.md)
- [Getting started](../getting-started/index.md)
- [Command index](../commands/index.md)

## Appendix
### Authors
This document is part of the [OpenMiHome project](https://github.com/openmihome). Authors include:

 * Wolfgang Frisch ([GitHub](https://github.com/wfr))
 
### Links
 * [Wireshark](https://www.wireshark.org/)
 * [Xiaomi MAC addresses](http://hwaddress.com/company/xiaomi-communications-co-ltd)
 * [Yeelight Inter-Operation Spec PDF](http://www.yeelight.com/download/Yeelight_Inter-Operation_Spec.pdf)
 * [PKCS#7 padding](https://en.wikipedia.org/wiki/Padding_\(cryptography\)#PKCS7)
