# Mi IO Generic - Update Firmware Over Air

Updates the firmware of the device.

## Update Firmware Over Air

### Command

| Key    | Value                                                                                           | Comment                                                                             |
| ------ | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| method | `"miIO.ota"`                                                                                    |                                                                                     |
| params | {"mode":"normal", "install":"1", "app_url":url, "file_md5":md5_checksum, "proc":"dnld install"} | `md5_checksum` = md5 checksum of the firmware file, `url` = url to download         |
| id     | `id`                                                                                            | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "mode": "normal",
    "install": "1",
    "app_url": "http://IP/v11_#version#.pkg",
    "file_md5": "#md5#",
    "proc": "dnld install"
}

```
