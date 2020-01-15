# Voice Pack Installation

This command initiates the download and installation of voicefiles

## Install Sound

### Command

| Key    | Value                                                       | Comment                                                                                                                              |
| ------ | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| method | `"dnld_install_sound"`                                      |                                                                                                                                      |
| params | `{"md5":md5_checksum, "sid":id, "url":url, "sver":version}` | `md5_checksum` = md5 checksum of the soundfile, `sid` = id of sound file, `url` = url to download, `sver` = version of the soundfile |
| id     | `id`                                                        | Random integer which is returned in the response used to link request and response.                                                  |

#### Example

```json
{
    "method": "dnld_install_sound",
    "params": {
        "md5": "#MD5#",
        "sid": 1005,
        "url": "http://PATH TO SERVER/FILE.pkg",
        "sver": 2
    },
    "id": 1794
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 1794
}
```
