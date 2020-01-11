# Water Box Custom Mode

Gets / sets the water quantity control during the cleaning process.

## Get Water Box Custom Mode

### Command

| Key    | Value                         | Comment                                                                             |
| ------ | ----------------------------- | ----------------------------------------------------------------------------------- |
| method | `"get_water_box_custom_mode"` |                                                                                     |
| id     | `id`                          | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_water_box_custom_mode",
    "id": 17735
}
```

### Response

| Key | Example | Description                                    |
| --- | ------- | ---------------------------------------------- |
| `-` | _201_   | Water flow mode, see values of [Modes](#modes) |

#### Example

```json
{
    "result": [201],
    "id": 17735
}
```

## Set Water Box Custom Mode

### Command

| Key    | Value                         | Comment                                                                             |
| ------ | ----------------------------- | ----------------------------------------------------------------------------------- |
| method | `"set_water_box_custom_mode"` |                                                                                     |
| params | `[water_flow_mode]`           | Desired `water_flow_mode`, see [Modes](#modes)                                      |
| id     | `id`                          | Random integer which is returned in the response used to link request and response. |

#### Modes

| Mode             | Flow |
| ---------------- | ---- |
| Off              | 200  |
| Low              | 201  |
| Medium           | 202  |
| High             | 203  |
| Customize (Auto) | 204  |

The "Customize" switch in the Xiaomi app only shows `on` when both the [Custom Mode](custom_mode.md) is set to [Auto=106](custom_mode.md#extended-modes) and the [Water Box Custom Mode](water_box_custom_mode.md) is set to [Auto=204](water_box_custom_mode.md#modes).

#### Example

```json
{
    "method": "set_water_box_custom_mode",
    "params": [202],
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
