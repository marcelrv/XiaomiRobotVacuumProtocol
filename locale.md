# Locale Information

Retrieves the locale information of the device.

## Get Locale Information

### Command

| Key    | Value              | Comment                                                                             |
| ------ | ------------------ | ----------------------------------------------------------------------------------- |
| method | `"app_get_locale"` |                                                                                     |
| id     | `id`               | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "app_get_locale",
    "id": 5879
}
```

### Response

| Key          | Example                     | Description                | Only available for |
| ------------ | --------------------------- | -------------------------- | ------------------ |
| `name`       | _custom_A.03.0070_CE_       | ?                          |                    |
| `bom`        | _A.03.0070_                 | Parts list ID of the robot |                    |
| `location`   | _de_                        | Setted location            |                    |
| `language`   | _en_                        | Setted  language           |                    |
| `wifiplan`   | _ _                         | ?                          |                    |
| `timezone`   | _Europe/Berlin_             | Setted  time zone          |                    |
| `logserver`  | _awsde0.fds.api.xiaomi.com_ | URL to the server          |                    |
| `featureset` | _1_                         | ?                          | s5e                |

#### Example

```json
{
    "result": [{
            "name": "custom_A.03.0070_CE",
            "bom": "A.03.0070",
            "location": "de",
            "language": "en",
            "wifiplan": "",
            "timezone": "Europe/Berlin",
            "logserver": "awsde0.fds.api.xiaomi.com",
            "featureset": 1
        }
    ],
    "id": 5879
}
```
