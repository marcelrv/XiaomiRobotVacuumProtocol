# Transports and call dispatch

[Home](../../README.md) / Concepts / Transports and dispatch

How the Mi Home plugin of a Roborock vacuum turns a button press into an RPC, and which routes a third-party integrator can rely on. Everything on this page was read from the plugin bundles (✅ Bundle) unless tagged otherwise; the primary reference code is the call wrapper `RobotApi` and the `RRMISDK` module of the a65 bundle (plugin 1.0.95, modules m10115 and m10046), cross-checked by script against all 42 bundles.

## The layers

```
UI code ──► RobotApi.<function>()  ──► asyncCallMethod(method, params)
                                            │  (generation B: retry protocol, see below)
                                            ├─ RRMISDK.isSpecSupported() ?  ──► MIoT action tunnel (siid 7, aiid 1)
                                            └─ otherwise ───────────────────► RRMISDK.callMethod ──► host SDK
```

| Layer | What it is | Evidence |
|---|---|---|
| `Protocol.Methods` | A table `Key -> method string`, for example `GetCustomMode -> "get_custom_mode"`. The table selected at start-up is the default (`rubyMethods`) one; models in the plugin's `saphireModelList` (the Xiaowa / Sapphire line: e2, c1 and, in the a01 family, a01 and a04) use a table whose strings carry the prefix `user.`; the `a01`, `c1` and `e2` bundles use a third table (`tanosMethods`). See [alternate table](../commands/alternate-table.md). | all bundles |
| `RobotApi` | A thin wrapper: one function per call (`getStatus`, `segmentClean`, `setCustomMode` …) that builds the parameters and calls `asyncCallMethod`. Present in all 42 bundles (older ones as a forwarding object, newer ones as a module with a literal call per function). | all bundles |
| `RRMISDK` | The plugin's own shim over the host app. When the plugin runs inside Mi Home (`isMiApp`, defined as "no `RRPluginSDK` global") the RPC goes to the Mi Home plugin SDK (`Device.getDeviceWifi().callMethod`). Inside Roborock's own app (not analysed here, but its branches are visible in the code) the call goes to `RRPluginSDK`. | a65 m10046 |
| Host SDK | Opaque to the bundles. It decides whether the RPC travels over the local network or through the Xiaomi cloud and adds the envelope (`id`, `result`/`error`). | not visible |

What the bundles therefore cannot tell you: the packet format, port, encryption and routing choice. These are the general miIO facts in [miIO protocol](miio-protocol.md).

## Routes inside `RRMISDK`

