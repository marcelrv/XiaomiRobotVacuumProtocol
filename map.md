# Map

Edit the map e.g. to create software barrier or no-go zones.

The following commands require an activated [`Lab Status`](lab_status.md).

Without first enabling the `lab_status` will result in the following response: `The Lab Status is disable`.

## Save Map

### Command

| Key    | Value                                          | Comment                                                                                                                                                                            |
| ------ | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| method | `"save_map"`                                   |                                                                                                                                                                                    |
| params | `[array of [zone/barrier]]`                    | List of `zone`s or `barrier`s to add.                                                                                                                                              |
|        | `[zone]`=`[0, x1, y1, x2, y2, x3, y3, x4, y4]` | A `zone` consists of a list of 9 integer values. The first parameter defines the type (`0` = zone) and the last eight integers define the rectangle no-go zone in map coordinates. |
|        | `[barrier]`=`[1, x1, y1, x2, y2]`              | A `barrier` consists of a list of 5 integer values. The first parameter defines the type (`1` = barrier) and the last four integers define the barrier line in map coordinates.    |
| id     | `id`                                           | Random integer which is returned in the response used to link request and response.                                                                                                |

#### Example

```json
{
    "method": "save_map",
    "params": [
        [0, 27000, 32000, 30750, 32000, 30750, 30250, 27000, 30250], // no-go zone
        [1, 33800, 27850, 34900, 28700] // barrier
    ],
    "id": 263
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 263
}
```
