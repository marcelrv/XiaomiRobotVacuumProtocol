# Model generations and families

[Home](../../README.md) / Concepts / Model generations

The plugins of the 42 analysed models come in two code generations and three file formats. Models that share a plugin share its code, so the differences between them are decided by the gates described in [feature flags](feature-flags.md).

## Plugin generations

| Generation | Models | What distinguishes it in the code |
|---|---|---|
| **A** (17) | a01 a08 a09 a10 a11 a19 c1 e2 m1s p5 s4 s5 s5e s6 t4 t6 v1 | No `DeviceModelManager` module (the product is found with group functions of the `RRMISDK` module such as `isTanosS6()`, each a list of model ids) and no retry protocol in the call wrapper. Most generation-A bundles still contain a `RobotApi` wrapper and, in some, the MIoT tunnel code. |
| **B** (25) | a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 | A `DeviceModelManager` module (`DMM`) with a `Products` enumeration and a `DeviceInfoMap` (series → model ids, product, volume range); `FeatureManager` reads `DMM.currentProduct`. The call wrapper has the retry protocol ([transports](transports.md#retry-protocol)). |

The boundary is by presence of the `DeviceModelManager` module (✅ Bundle · `deviceModelManager` module id per bundle in [`data/bundles.json`](../../data/bundles.json)). Bundle versions ≈ app plugin versions (`project.json` `version`); they are **not** firmware versions.

## File formats

| Format | Bundles |
|---|---|
| plain JavaScript (one `main.bundle`) | a01 a08 a09 a10 a11 a14 a15 a19 a23 c1 e2 m1s p5 s4 s5 s5e s6 t4 t6 v1 |
| Metro indexed RAM bundle, minified | a26 a27 a29 a30 a46 a51 a66 a69 a70 a76 |
| Metro indexed RAM bundle, not minified | a34 a37 a38 a40 a52 a62 a64 a65 a72 a73 a74 a75 |

## Plugin versions

| Plugin version | Build date (UTC) | Models |
|---|---|---|
| 1.0.32 | 2020-01-03 | t4 t6 |
| 1.0.34 | 2020-03-17 … 2020-04-14 | a11 m1s p5 |
| 1.0.46 | 2020-11-18 | v1 |
| 1.0.47 | 2020-12-04 … 2020-12-08 | a08 s4 s5 s6 |
| 1.0.48 | 2020-12-25 … 2020-12-30 | a09 c1 e2 |
| 1.0.49 | 2021-01-05 | s5e |
| 1.0.50 | 2021-02-08 | a10 |
| 1.0.51 | 2021-03-03 | a01 |
| 1.0.52 | 2021-03-29 | a19 |
| 1.0.53 | 2021-04-01 … 2021-04-14 | a14 a15 a23 |
| 1.0.69 | 2022-05-10 | a62 |
| 1.0.70 | 2022-06-23 … 2022-07-21 | a34 a37 a38 a40 a52 |
| 1.0.75 | 2022-11-04 | a29 a30 |
| 1.0.77 | 2023-01-05 | a76 |
| 1.0.83 | 2023-06-30 … 2023-07-07 | a51 a70 |
| 1.0.84 | 2023-07-21 | a26 a27 a46 a66 |
| 1.0.86 | 2023-10-09 | a69 |
| 1.0.89 | 2023-12-12 | a75 |
| 1.0.92 | 2024-04-17 | a72 a73 |
| 1.0.95 | 2024-06-27 | a64 a65 |
| 1.0.96 | 2024-08-01 | a74 |

## Product code names

The plugin groups models into "products" with code names (not marketing names). The name is taken from the model's own bundle where it has one; models of generation A without a `DeviceModelManager` get their code name from the newest bundle's model table (marked with `*`; that bundle lists models it was not built for). The spelling differs between the two sources (for example `Rubyplus` from an own bundle, `RUBYPLUS` from the model table): each is the enumeration value as that bundle spells it.

| Product code name | Models |
|---|---|
| `Pearl` | a74 a75 |
| `Ruby` | v1 |
| `RUBY2` | m1s* |
| `Rubyplus` | s4 t4 |
| `Rubys` | s5 |
| `RubysC` | a08 p5 |
| `RubysE` | a19 |
| `RubysLite` | s5e |
| `Sapphire` | e2 |
| `SapphireCC` | c1 |
| `SapphireLiteCC` | a01 |
| `TanosE` | a11 |
| `TANOSS` | a14 a15 |
| `TanosS6` | s6 |
| `TANOSSC` | a40 |
| `TANOSSE` | a34 |
| `TANOSSL` | a37 a38 |
| `TANOSSMAX` | a52 |
| `TANOSSPLUS` | a23 |
| `TanosT6` | t6 |
| `TanosV` | a09 a10 |
| `TOPAZS` | a29 a76 |
| `TOPAZS_CE` | a30 |
| `TOPAZSC_CE` | a65 |
| `TOPAZSC_CN` | a64 |
| `TOPAZSPLUS` | a46 a66 |
| `TopazSPower` | a62 |
| `TOPAZSV_CE` | a27 |
| `TOPAZSV_CN` | a26 |
| `Ultron` | a51 |
| `UltronE` | a72 |
| `UltronLite` | a73 |
| `UltronSPlus` | a69 a70 |

## Revision-suffixed ids

Most bundles recognise a model id together with revision-suffixed ids `v2` … `v5` (for example `roborock.vacuum.a65v2`); they are listed on the device pages. A bundle is shared by all of them.

## Two special tables

- Bundles of `a01`, `c1`, `e2` choose a third method table (`tanosMethods`) instead of the default one ([`user.*` table](../commands/alternate-table.md)).
- A `user.`-prefixed alternate table exists in every bundle but is selected only for models in the plugin's `saphireModelList`, which names the Xiaowa / Sapphire robots (e2, c1, a01 family); no analysed bundle activates it for its own model (details in [alternate table](../commands/alternate-table.md)).

## See also

- [Devices](../devices/index.md)
- [Feature flags](feature-flags.md)
- [Methodology](../methodology.md)
