# Clean Summary

These commands retreive the cleaning history from the vacuum.

## Get Clean Summary (older devices)

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

## Get Clean Summary (newer devices)

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

| Key | Example                                                                          | Description                    |
| --- | -------------------------------------------------------------------------------- | ------------------------------ |
| `clean_time` | _38629_                                                                 | Total cleaning time in sec     |
| `clean_area` | _650425000_                                                             | Total area (in cm2)            |
| `clean_count` | _68_                                                                   | Total # cleanups               |
| `dust_collection_count` | _0_                                                          | Total # cleanups               |
| `records` | _[1497139200, 1496966400, 1496620800, 1496534400, 1496448000, 1496361600]_ | Array of cleaning records ID's |

#### Example

```json
{ "id":5018,
   "result":{"clean_time":38629,"clean_area":650425000,"clean_count":68,"dust_collection_count":0,"records": 
              [1626292843,1626260657,1626255012,1626206412,1626174164,1626168621,1626036597,1626036415,1626035701,1626035555,1626033643,1626028227,1626021936,1626021732,1626021575,1626020891,1626020332,1626019286,1626019207,1626019147]
            },
   "exe_time":100
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

| Key | Example      | Description                  | Restrictions |
| --- | ------------ | ---------------------------  | ------------ |
| `-` | _1497163727_ | Start time (unix timestamp)  |              |
| `-` | _1497165195_ | End time (unix timestamp)    |              |
| `-` | _1468_       | Cleaning duration (in s)     |              |
| `-` | _22902500_   | Area (in cm²)                |              |
| `-` | _0_          | Errors??                     |              |
| `-` | _1_          | Completed  (0=no, 1=yes)     |              |
| `-` | _2_          | Unknown                      | s5e          |
| `-` | _3_          | Mode (1=full, 2=zone, 3=room)| s5e          |
| `-` | _60_         | Unknown                      | s5e          |

#### Example (generic)

```json
{
    "result": [[1497163727, 1497165195, 1468, 22902500, 0, 1]],
    "id": 263
}
```

#### Example (s5e)
```json
{
    "result": [[1497163727, 1497165195, 1468, 22902500, 0, 1, 2, 2, 60]],
    "id": 263
}
```

## Get Clean Record Map

Gets part of the URL to fetch the map from the Xiaomi cloud.
With the proper cloud decoding it can be retreived from the cloud independently of the Mi Home app
File can be retreived from the Xiaomi cloud  https://[country server].api.io.mi.com/app/home/getmapfileurl while passing  the response from below get_map_v1 as parameter. The response from this is a URL which the RR enconded map can be downloaded.

For decoding of the mapfile see [RR Map File](RRMapFile)

### Command

| Key    | Value                    | Comment                                                                             |
| ------ | ------------------------ | ----------------------------------------------------------------------------------- |
| method | `"get_clean_record_map"` |                                                                                     |
| params | `[cleaning_id]`          | `cleaning_id` can be taken from the array of `get_clean_summary`.                   |
| id     | `id`                     | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_clean_record_map",
    "params": [1497139200],
    "id": 263
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
