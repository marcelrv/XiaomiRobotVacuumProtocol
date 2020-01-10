# Custom Mode

Gets / sets the fan level during the cleaning process.
Fan level is also used to set the Mop mode of the Xiaomi Robot Vacuum 2.

## Get Custom Mode

### Command

| Key    | Value               | Comment                                                                             |
| ------ | ------------------- | ----------------------------------------------------------------------------------- |
| method | `"get_custom_mode"` |                                                                                     |
| id     | `id`                | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_custom_mode",
    "id": 17735
}
```

### Response

| Key | Example | Description    |
| --- | ------- | -------------- |
| `-` | _40_    | Fan level in % |

#### Example

```json
{
    "result": [40],
    "id": 17735
}
```

## Set Custom Mode

### Command

| Key    | Value               | Comment                                                                             |
| ------ | ------------------- | ----------------------------------------------------------------------------------- |
| method | `"set_custom_mode"` |                                                                                     |
| params | `[level]`           | Desired fan level                                                                   |
| id     | `id`                | Random integer which is returned in the response used to link request and response. |

To use mop mode, set the fan speed to 105

#### Regular Modes

| Mode     | Level |
| -------- | ----- |
| Quiet    | 38    |
| Balanced | 60    |
| Turbo    | 75    |
| Max      | 100   |
| Mop      | 105   |

#### Example

```json
{
    "method": "set_custom_mode",
    "params": [40],
    "id": 17694
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 17694
}
```
