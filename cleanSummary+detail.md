# Clean Summary

These commands retreive the cleaning history from the vacuum.

## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `get_clean_summary` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
`{'method': 'get_clean_summary', 'id': 2}`


## Response

|  Key  | Example | Description |
| ------------- | :------ | :------------------------------ |
|  - |  `16414` | Total cleaning time in sec |
|  - | `252165000` | total area (in cm2) |
|  - | `9` | Total # cleanups |
|  -  | `[ 1497139200, 1496966400, 1496620800, 1496534400, 1496448000, 1496361600 ]` | Array clean of cleaning records ID's |

### Example Response
```
{
   "result": [ 16414, 
               252165000, 
               9, 
               [ 1497139200, 1496966400, 1496620800, 1496534400, 1496448000, 1496361600 ] ],
   "id": 2 
}
```

# Clean Details
## Command
| Key  | Value  | Comment  |
| ------- | :----------- | ------- |
| method | `get_clean_record` |  | 
| params | `[1497139200]` |  Cleaning ID| 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
```
{
'method': 'get_clean_record'
'params': [1497139200], 
'id': 2, 
}
```

## Response

|  Key  | Example | Description |
| ------------- | :------ | :------------------------------ |
|  - |  `1497163727` | Start time (unix timestamp) |
|  - | `1497165195` | End time (unix timestamp) |
|  - | `1468` | Cleaning duration in secs |
|  -  | `22902500` | Area (in cm²) |
|  -  | `0` | Errors?? |
|  -  | `1` | Completed (Y/N) |

### Example Response
```
{
   "result": [ 
              [1497163727, 1497165195, 1468, 22902500, 0, 1]
             ],
   "id": 2 
}
```
