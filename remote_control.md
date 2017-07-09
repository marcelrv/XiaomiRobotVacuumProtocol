# Remote Control

The remote controlling allows you to steer the Vacuum.

## Start Remote Control
### Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `app_rc_start` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
`{'id': 1, 'method': 'app_rc_start'}`

## End Remote Control
### Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `app_rc_end` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
`{'id': 1, 'method': 'app_rc_end'}`

## Remote Control Movement
### Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `app_rc_move` |  | 
| params | `[{"omega":angle ,"velocity":Speed,"seqnum":sequence #,"duration":time in MS}]` | omega range -3.1 , 3.1 speed range -0.3 , 0.3. Sequence number needs to increment with each command 0-1000? | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
`{'id': 1, 'method': 'app_rc_end' , 'params': [[{"omega":0.5712,"velocity":0,"seqnum":19,"duration":1500}]] }
