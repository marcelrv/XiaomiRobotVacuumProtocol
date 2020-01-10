# Serial Number

Retreives the serial number from the device.

## Get Serial Number

### Command

| Key    | Value                 | Comment                                                                             |
| ------ | --------------------- | ----------------------------------------------------------------------------------- |
| method | `"get_serial_number"` |                                                                                     |
| id     | `id`                  | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_serial_number",
    "id": 1
}
```

### Response

| Key             | Example         | Description                   |
| --------------- | --------------- | ----------------------------- |
| `serial_number` | _1387100330000_ | Serial nr of the robot vacuum |

#### Example

```json
{
    "result": [{
            "serial_number": "1387100330000"
        }
    ],
    "id": 1
}
```
