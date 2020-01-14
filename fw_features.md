# Firmware Features

Retrieves a list of supported firmware features of the device.

## Get Firmware Features

### Command

| Key    | Value               | Comment                                                                             |
| ------ | ------------------- | ----------------------------------------------------------------------------------- |
| method | `"get_fw_features"` |                                                                                     |
| id     | `id`                | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_fw_features",
    "id": 7177
}
```

### Response

| Key | Example | Description                                |
| --- | ------- | ------------------------------------------ |
| `-` | _111_   | Feature (see [list](#feature-codes) below) |

#### Example

```json
{
    "result": [111, 112, 113, 114, 115, 116, 117, 118, 119, 122, 125],
    "id": 7177
}
```

## Codes

### Feature Codes

| Code | Description |
| ---- | ----------- |
| 111  | ???         |
| 112  | ???         |
| 113  | ???         |
| 114  | ???         |
| 115  | ???         |
| 116  | ???         |
| 117  | ???         |
| 118  | ???         |
| 122  | ???         |
| 125  | ???         |
