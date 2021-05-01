# Sound Volume

Gets / sets / tests the sound volume.

## Get Sound Volume

### Command

| Key    | Value                | Comment                                                                             |
| ------ | -------------------- | ----------------------------------------------------------------------------------- |
| method | `"get_sound_volume"` |                                                                                     |
| id     | `id`                 | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_sound_volume",
    "id": 657
}
```

### Response

| Key | Example | Description         |
| --- | ------- | ------------------- |
| `-` | _100_   | Sound volume (in %) |

#### Example

```json
{
    "result": [100],
    "id": 657
}
```

## Change Sound Volume

### Command

 | Key    | Value                   | Comment                                                                             |
 | ------ | ----------------------- | ----------------------------------------------------------------------------------- |
 | method | `"change_sound_volume"` |                                                                                     |
 | params | `[volume]`              | `volume` level range from 0 to 100 (in %)                                           |
 | id     | `id`                    | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "change_sound_volume",
    "params": [55],
    "id": 624
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 624
}
```

## Test Sound Volume

### Command

| Key    | Value                 | Comment                                                                             |
| ------ | --------------------- | ----------------------------------------------------------------------------------- |
| method | `"test_sound_volume"` |                                                                                     |
| id     | `id`                  | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "test_sound_volume",
    "id": 546
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 546
}
```
