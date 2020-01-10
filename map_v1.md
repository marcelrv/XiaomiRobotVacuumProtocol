# Map V1

Gets part of the URL to fetch the map from the Xiaomi cloud.
Unfortunately no examples yet to retrieve it independently of the Mi Home app

## Get Map V1

### Command

| Key    | Value          | Comment                                                                             |
| ------ | -------------- | ----------------------------------------------------------------------------------- |
| method | `"get_map_v1"` |                                                                                     |
| id     | `id`           | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_map_v1",
    "id": 1
}
```

### Response

| Key | Example                        | Description         |
| --- | ------------------------------ | ------------------- |
| `-` | `"roboroommap%2255512245%2F1"` | Pointer to map data |

#### Example

```json
{
    "result": ["roboroommap%2255512245%2F1"],
    "id": 2
}
```
