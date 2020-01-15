# Find Robot

The vacuum cleaner emits a sound (e.g. "Hey, here I am!") so you can find it.

## Find Me

### Command

| Key    | Value       | Comment                                                                             |
| ------ | ----------- | ----------------------------------------------------------------------------------- |
| method | `"find_me"` |                                                                                     |
| id     | `id`        | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "find_me",
    "id": 12394
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 12394
}
```