| Function | Behaviour inside Mi Home | Used for |
|---|---|---|
| `callMethod(method, params, extra, callback)` | `Device.getDeviceWifi().callMethod(method, params)`; the callback receives `(true, reply)` or `(false, error)` | almost every call |
| `callMethodFromCloud` | In Mi Home the body is identical to `callMethod`; the name only has an effect in the Roborock app. | `send_sdp_to_robot` ([camera](../commands/camera.md#send_sdp_to_robot)) |
| `callMethodForceWay` / `callMethodForceWayNew` | `Device.getDeviceWifi().callMethodFromLocal(method, params)`: the host is told to use the local route only | some call sites of [`app_pause`](../commands/cleaning-control.md#app_pause), [`app_rc_start`](../commands/remote-control.md#app_rc_start) and [`app_rc_move`](../commands/remote-control.md#app_rc_move) |
| `getMapData` / `getAndDecBase64Data` | map and photo download paths, see [maps overview](maps-overview.md#how-a-map-reaches-the-app) | [`get_map_v1`](../commands/maps.md#get_map_v1), [`get_multi_map`](../commands/maps.md#get_multi_map), [`get_map`](../commands/maps.md#get_map), [`get_photo`](../commands/maps.md#get_photo), [`get_clean_record_map`](../commands/clean-history.md#get_clean_record_map) |

The per-command pages show the route of each method under "Transport"; the data is in `via` of [`data/commands.json`](../../data/commands.json).

## MIoT tunnel (`miSpec`)

Present in the call wrapper of 32 bundles (a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6). It is switched on when

```js
isSpecSupported() { return isMiApp && (isTanosS() || isRubysE()); }
```

(identical in the 22 readable bundles that contain it; the minified ones have the same shape). `isTanosS()` lists `a14` and `a15` and their revision ids, `isRubysE()` lists `a19` and its revisions, so, according to the lists in the bundles, inside Mi Home only these three models use the tunnel (the other 29 bundles that contain the code never switch it on for their own model). The tunnel sends every RPC as a MIoT *action*:

| Field | Value |
|---|---|
| `did` | device id |
| `siid` / `aiid` | `7` / `1` |
| `in` | one base64 string holding `{"id": <counter>, "method": "<method>", "params": <params>}` |
| reply | `out[0]` is a base64 string holding the usual miIO reply (`{"id":…, "result":…}`) |

A reply without `out` is an error. The inner JSON is the same RPC as everywhere else, so documentation of a method applies to both routes. Whether other robots implement MIoT action 7/1 is ❓ Unknown (the bundles only show it for these three).

<a id="cloud-calls"></a>
## Cloud calls

Some things the app does are not robot RPCs at all: it asks the Mi Home plugin SDK or the Xiaomi cloud for map download addresses, account-side timer scenes, rooms, stored per-device settings and firmware update information. The list, with call sites and the models whose plugin contains each call, is [cloud and smart-home calls](../commands/cloud.md). They are **cloud only** and cannot be sent to the robot over local miIO. `RRMISDK.callSmartHomeAPI` is a no-op in all 42 bundles (it only calls its callback with an empty object), so the smart-home paths the code names never produce a request.

## Success and failure as the app sees it

`promiseWrap` (a65 m10115) resolves the promise when the host reports success **and** the reply has a truthy `result` **and** `result != "unknown_method"`. Everything else rejects with `{error: "error: <method>", data: <reply or "unknow reason">}`.

Consequences for integrators:

- A reply whose `result` is an empty value (`0`, `""`, `null`) is treated as a failure by the app.
- `"result": "unknown_method"` is how the app learns that firmware does not know a call. Several pages react to it explicitly: the saved-map list, the delete-map flow and the map-restore flow show the localized text *"New plugin required. Uninstall and reinstall the app before use."* (`plugin_need_update`) with an *OK* button (✅ Bundle · a65 m14174, m13862, m12527).
- The generic communication failure toast reads *"Robot response timeout due to unstable network connection. Restart and try again."* (`robot_communication_exception`).
- Some pages treat an `error` object with `error == -97` or `error.code == -12` as "ignore silently" (✅ Bundle · a65 m14174); the bundles do not explain the numbers.

<a id="retry-protocol"></a>
## Retry protocol (generation B)

Added in generation B ([model generations](model-generations.md)). It is active only if the robot announces it: `FeatureManager.isRPCRetrySupported()` is bit 26 of the low word of `new_feature_info` (`0x4000000`, [feature flags](feature-flags.md#new_feature_info)), and never for the method `retry_request` itself. Present in the call wrapper of all 25 generation-B bundles (a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76).

Methods that take part (the plugin's `SupportRetryMethods`; the list is identical in all 25 generation-B bundles; checked by script, including the minified ones):

`save_map`, `merge_segment`, `split_segment`, `name_segment`, `set_customize_clean_mode`, `load_multi_map`, `save_as_multi_map`, `set_clean_sequence`, `set_lab_status`, `set_timer`, `set_ignore_identify_area`, `set_ignore_carpet_zone`, `set_server_timer`.

Behaviour:

1. For a method on the list the parameters are wrapped: an array `[…]` becomes `{"data": […], "need_retry": 1}`; an object gets `"need_retry": 1` added.
2. If the reply is `{"result": "retry", "id": <n>}` the firmware is working asynchronously. The app waits 2 s and sends [`retry_request`](../commands/diagnostic.md#retry_request) with `{"retry_id": <n>, "method": "<method>", "retry_count": <k>}`.
3. A reply `result == "retry"` repeats step 2 until `retry_count` reaches 8; then the call fails with `reach_max_retry_count`. Any other reply completes the original call with that reply.
4. A `retry` reply without an `id` fails with `retry_id_invalid`.

(✅ Bundle · a65 m10115 `asyncCallMethod`.) This is an app-side convention; whether firmware that lacks the feature bit accepts `need_retry` is not shown by the bundles.

## Map download retry

The map path has its own retry loop (8 attempts, 1 s / 2 s delays) described in [maps overview](maps-overview.md#how-a-map-reaches-the-app).

## Status polling

The home page polls [`get_prop`](../commands/status.md#get_prop) with `["get_status"]` every 2000 ms (`LoopDelay`) and reads `result[0]`; the app never sends `get_status` itself as a method name (✅ Bundle, all bundles; see the command page for the exact wording and the legacy conflict).

## See also

- [miIO protocol](miio-protocol.md)
- [JSON-RPC envelope](json-rpc-envelope.md)
- [Feature flags](feature-flags.md)
- [Command index](../commands/index.md)
- [Methodology](../methodology.md)
