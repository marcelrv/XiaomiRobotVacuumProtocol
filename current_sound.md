# Voice Command

This command retreives the current active voice and which is being installed

## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `get_current_sound` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example

`{'id': 1, 'method': 'get_current_sound'}`

## Response

|  Key  | Example | Description |
| ------------- | :------ | :------------------------------ |
|   `sid_in_use` |   _3_ | Active voice (English = 3) |
|  `sid_in_progress` | _0_ | Voice in progress of being installed (0=none) |

### Example Response
`{'result': [{'sid_in_use': 3, 'sid_in_progress': 0}], 'id': 1}`

