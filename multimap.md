# Multimap

Gets network details.

## Get Info

### Command

| Key    | Value                    | Comment                                                                             |
| ------ | -------------            | ----------------------------------------------------------------------------------- |
| method | `"get_multi_maps_list"`  |                                                                                     |
| id     | `id`                     | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_multi_maps_list",
    "id": 7840
}
```
### Response

| Key               | Example                            | Description                    |
| ------------      | ---------------------------------- | ------------------------------ |
| `id`              | _7840_                             | Returned ID from request       |
| `result`          |                                    | Response to the command        |
| `max_multi_map`   | _4_                                | Maximum Saved maps             |
| `max_bak_map`     | _0_                                | Maximum backup maps            |
| `multi_map_count` | _3_                                | Actual stored maps             |
| `map_info`        | _array_                            | Array of storred maps          |
| `mapFlag`         | _0-4_                              | Map number                     |
| `length`          | _11_                               | ??                             |
| `name`            | _anyMapname_                       | Mapname from the map           |
| `bak_maps`        | _array_                            | Array of Backup maps           |

#### Example

```json
{
  "id": 36,
  "result": [
    {
      "max_multi_map": 4,
      "max_bak_map": 0,
      "multi_map_count": 3,
      "map_info": [
        {
          "mapFlag": 0,
          "add_time": 1619719086,
          "length": 11,
          "name": "Erdgeschoss",
          "bak_maps": []
        },
        {
          "mapFlag": 1,
          "add_time": 1619709702,
          "length": 5,
          "name": "TEST3",
          "bak_maps": []
        },
        {
          "mapFlag": 2,
          "add_time": 1619721286,
          "length": 0,
          "name": "",
          "bak_maps": []
        }
      ]
    }
  ],
  "exe_time": 100
}
```



### load Multimap

| Key    | Value                    | Comment                                                                             |
| ------ | -------------            | ----------------------------------------------------------------------------------- |
| method | `"load_multi_map"`  |                                                                                     |
| id     | `id`                     | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "load_multi_map",
    "params": [
        [1], // Mapnumber
    ],
    "id": 7840
}