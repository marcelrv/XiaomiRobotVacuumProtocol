# Remote Control

The remote controlling allows you to steer the Vacuum.

## Start Remote Control

### Command

| Key    | Value            | Comment                                                                             |
| ------ | ---------------- | ----------------------------------------------------------------------------------- |
| method | `"app_rc_start"` |                                                                                     |
| id     | `id`             | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "app_rc_start",
    "id": 1756
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 1756
}
```

## End Remote Control

### Command

| Key    | Value          | Comment                                                                             |
| ------ | -------------- | ----------------------------------------------------------------------------------- |
| method | `"app_rc_end"` |                                                                                     |
| id     | `id`           | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "app_rc_end",
    "id": 64346
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 64346
}
```

## Movement Remote Control

### Command

| Key    | Value                                                                       | Comment                                                                                                                                  |
| ------ | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| method | `"app_rc_move"`                                                             |                                                                                                                                          |
| params | `[[{"omega":angle, "velocity":speed, "seqnum":sequence, "duration":time}]]` | `angle` range from -3.1 to 3.1), `speed` range from -0.3 to 0.3, `sequence` needs to increment with each command (0-1000?), `time` in ms |
| id     | `id`                                                                        | Random integer which is returned in the response used to link request and response.                                                      |

#### Example

```json
{
    "id": 353,
    "method": "app_rc_end",
    "params": [[{
                "omega": 0.5712,
                "velocity": 0,
                "seqnum": 19,
                "duration": 1500
            }
        ]]
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 353
}
```
