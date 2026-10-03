# JSON-RPC envelope and result shapes

[Home](../../README.md) / Concepts / JSON-RPC envelope

Every call documented in the [command reference](../commands/index.md) is a small JSON object sent to the robot and a JSON object coming back. This page describes that envelope and the result and error shapes, separating what the plugin bundles show from what only the legacy documentation says.

## Request

```json
{"id": 12345, "method": "get_prop", "params": ["get_status"]}
```

| Key | Evidence | Notes |
|---|---|---|
| `method` | ✅ Bundle (all) | the strings in the [command index](../commands/index.md) |
| `params` | ✅ Bundle (all) | an array (older calls) or an object (newer calls); see below |
| `id` | ✅ Bundle (MIoT tunnel, a65 m10115): `{"id": <counter>, "method", "params"}`; ⚪ Legacy: "random integer which is returned in the response" | inside Mi Home the host SDK adds the `id`; the plugin only chooses it in the MIoT tunnel ([transports](transports.md#miot-tunnel-mispec)). It starts at a random multiple of 1000 and increases by one per call. |

Parameter shapes found in the plugin code (examples are on the command pages):

- no parameters: `[]` (or `{}` for a few newer calls);
- positional: `[42]`, `["get_status"]`;
- one object in an array: `[{"key": value}]` (for example `app_rc_move`, in every bundle) or a bare `{...}` (newer calls);
- nested: lists of rows, for example zones `[[x1, y1, x2, y2, repeats], …]` or timers `[[id, [cron, [action, …]]], …]`;
- the generation-B retry protocol turns an array into `{"data": […], "need_retry": 1}` for the methods on its list ([retry protocol](transports.md#retry-protocol)).

## Response

```json
{"id": 12345, "result": ["ok"]}
```

What the plugin code relies on (✅ Bundle · a65 m10115 `promiseWrap`, `miSpec`):

- The reply is an object with the key `result`. The call counts as successful only when `result` is truthy and is not the string `"unknown_method"`.
- `result` is most often an array whose first element is the payload (`result[0]`): an object (status), a number (volume), or a string. Some replies use `result` directly as an object or an array.
- `result: "unknown_method"` means the firmware does not know the method. The plugin reacts with the app string "New plugin required. Uninstall and reinstall the app before use." in several flows.
- `result: "retry"` (with an `id`) belongs to the generation-B retry protocol; `result: "locating"` is a map-file reply while the robot relocates ([maps overview](maps-overview.md#how-a-map-reaches-the-app)).
- Many write commands answer `["ok"]`; this is ⚪ Legacy (the legacy pages show it for every command). The plugin does not compare `result[0]` with `"ok"` for ordinary commands; it only checks that the call succeeded.

## Errors

The plugin looks at the failed reply in the keys `error`:

| Shape seen in code | Examples (✅ Bundle · a65) |
|---|---|
| `error` is a number | `-97` and `-3` (ignored silently by the map-list pages) |
| `error` is an object with `code` | `{"code": -10005}` parameter error, `{"code": -10010}` wrong password (`handleWrongPassword`), `{"code": -12}`, `{"code": -105}` too many rooms (map editing) |
| `error` is a string | `"timeout"` (treated as a communication failure) |
| `message` carries the error object | map editing (`result.message.error.code`) |

The numeric codes that the plugin names are in [errors](../reference/errors.md#map-operation-errors-mapoperrorcode) (map operations) and in the video error table; the meaning of `-97` and `-12` is not given in the bundles. Robot-side error conditions (stuck, brush blocked, …) are **not** RPC errors: they appear as `error_code` in the [status](../reference/status-fields.md) and are decoded in [errors](../reference/errors.md).

## Generic miIO replies (⚪ Legacy)

The legacy documentation of the generic `miIO.*` calls shows replies with `code`, `message` and `partner_id` beside `result`; see [miIO protocol](miio-protocol.md#generic-methods). The plugin bundles never send those calls (except `miIO.ota`), so this envelope variant has no bundle evidence.

## See also

- [Transports and dispatch](transports.md)
- [miIO protocol](miio-protocol.md)
- [Units and conventions](../reference/units.md)
- [Command index](../commands/index.md)
