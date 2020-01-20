# Voice Pack Installation

These commands can be used to download language files and check the installation progress.

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

## Get Sound Installation Progress

### Command

| Key    | Value                  | Comment                                                                             |
| ------ | ---------------------- | ----------------------------------------------------------------------------------- |
| method | `"get_sound_progress"` |                                                                                     |
| id     | `id`                   | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_sound_progress",
    "id": 5172
}
```

### Response

| Key               | Example | Description                                   |
| ----------------- | ------- | --------------------------------------------- |
| `sid_in_progress` | _0_     | Voice in progress of being installed (0=none) |
| `progress`        | _0_     | Progress of installation                      |
| `state`           | _0_     | ?                                             |
| `error`           | _0_     | Error during installation                     |

#### Example

```json
{
    "result": [{
            "sid_in_progress": 0,
            "progress": 0,
            "state": 0,
            "error": 0
        }
    ],
    "id": 5172
}
```
