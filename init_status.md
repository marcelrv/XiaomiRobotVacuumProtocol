# Initial Status

Retrieves the initial status of the device.

The `app_get_init_status` simply consists of [Locale Information](locale.md), [Firmware Features](fw_features.md) and the [Status Message](status.md).

## Get Initial Status

### Command

| Key    | Value                   | Comment                                                                             |
| ------ | ----------------------- | ----------------------------------------------------------------------------------- |
| method | `"app_get_init_status"` |                                                                                     |
| id     | `id`                    | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "app_get_init_status",
    "id": 5879
}
```

### Response

| Key            | Example & Description                   |
| -------------- | --------------------------------------- |
| `local_info`   | see [Locale Information](locale.md)     |
| `feature_info` | see [Firmware Features](fw_features.md) |
| `status_info`  | see [Status Message](status.md)         |

#### Example

```json
{
    "result": [{
            "local_info": {
                "name": "custom_A.03.0070_CE",
                "bom": "A.03.0070",
                "location": "de",
                "language": "en",
                "wifiplan": "",
                "timezone": "Europe/Berlin",
                "logserver": "awsde0.fds.api.xiaomi.com",
                "featureset": 1
            },
            "feature_info": [111, 112, 113, 114, 115, 116, 117, 118, 119, 122, 125],
            "status_info": {
                "state": 8,
                "battery": 100,
                "clean_time": 2496,
                "clean_area": 34912500,
                "error_code": 0,
                "in_cleaning": 0,
                "in_returning": 0,
                "in_fresh_state": 1,
                "lab_status": 1,
                "water_box_status": 1,
                "map_status": 3,
                "is_locating": 0,
                "lock_status": 0,
                "water_box_mode": 204,
                "water_box_carriage_status": 1,
                "mop_forbidden_enable": 1
            }
        }
    ],
    "id": 6652
}
```
