# Room Mapping

Retrieves a list of segments.

## Get Room Mapping

### Command

| Key    | Value                | Comment                                                                             |
| ------ | -------------------- | ----------------------------------------------------------------------------------- |
| method | `"get_room_mapping"` |                                                                                     |
| id     | `id`                 | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_room_mapping",
    "id": 14837
}
```

### Response

| Key | Example        | Description    |
| --- | -------------- | -------------- |
| `-` | 16             | Segment number |
| `-` | "516001007152" | ?              |

#### Example

```json
{
    "result": [[16, "516001007152"], [17, "516001007153"], [18, "516001007151"], [19, "516001007154"]],
    "id": 14837
}

```
