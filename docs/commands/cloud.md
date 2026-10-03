# Cloud and smart-home calls (not miIO)

[Home](../../README.md) / [Commands](index.md) / Cloud calls

Besides the miIO RPCs of the [command reference](index.md), the plugins call services of the Mi Home plugin SDK and the Xiaomi cloud. These are **cloud only**: an integrator that talks to the robot over the local network cannot use them, and none of them is a robot method. They are listed because they explain behaviour that otherwise looks like a robot feature (map download addresses, account-side timers, stored settings). Generated from [`data/cloud_calls.json`](../../data/cloud_calls.json) (`tools/js/extract_cloud_calls.mjs`) and `tools/curated/cloud_calls.yaml`; evidence tag ✅ Bundle for every row.

| Call | Kind | What the app does with it | Present in |
|---|---|---|---|
| `MHApi.getCountryInfo` | SDK helper | Reads the country information of the Mi Home account (callback with `countryInfo`); used for region logic. | all 42 |
| `callSmartHomeAPI(/scene/delete)` | SDK helper | Passes the path to the SDK helper (no-op, see below). | all 42 |
| `callSmartHomeAPI(/scene/edit)` | SDK helper | Passes the path to the SDK helper (no-op, see below). | all 42 |
| `callSmartHomeAPI(/scene/list)` | SDK helper | Passes the path to the SDK helper (no-op, see below). | all 42 |
| `callSmartHomeAPI(<computed path>)` | SDK helper | The generic helper itself (`callSmartHomeAPI(method, params, callback)` of the plugin's SDK shim). | all 42 |
| `getVoicePackageList` | SDK helper | Lists the special voice packs the account is entitled to for a serial number ([voice packs](../reference/voice-packs.md)). | 25: a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `Service.room.createRoom` | SDK service | Creates a Mi Home room by name. a65 m10046. | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| `Service.room.loadAllRoom` | SDK service | Lists the rooms of the Mi Home account (the plugin ignores the default room `mijia.roomid.default`). a65 m10046 `getRoomList`. | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| `Service.scene.createTimerScene` | SDK service | Creates a Mi Home timer scene for the device (`deviceId`, options); used when a timer is added through Mi Home (`miAddTimer`). a65 m10046. | all 42 |
| `Service.scene.loadTimerScenes` | SDK service | Loads the Mi Home timer scenes of the device (account-side timers, `deviceId`). a65 m10046. | all 42 |
| `Service.smarthome.batchGetDeviceDatas` | SDK service | Reads the cloud device property `prop.s_mixxx`, a JSON string in which the plugin keeps its own per-device settings by key (`getValue`). a65 m10046. | all 42 |
| `Service.smarthome.batchSetDeviceDatas` | SDK service | Writes that property back after changing one key (`setValue`). a65 m10046. | all 42 |
| `Service.smarthome.checkDeviceVersion` | SDK service | Asks the cloud for firmware update information of the device (`did`, `pid`); used for the firmware-upgrade hint. a65 m10046 `getFirmwareUpgradingInfo`. | all 42 |
| `Service.smarthome.getMapfileUrl` | SDK service | Asks the Mi Home cloud for a download address of a map object: argument `{model, obj_name}`, answer has `url`. Used by the map download after the robot returned a file name ([maps overview](../concepts/maps-overview.md#how-a-map-reaches-the-app)). a65 m10109. | all except a01 c1 e2 |
| `Service.smarthome.getRobomapUrl` | SDK service | Older name of the same map-address request (arguments `{model, obj_name}`), used by the a01-family map download. | 3: a01 c1 e2 |
| `Service.spec.doAction` | SDK service | MIoT action call; the plugin uses it as the transport tunnel for RPCs on a14, a15 and a19 ([transports](../concepts/transports.md#miot-tunnel-mispec)). Not a separate cloud API. | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| `Service.storage.getThirdUserConfigsForOneKey` | SDK service | Reads a per-user configuration value stored in the Xiaomi cloud by model and key. a65 m10046. | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| `Service.storage.setThirdUserConfigsForOneKey` | SDK service | Writes such a value. a65 m10046. | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |

## Smart-home endpoint paths named in the code

| Path | Present in |
|---|---|
| `/home/checkversion` | all 42 |
| `/home/device_list` | all 42 |
| `/home/getmapfileurl` | all 42 |
| `/scene/delete` | all 42 |
| `/scene/edit` | all 42 |
| `/scene/list` | all 42 |
| `/user/del_user_map` | all 42 |

`callSmartHomeAPI` is a no-op in every analysed bundle: its body only calls the callback with an empty object (`callback && callback({})`; a65 m10046). The paths `/scene/list`, `/scene/edit` and `/scene/delete` that the plugin passes to it, and the other smart-home paths in its constants table (`/home/getmapfileurl`, `/home/checkversion`, `/home/device_list`, `/user/del_user_map`), therefore never produce a request from these plugins; they are documented as the endpoints the code names.

## See also

- [Transports and dispatch](../concepts/transports.md)
- [Maps overview](../concepts/maps-overview.md)
- [Command index](index.md)
