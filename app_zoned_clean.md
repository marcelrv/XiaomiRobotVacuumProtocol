# Zone Cleaning

This command starts the zone cleanup for robot v2 and v1 with firmware versions `3.3.9_003194` or newer.

## Command

| Key     | Value             | Comment                                                                                                                                                                     |
| ------- | -----------       | -------                                                                                                                                                                     |
| method  | `app_zoned_clean` |                                                                                                                                                                             |
| params  | `[List of zones]` | List of `zones` to clean.                                                                                                                                                   |
|         | `[zone]`          | A `zone` consists of a list of 5 integer values. The first four define the rectangle in map coordinates and the last integer defines the times this zone should be cleaned. |
| id      | `[Integer]`       | Random integer which is returned in the response used to link request and response.                                                                                         |

### Example
```json
{
  "id":8338,
  "method":"app_zoned_clean",
  "params":[
    [26234,26042,27284,26642,1], // zone A should be cleaned once
    [26232,25304,27282,25804,2], // zone B should be cleaned twice
    [26246,24189,27296,25139,3]  // zone C should be cleaned 3 times
  ]
}
```
