# Fan Power

This command gets/sets the fan level during the cleaning process.

# Get Fan Level Details
## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `get_custom_mode` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
`{'method': 'get_custom_mode', 'id': 17735}`

## response
|  Key  | Example | Description |
| ------------ |------ |------------------------------ |
| `-` |  _40_ | Fan level in % |

### Example
`{ "result": [ 40 ], "id": 17735 }`

# Set Fan level Details
## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `set_custom_mode` |  | 
| params | `[40] ` | Desired fan level |   
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
`{'method': 'set_custom_mode', 'params': [40],'id': 17694} `

### Example Response
Standard response to succeeded commands

`{ "result": 0, "id": 17694 }`
