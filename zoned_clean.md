# Zone Cleaning

Starts, stops and resumes the zone cleaning.

## Start Zone Cleaning

### Command

| Key    | Value                             | Comment                                                                                                                                                                     |
| ------ | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| method | `"app_zoned_clean"`               |                                                                                                                                                                             |
| params | `[array of [zone]]`               | List of `zone`s to clean.                                                                                                                                                   |
|        | `[zone]`=`[x1, y1, x2, y2, iter]` | A `zone` consists of a list of 5 integer values. The first four define the rectangle in map coordinates and the last integer defines the times this zone should be cleaned. |
| id     | `id`                              | Random integer which is returned in the response used to link request and response.                                                                                         |

#### Example

```json
{
    "method": "app_zoned_clean",
    "params": [
        [26234, 26042, 27284, 26642, 1], // zone A should be cleaned once
        [26232, 25304, 27282, 25804, 2], // zone B should be cleaned twice
        [26246, 24189, 27296, 25139, 3]  // zone C should be cleaned 3 times
    ],
    "id": 8338
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 8338
}
```

## Stop Zone Cleaning

### Command

| Key    | Value                | Comment                                                                             |
| ------ | -------------------- | ----------------------------------------------------------------------------------- |
| method | `"stop_zoned_clean"` |                                                                                     |
| id     | `id`                 | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "stop_zoned_clean",
    "id": 6341
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 6341
}
```

## Resume Zone Cleaning

### Command

| Key    | Value                  | Comment                                                                             |
| ------ | ---------------------- | ----------------------------------------------------------------------------------- |
| method | `"resume_zoned_clean"` |                                                                                     |
| id     | `id`                   | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "resume_zoned_clean",
    "id": 12363
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 12363
}
```
