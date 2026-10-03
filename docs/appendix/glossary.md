# Glossary

[Home](../../README.md) / Appendix / Glossary

Terms as used in this repository.

| Term | Meaning |
|---|---|
| **miIO** | Xiaomi's device protocol: JSON requests (`method`, `params`, `id`) carried in encrypted UDP packets or through the cloud ([miIO protocol](../concepts/miio-protocol.md)). |
| **Plugin / bundle** | The React-Native program the Mi Home app downloads for a device model. "Bundle" is its JavaScript file(s). |
| **Plugin version** | `version` in the bundle's `project.json` (for example 1.0.95). Not a firmware version. |
| **SDK level** | `sdk_api_level` / `min_sdk_api_level` in `project.json`: the Mi Home plugin API level. |
| **Model id** | The device model string such as `roborock.vacuum.a65`. Revision-suffixed ids (`v2`...`v5`) are treated by the plugin as the same model. |
| **Product code name** | The plugin's own grouping of models into product lines (`TOPAZSC_CE`, `Ultron`, `Pearl`, ...), not a marketing name ([model generations](../concepts/model-generations.md)). |
| **Generation A / B** | Older plugins with model groups, newer plugins with a `DeviceModelManager` and the retry protocol ([model generations](../concepts/model-generations.md)). |
| **Call wrapper / `RobotApi`** | The plugin module with one function per RPC; all calls go through `asyncCallMethod` ([transports](../concepts/transports.md)). |
| **Called / wrapper only / declared only** | Evidence levels of a method string in a bundle: a call site exists / only a wrapper function exists / only the method table lists it. |
| **Method table** | The `Methods` object mapping app keys to method strings; three variants exist (default, `user.`-prefixed, a01-family). |
| **MIoT tunnel (`miSpec`)** | Sending the normal RPC as a MIoT action (siid 7, aiid 1) with a base64 JSON payload ([transports](../concepts/transports.md#miot-tunnel-mispec)). |
| **Retry protocol** | `need_retry` / `retry_request` handshake for slow operations ([transports](../concepts/transports.md#retry-protocol)). |
| **Feature code** | A number 101-130 in `feature_info` that the robot reports ([feature flags](../concepts/feature-flags.md#feature-codes)). |
| **Feature word** | `new_feature_info` (number) or `new_feature_info_str` (hex string): bit fields of capabilities ([feature flags](../concepts/feature-flags.md)). |
| **Gate / predicate** | A function in the plugin's `FeatureManager` (`isCarpetSupported()`) that decides whether a control is shown. |
| **Gate class `Y`, `FW`, `REG`, `RT`, `N`, `ERR`** | Results of evaluating a predicate in the sandbox ([feature flags](../concepts/feature-flags.md#how-the-gates-were-evaluated)). |
| **Segment / room** | A room of the map, identified by a number 0-31 in the map image and by room commands ([maps overview](../concepts/maps-overview.md)). |
| **Zone** | A rectangle on the map in millimetres, `[x1, y1, x2, y2]`. |
| **No-go zone, no-mop zone, virtual wall** | Forbidden areas written with `save_map` ([maps overview](../concepts/maps-overview.md#virtual-walls-and-forbidden-zones)). |
| **Multi-floor map** | Several saved maps on one robot (`get_multi_maps_list`, `load_multi_map`). |
| **Incremental map** | A map request with a `nonce` so that only changes are transferred ([maps overview](../concepts/maps-overview.md#incremental-maps)). |
| **Dock class** | Classification of the docking station from `dock_type` ([dock](../reference/dock.md)). |
| **Custom mode** | Fan power setting (`set_custom_mode`) ([fan, water and mop values](../reference/fan-water-mop.md)). |
| **Evidence badges** | ✅ Bundle, 🔶 openHAB, ⚪ Legacy, ❓ Unknown ([README](../../README.md#evidence-legend)). |
| **Constructed from app code** | An example payload built from the call site; values are invented. |
| **Legacy capture (unverified)** | An example from the earlier repository content that no bundle confirms. |

## See also

- [Methodology](../methodology.md)
- [README](../../README.md)
