# Consumable

Gets / resets the status of the consumables.

## Get Consumable

### Command

| Key    | Value              | Comment                                                                             |
| ------ | ------------------ | ----------------------------------------------------------------------------------- |
| method | `"get_consumable"` |                                                                                     |
| id     | `id`               | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_consumable",
    "id": 2
}
```

### Response

| Key                        | Example | Description                                              |
| -------------------------- | ------- | -------------------------------------------------------- |
| `main_brush_work_time`     | _32030_ | Operating time of the main brush (in s)                  |
| `side_brush_work_time`     | _32030_ | Operating time of the side brush (in s)                  |
| `filter_work_time`         | _32030_ | Operating time of the filter (in s)                      |
| `filter_element_work_time` | _7037_  | Operating time of the filter element (in s)              |
| `sensor_dirty_time`        | _34922_ | Operating time of the sensors since last cleaning (in s) |

#### Example

```json
{
    "result": [{
            "main_brush_work_time": 32030,
            "side_brush_work_time": 32030,
            "filter_work_time": 32030,
            "filter_element_work_time": 7037,
            "sensor_dirty_time": 34922
        }
    ],
    "id": 12794
}
```

## Reset Consumable

### Command

| Key    | Value                | Comment                                                                                 |
| ------ | -------------------- | --------------------------------------------------------------------------------------- |
| method | `"reset_consumable"` |                                                                                         |
| params | `[consumable]`       | The `consumable` to be reset, the spelling corresponds to the keys of `get_consumable`. |
| id     | `id`                 | Random integer which is returned in the response used to link request and response.     |

#### Example

```json
{
    "method": "reset_consumable",
    "params": ["filter_work_time"],
    "id": 2
}
```
