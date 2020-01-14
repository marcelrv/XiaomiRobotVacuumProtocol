# Clean Summary

These commands retreive the cleaning history from the vacuum.

## Get Clean Summary

### Command

| Key    | Value                 | Comment                                                                             |
| ------ | --------------------- | ----------------------------------------------------------------------------------- |
| method | `"get_clean_summary"` |                                                                                     |
| id     | `id`                  | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_clean_summary",
    "id": 2
}
```

### Response

| Key | Example                                                                    | Description                    |
| --- | -------------------------------------------------------------------------- | ------------------------------ |
| `-` | _16414_                                                                    | Total cleaning time in sec     |
| `-` | _252165000_                                                                | Total area (in cm2)            |
| `-` | _9_                                                                        | Total # cleanups               |
| `-` | _[1497139200, 1496966400, 1496620800, 1496534400, 1496448000, 1496361600]_ | Array of cleaning records ID's |

#### Example

```json
{
    "result": [16414, 252165000, 9, [1497139200, 1496966400, 1496620800, 1496534400, 1496448000, 1496361600]],
    "id": 2
}
```

## Get Clean Record

### Command

| Key    | Value                | Comment                                                                             |
| ------ | -------------------- | ----------------------------------------------------------------------------------- |
| method | `"get_clean_record"` |                                                                                     |
| params | `[cleaning_id]`      | `cleaning_id` can be taken from the array of `get_clean_summary`.                   |
| id     | `id`                 | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_clean_record",
    "params": [1497139200],
    "id": 263
}
```

### Response

| Key | Example      | Description                 |
| --- | ------------ | --------------------------- |
| `-` | _1497163727_ | Start time (unix timestamp) |
| `-` | _1497165195_ | End time (unix timestamp)   |
| `-` | _1468_       | Cleaning duration (in s)    |
| `-` | _22902500_   | Area (in cm²)               |
| `-` | _0_          | Errors??                    |
| `-` | _1_          | Completed  (0=no, 1=yes)    |

#### Example

```json
{
    "result": [[1497163727, 1497165195, 1468, 22902500, 0, 1]],
    "id": 263
}
```
