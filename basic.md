# Basic Operations

The vacuum cleaner emits a sound (e.g. "Hey, here I am!") so you can find it.

## Start Cleaning

### Command

| Key    | Value         | Comment                                                                             |
| ------ | ------------- | ----------------------------------------------------------------------------------- |
| method | `"app_start"` |                                                                                     |
| id     | `id`          | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "app_start",
    "id": 6340
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 6340
}
```

## Stop Cleaning

### Command

| Key    | Value        | Comment                                                                             |
| ------ | ------------ | ----------------------------------------------------------------------------------- |
| method | `"app_stop"` |                                                                                     |
| id     | `id`         | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "app_stop",
    "id": 12363
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 12363
}
```

## Start Spot Cleaning

### Command

| Key    | Value        | Comment                                                                             |
| ------ | ------------ | ----------------------------------------------------------------------------------- |
| method | `"app_spot"` |                                                                                     |
| id     | `id`         | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "app_spot",
    "id": 63362
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 63362
}
```

## Pause Cleaning

### Command

| Key    | Value         | Comment                                                                             |
| ------ | ------------- | ----------------------------------------------------------------------------------- |
| method | `"app_pause"` |                                                                                     |
| id     | `id`          | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "app_pause",
    "id": 633
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 633
}
```

## Start Charging

### Command

| Key    | Value          | Comment                                                                             |
| ------ | -------------- | ----------------------------------------------------------------------------------- |
| method | `"app_charge"` |                                                                                     |
| id     | `id`           | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "app_charge",
    "id": 45334
}
```

### Response

Standard response to succeeded command.

#### Example

```json
{
    "result": ["ok"],
    "id": 45334
}
```
