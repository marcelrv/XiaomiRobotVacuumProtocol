# Voice Pack Installation Command

This command initiates the download and installation of voicefiles

## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `dnld_install_sound` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |
| params | `{"md5":"#MD5#","sid":1005,"url":"http://PATH TO SERVER/FILE.pkg","sver":2}` |  md5 = md5 checksum of the soundfile, sid = id of soundfile, url = url to download, sver = version of the soundfile for robot v2 and v1 with firmware versions 3.3.9_003194 or newer |

### Example

`{"id": 1, "method": "dnld_install_sound", "params": {"md5":"#MD5#","sid":1005,"url":"http://PATH TO SERVER/FILE.pkg","sver":2} }`

### Example Response
Standard response to succeeded commands

`{ "result": 0, "id": 17694 }`
