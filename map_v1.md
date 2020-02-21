# Map V1

Gets part of the URL to fetch the map from the Xiaomi cloud.
With the proper cloud decoding it can be retreived from the cloud independently of the Mi Home app
File can be retreived from the Xiaomi cloud  https://[country server].api.io.mi.com/app/home/getmapfileurl while passing  the response from below get_map_v1 as parameter. The response from this is a URL which the RR enconded map can be downloaded.

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
    "id": 2475
}
```

### Response

| Key | Example                        | Description         |
| --- | ------------------------------ | ------------------- |
| `-` | `"roboroommap%2255512245%2F1"` | Pointer to map data |

Returns ["retry"] without internet.

Note: this URLdecodes to  roboroommap"2255512245/1  where 2255512245 is the decimal representation of the deviceId, the digit after / appears to be a sequencial number 

#### Example

```json
{
    "result": ["roboroommap%2255512245%2F1"],
    "id": 2475
}
```
