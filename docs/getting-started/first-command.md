# Send your first command

[Home](../../README.md) / [Getting started](index.md) / First command

The first call is a status request. The official app polls the status with the method `get_prop` and the single parameter `"get_status"` (✅ Bundle, all 42 bundles; [`get_prop`](../commands/status.md#get_prop)):

```json
{"id": 1, "method": "get_prop", "params": ["get_status"]}
```

The state and error codes of the reply are explained in [status fields](../reference/status-fields.md), [states](../reference/states.md) and [errors](../reference/errors.md). The example is **constructed from app code**; a real reply carries the fields listed in [status fields](../reference/status-fields.md) in `result[0]`.

## python-miio (external)

The python-miio project (`pip install python-miio`) provides a command line client. The command names changed between versions; check `miiocli --help`. A typical call looks like:

```
miiocli roborockvacuum --ip <robot ip> --token <token> status
miiocli roborockvacuum --ip <robot ip> --token <token> raw_command get_prop '["get_status"]'
```

`raw_command <method> <params>` sends any method of this reference. (External tool; syntax not verified here.)

## openHAB (external)

The openHAB miio binding discovers robots, asks for the token and offers channels for status, cleaning and maps; it can also send raw method calls. (🔶 openHAB; see the binding's own documentation for the syntax.)

## Raw UDP (outline)

1. Send the 32-byte "hello" packet to `<robot ip>:54321` and read the reply: it carries the device id and a time stamp ([packet format](../concepts/miio-protocol.md#packet-format)).
2. Derive key and IV from the token ([encryption](../concepts/miio-protocol.md#encryption)), encrypt the JSON above, add the header with the MD5 checksum, send it.
3. Decrypt the reply and read `result` ([JSON-RPC envelope](../concepts/json-rpc-envelope.md)).

Use a library unless you want to implement the packet format yourself.

## Next calls

- Start and stop: [`app_start`](../commands/cleaning-control.md#app_start), [`app_pause`](../commands/cleaning-control.md#app_pause), [`app_charge`](../commands/cleaning-control.md#app_charge).
- Fan power: [`set_custom_mode`](../commands/cleaning-modes.md#set_custom_mode) with the codes of [fan, water and mop values](../reference/fan-water-mop.md).
- Which commands your model's app offers: the [device page](../devices/index.md) of your model.

## See also

- [Get the token and the IP address](get-token-and-ip.md)
- [Troubleshooting](troubleshooting.md)
- [Command index](../commands/index.md)
