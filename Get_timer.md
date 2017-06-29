# Cleaning Timer

This command sets the automatic start of the cleaning process.
It uses a cron-like notation of the cleaning schedule

## Command
| Key  | Value  | Comment  |
| ------- | ----------- | ------- |
| method | `get_timer` |  | 
| id   | [Integer] | is returned in the response used to link the send message to the response. |

### Example
`{'id': 1, 'method': 'get_timer'}`

## Response

|  Key  | Example | Description |
| ------------ |------ |------------------------------ |
|   |  _1498595924541_ | Entry time of this schedule (Unix time) |
|   |  _on_ | Is this schedule active |
|   |  _['38 9 28 6 *', ['start_clean', '']]]_ | Timing in [cron-like](https://en.wikipedia.org/wiki/Cron) notation. The time appears to be China timezone based (e.g. in Europe add + 6 hours to the CET time)|


```
   ┌───────────── minute (0 - 59)
   │ ┌───────────── hour (0 - 23)
   │ │ ┌───────────── day of month (1 - 31)
   │ │ │ ┌───────────── month (1 - 12)
   │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday;
   │ │ │ │ │                                       7 is also Sunday)
   │ │ │ │ │
   │ │ │ │ │
   * * * * *      command to execute
 ['1 5 * * 0,6', ['start_clean', '']]]
 ```
 
### Example Response

```
{'result': [
	['1498595924541', 'on', ['38 10 * * 0,6', ['start_clean', '']]], 
	['1498595904821', 'on', ['38 5 * * 1,2,3,4,5', ['start_clean', '']]], 
	['1498595882094', 'on', ['38 9 28 6 *', ['start_clean', '']]]
	], 
'id': 1}
```
