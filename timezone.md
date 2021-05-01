# Timezone

Gets / resets the timezone.

## Get Timezone

### Command

| Key    | Value            | Comment                                                                             |
| ------ | ---------------- | ----------------------------------------------------------------------------------- |
| method | `"get_timezone"` |                                                                                     |
| id     | `id`             | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_timezone",
    "id": 30
}
```

### Response

| Key | Example              | Description                                                                            |
| --- | -------------------- | -------------------------------------------------------------------------------------- |
| `-` | _"Europe/Amsterdam"_ | Timezone name see [list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |

#### Example

```json
{
    "result": ["Europe/Amsterdam"],
    "id": 30
}
```

## Set Timezone

### Command

 | Key    | Value             | Comment                                                                                  |
 | ------ | ----------------- | ---------------------------------------------------------------------------------------- |
 | method | `"set_dnd_timer"` |                                                                                          |
 | params | `[timezone]`      | `timezone` name see [list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) |
 | id     | `id`              | Random integer which is returned in the response used to link request and response.      |

#### Example

```json
{
    "method": "set_timezone",
    "params": ["Europe/Amsterdam"],
    "id": 31
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 31
}
```
