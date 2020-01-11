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

| Key    | Value               | Comment                                                                                               |
| ------ | ------------------- | ----------------------------------------------------------------------------------------------------- |
| method | `"set_custom_mode"` |                                                                                                       |
| params | `[level]`           | Desired fan level, see [Regular Modes](#regular-modes) or [Extended Modes](#extended-modes) (for s5e) |
| id     | `id`                | Random integer which is returned in the response used to link request and response.                   |

#### Regular Modes

| Mode     | Level |
| -------- | ----- |
| Quiet    | 38    |
| Balanced | 60    |
| Turbo    | 75    |
| Max      | 100   |
| Mop Mode | 105   |

#### Extended Modes

| Mode             | Level |
| ---------------- | ----- |
| Silent           | 101   |
| Balanced         | 102   |
| Turbo            | 103   |
| Max              | 104   |
| Gentle           | 105   |
| Customize (Auto) | 106   |

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
