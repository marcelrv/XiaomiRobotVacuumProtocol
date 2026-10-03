# Troubleshooting

[Home](../../README.md) / [Getting started](index.md) / Troubleshooting

| Symptom | Likely cause | Notes |
|---|---|---|
| No reply at all | wrong token; robot not reachable on UDP 54321; wrong IP | The robot ignores packets it cannot decrypt (external knowledge). |
| Works on the sofa, not from another network | VLAN / guest network / client isolation | Same as above. |
| `"result": "unknown_method"` | The firmware does not know the method | The official app treats this as "plugin needs an update" and shows *"New plugin required. Uninstall and reinstall the app before use."* ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)). A method that the bundle of your model calls may still be unknown to older firmware. |
| Reply with `error` | parameter error, busy, access denied | Map operations use the codes of [errors](../reference/errors.md#map-operation-errors-mapoperrorcode) (`-10005` parameter error, `-10002` access denied). |
| A command has no effect while the robot sleeps | The robot may be in state 2 (`SLEEPING`) | The app has an [`app_wakeup_robot`](../commands/cleaning-control.md#app_wakeup_robot) call and uses it before some actions (a65: the self-clean button when the state is sleeping, and the go-to page). Whether firmware ignores other commands while asleep is not shown by the bundles. |
| A map call returns a file name or `retry` | Maps are downloaded files, not inline data | See [maps overview](../concepts/maps-overview.md#how-a-map-reaches-the-app). |
| Edit calls answer `retry` | Slow operations use a retry handshake on firmware that announces the retry feature bit | See [retry protocol](../concepts/transports.md#retry-protocol). |
| Status shows an unfamiliar number | New state or error code | Look it up in [states](../reference/states.md) and [errors](../reference/errors.md); the bundles of different models carry different tables. |
| Call works in the app but not for you | The app may send it through the cloud or the MIoT tunnel | See [transports](../concepts/transports.md). |
| Timeouts when polling quickly | unknown | The app polls the status every 2 s (`LoopDelay` 2000 ms, ✅ Bundle); a shorter interval is untested here, so a similar rate is a safe starting point. |

## See also

- [First command](first-command.md)
- [Transports and dispatch](../concepts/transports.md)
- [Open questions](../appendix/open-questions.md)
