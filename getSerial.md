# Get Serial

Retreives the serial # from the device

## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `get_serial_number` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example

 `{'method': 'get_serial_number', 'id': 1} `

### Response

|  Key  | Example | Description |
| ------------ |------ |------------------------------ |
| `serial_number` |  _1387100330000_ | Serial nr of the robot vacuum |

### Example Response

{'result': [{'serial_number': '1387100330000'}], 'id': 1}
