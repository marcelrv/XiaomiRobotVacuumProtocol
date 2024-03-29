# Segment Cleaning

Starts, stops and resumes the segment cleaning (= room cleaning).

## Start Segment Cleaning

### Command

| Key    | Value                 | Comment                                                                                                               |
| ------ | --------------------- | --------------------------------------------------------------------------------------------------------------------- |
| method | `"app_segment_clean"` |                                                                                                                       |
| params | `[array of segments]` or<br> `[{"segments": [array of segments], "repeat": <count of iterations>}]` | List of `segments` (rooms) to clean, to get `segments` the command [`get_room_mapping`](room_mapping.md) can be used. <br> You can also provide further information for each segemnts array like `repeat` for count of iterations |
| id     | `id`                  | Random integer which is returned in the response used to link request and response.                                   |

#### Example

```json
{
    "method": "app_segment_clean",
    "params": [16, 17, 18],
    "id": 6764
}
or
{
    "method": "app_segment_clean",
    "params": [{"segments": [16, 17, 18],"repeat": 2}],
    "id": 6764
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 3453
}
```

## Stop Segment Cleaning

### Command

| Key    | Value                  | Comment                                                                             |
| ------ | ---------------------- | ----------------------------------------------------------------------------------- |
| method | `"stop_segment_clean"` |                                                                                     |
| id     | `id`                   | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "stop_segment_clean",
    "id": 3453
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 3453
}
```

## Resume Segment Cleaning

### Command

| Key    | Value                    | Comment                                                                             |
| ------ | ------------------------ | ----------------------------------------------------------------------------------- |
| method | `"resume_segment_clean"` |                                                                                     |
| id     | `id`                     | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "resume_segment_clean",
    "id": 342
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 342
}
```
