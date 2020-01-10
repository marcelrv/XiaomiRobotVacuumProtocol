# Mi Io Generic commands

These commands appear to be shared amngs all(?) Xiaomi Mi Io devices.

# Get Ota
## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `miIO.ota` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
miIO.ota '{"mode":"normal", "install":"1", "app_url":"http://IP/v11_#version#.pkg", "file_md5":"#md5#","proc":"dnld install"}'