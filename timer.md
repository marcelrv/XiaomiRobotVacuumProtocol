# Cleaning Timer

Gets / Sets the automatic start of the cleaning process.
It uses a cron-like notation of the cleaning schedule.

## Get Cleaning Timer

### Command

| Key    | Value         | Comment                                                                             |
| ------ | ------------- | ----------------------------------------------------------------------------------- |
| method | `"get_timer"` |                                                                                     |
| id     | `id`          | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_timer",
    "id": 173
}
```

### Response

| Key | Example                                 | Description                                                                                                                                                    |
| --- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-` | _"1498595924541"_                       | `timer_id` corresponds to entry time of this schedule (Unix time)                                                                                              |
| `-` | _"on"_                                  | Is this schedule active                                                                                                                                        |
| `-` | _["38 9 28 6 *", ["start_clean", ""]]]_ | Timing in [cron-like](https://en.wikipedia.org/wiki/Cron) notation. The time appears to be China timezone based (e.g. in Europe add + 6 hours to the CET time) |

```txt
   ┌───────────── minute (0 - 59)
   │ ┌───────────── hour (0 - 23)
   │ │ ┌───────────── day of month (1 - 31)
   │ │ │ ┌───────────── month (1 - 12)
   │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday,
   │ │ │ │ │                                       7 is also Sunday)
   │ │ │ │ │
   │ │ │ │ │
   * * * * *      command to execute + parameter
 ["1 5 * * 0,6", ["start_clean", ""]]]
 ```

#### Example

```json
{
    "result": [
        ["1498595924541", "on", ["38 10 * * 0,6", ["start_clean", ""]]],
        ["1498595904821", "on", ["38 5 * * 1,2,3,4,5", ["start_clean", ""]]],
        ["1498595882094", "on", ["38 9 28 6 *", ["start_clean", ""]]]
    ],
    "id": 173
}
```

## Set Cleaning Timer

### Command

| Key    | Value                                            | Comment                                                                             |
| ------ | ------------------------------------------------ | ----------------------------------------------------------------------------------- |
| method | `"set_timer"`                                    |                                                                                     |
| params | `[[timer_id, [schedule, [command, parameter]]]]` | See above for the schedule settings. `timer_id` is used as sort of record id        |
| id     | `id`                                             | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "set_timer",
    "params": [["1498595904821", ["30 12 * * 1,2,3,4,5", ["start_clean", ""]]]],
    "id": 1734
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 1734
}
```

## Enable/Disable Cleaning Timer

### Command

| Key    | Value                   | Comment                                                                             |
| ------ | ----------------------- | ----------------------------------------------------------------------------------- |
| method | `"upd_timer"`           |                                                                                     |
| params | `[timer_id, de/active]` | `timer_id` see `get_timer`, `activate` = "on", `deactive` = "off"                   |
| id     | `id`                    | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "upd_timer",
    "params": ["1498595904821", "off"],
    "id": 634
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 634
}
```
