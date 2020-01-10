# Get Map

Gets part of the URL to fetch the map from the Xiaomi cloud.
Unfortunately no examples yet to retrieve it independently of the Mi Home app

## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `get_map_v1` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example

 {'method': 'get_map_v1', 'id': 2}
 
 ## Response

|  Key  | Example | Description |
| ------------- | :------ | :------------------------------ |
|  - |  `roboroommap%2255512245%2F1` | Pointer to map data |

### Example Response

{ "result": [ "roboroommap%2255512245%2F1" ], "id": 2 }

