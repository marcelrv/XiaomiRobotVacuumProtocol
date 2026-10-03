<a id="xiaomi-robot-vacuum-protocol"></a>
# Xiaomi / Roborock Robot Vacuum Protocol

The command reference for Xiaomi and Roborock robot vacuums that speak the **miIO** protocol: which methods exist, what parameters they take, what they return, which robot models the official app offers them for, and how maps are encoded. Every statement carries its evidence level: **Mi Home plugin bundles** (the programs the official app runs for each model) are the evidence; where a fact comes from elsewhere or cannot be determined, the page says so.

**For:** integrators (openHAB, Home Assistant, ioBroker, python-miio), tinkerers, and anyone asking "what does command X do, with which parameters, on which robot?".

## Quick start

1. [Get the token and the IP address](docs/getting-started/get-token-and-ip.md) of your robot.
2. [Send a first command](docs/getting-started/first-command.md), for example `{"id": 1, "method": "get_prop", "params": ["get_status"]}`.
3. Look up what you want to do in the [command index](docs/commands/index.md) and what your model offers on its [device page](docs/devices/index.md).

Implementations of the protocol: [openHAB](https://github.com/openhab/openhab-addons/tree/main/bundles/org.openhab.binding.miio) (Java), [python-miio](https://github.com/rytilahti/python-miio) (Python), [ioBroker mihome-vacuum](https://github.com/iobroker-community-adapters/ioBroker.mihome-vacuum) and [ioBroker roborock](https://github.com/copystring/ioBroker.roborock/) (JavaScript).

<a id="evidence-legend"></a>
## Evidence legend

Every page marks where a fact comes from:

| Badge | Meaning |
|---|---|
| ✅ **Bundle** | Verified in at least one Mi Home plugin bundle. The page names the models and, for non-trivial facts, a source anchor in the form `model@plugin version · m<module id> · "string anchor"` (module ids are numeric and local to one bundle). |
| 🔶 **openHAB** | Only in the openHAB miio binding; not seen in any bundle. Cross-check only. |
| ⚪ **Legacy** | Only in the earlier content of this repository (device captures, community knowledge); not confirmed by a bundle. |
| ❓ **Unknown** | Not determinable; the page says what was checked. |

Important distinction: **"the bundle calls it" is not "this robot's firmware answers it".** A call site proves that the official app can send the call and how it builds the parameters; it does not prove that a particular firmware responds. Details and limits: [methodology](docs/methodology.md#what-a-bundle-does-and-does-not-prove). Example payloads are labelled **constructed from app code** (values invented) or **legacy capture (unverified)**.

## Contents

| Section | What is in it |
|---|---|
| [Getting started](docs/getting-started/index.md) | token and IP, first command, troubleshooting |
| [Concepts](docs/concepts/index.md) | [miIO protocol](docs/concepts/miio-protocol.md), [JSON-RPC envelope](docs/concepts/json-rpc-envelope.md), [transports and dispatch](docs/concepts/transports.md), [feature flags](docs/concepts/feature-flags.md), [model generations](docs/concepts/model-generations.md), [maps overview](docs/concepts/maps-overview.md) |
| [Commands](docs/commands/index.md) | all 295 method strings found in the bundles, in 16 categories, with the [`user.*` alternate table](docs/commands/alternate-table.md) |
| [Reference](docs/reference/index.md) | [states](docs/reference/states.md), [errors](docs/reference/errors.md), [fan, water and mop values](docs/reference/fan-water-mop.md), [status fields](docs/reference/status-fields.md), [consumables](docs/reference/consumables.md), [dock](docs/reference/dock.md), [clean record](docs/reference/clean-record.md), [voice packs](docs/reference/voice-packs.md), [units](docs/reference/units.md), [other enumerations](docs/reference/other-enums.md) |
| [Devices](docs/devices/index.md) | one page per model, [command matrix](docs/devices/matrix-commands.md), [feature matrix](docs/devices/matrix-features.md) |
| [Maps](docs/maps/index.md) | [RR map file format](RRMapFile/RRFileFormat.md), sample files and viewers in [`RRMapFile/`](RRMapFile/README.md) |
| [Methodology](docs/methodology.md) | how the facts were derived, bundle inventory, limits, regeneration |
| [Appendix](docs/appendix/index.md) | [corrections](docs/appendix/corrections.md), [legacy captures](docs/appendix/legacy-captures.md), [unverified models](docs/appendix/unverified-models.md), [open questions](docs/appendix/open-questions.md), [glossary](docs/appendix/glossary.md) |
| [Tools and data](tools/README.md) | scripts that regenerate everything, and the machine-readable datasets in [`data/`](data/) |

## Analysed models

42 models were analysed from their own plugin bundle; pages are generated from [`data/models.json`](data/models.json). Names are tagged with their source on the device pages (Mi Home cloud device catalog, openHAB binding, legacy text). Models known only from other sources are in the [unverified models](docs/appendix/unverified-models.md) appendix.

| Model | Name (Mi Home cloud device catalog) | Plugin | Generation |
|---|---|---|---|
| [`roborock.vacuum.a01`](docs/devices/a01.md) | Roborock E Series | 1.0.51 | A |
| [`roborock.vacuum.a08`](docs/devices/a08.md) | Roborock S6 Pure | 1.0.47 | A |
| [`roborock.vacuum.a09`](docs/devices/a09.md) | Roborock T7 Pro | 1.0.48 | A |
| [`roborock.vacuum.a10`](docs/devices/a10.md) | Roborock S6 MaxV | 1.0.50 | A |
| [`roborock.vacuum.a11`](docs/devices/a11.md) | Roborock T7 | 1.0.34 | A |
| [`roborock.vacuum.a14`](docs/devices/a14.md) | Roborock T7S | 1.0.53 | B |
| [`roborock.vacuum.a15`](docs/devices/a15.md) | Roborock S7 | 1.0.53 | B |
| [`roborock.vacuum.a19`](docs/devices/a19.md) | Roborock S4 Max | 1.0.52 | A |
| [`roborock.vacuum.a23`](docs/devices/a23.md) | Roborock T7S Plus | 1.0.53 | B |
| [`roborock.vacuum.a26`](docs/devices/a26.md) | Roborock G10S Pro | 1.0.84 | B |
| [`roborock.vacuum.a27`](docs/devices/a27.md) | Roborock S7 MaxV | 1.0.84 | B |
| [`roborock.vacuum.a29`](docs/devices/a29.md) | Roborock G10 | 1.0.75 | B |
| [`roborock.vacuum.a30`](docs/devices/a30.md) | Roborock G10 | 1.0.75 | B |
| [`roborock.vacuum.a34`](docs/devices/a34.md) | Roborock Q5 | 1.0.70 | B |
| [`roborock.vacuum.a37`](docs/devices/a37.md) | Roborock T8 | 1.0.70 | B |
| [`roborock.vacuum.a38`](docs/devices/a38.md) | Roborock Q7 Max | 1.0.70 | B |
| [`roborock.vacuum.a40`](docs/devices/a40.md) | Roborock Q7 | 1.0.70 | B |
| [`roborock.vacuum.a46`](docs/devices/a46.md) | Roborock G10S | 1.0.84 | B |
| [`roborock.vacuum.a51`](docs/devices/a51.md) | Roborock S8 | 1.0.83 | B |
| [`roborock.vacuum.a52`](docs/devices/a52.md) | Roborock T8 Plus | 1.0.70 | B |
| [`roborock.vacuum.a62`](docs/devices/a62.md) | Roborock S7 Pro Ultra | 1.0.69 | B |
| [`roborock.vacuum.a64`](docs/devices/a64.md) | Roborock G10S Pure | 1.0.95 | B |
| [`roborock.vacuum.a65`](docs/devices/a65.md) | Roborock S7 Max Ultra | 1.0.95 | B |
| [`roborock.vacuum.a66`](docs/devices/a66.md) | Roborock G10 Plus | 1.0.84 | B |
| [`roborock.vacuum.a69`](docs/devices/a69.md) | Roborock G20 | 1.0.86 | B |
| [`roborock.vacuum.a70`](docs/devices/a70.md) | Roborock S8 Pro Ultra | 1.0.83 | B |
| [`roborock.vacuum.a72`](docs/devices/a72.md) | Roborock Q5 Pro | 1.0.92 | B |
| [`roborock.vacuum.a73`](docs/devices/a73.md) | Roborock Q8 Max | 1.0.92 | B |
| [`roborock.vacuum.a74`](docs/devices/a74.md) | Roborock P10 | 1.0.96 | B |
| [`roborock.vacuum.a75`](docs/devices/a75.md) | Roborock Qrevo | 1.0.89 | B |
| [`roborock.vacuum.a76`](docs/devices/a76.md) | Roborock G10S Auto | 1.0.77 | B |
| [`roborock.vacuum.c1`](docs/devices/c1.md) | Xiaowa C1 | 1.0.48 | A |
| [`roborock.vacuum.e2`](docs/devices/e2.md) | Xiaowa E Series | 1.0.48 | A |
| [`roborock.vacuum.m1s`](docs/devices/m1s.md) | Mi Robot Vacuum 1S | 1.0.34 | A |
| [`roborock.vacuum.p5`](docs/devices/p5.md) | Roborock P5 | 1.0.34 | A |
| [`roborock.vacuum.s4`](docs/devices/s4.md) | Roborock S4 | 1.0.47 | A |
| [`roborock.vacuum.s5`](docs/devices/s5.md) | Roborock S5 | 1.0.47 | A |
| [`roborock.vacuum.s5e`](docs/devices/s5e.md) | Roborock S5 Max | 1.0.49 | A |
| [`roborock.vacuum.s6`](docs/devices/s6.md) | Roborock S6 | 1.0.47 | A |
| [`roborock.vacuum.t4`](docs/devices/t4.md) | Roborock T4 | 1.0.32 | A |
| [`roborock.vacuum.t6`](docs/devices/t6.md) | Roborock T6 | 1.0.32 | A |
| [`rockrobo.vacuum.v1`](docs/devices/v1.md) | Mi Robot Vacuum | 1.0.46 | A |

Generation A = older plugin, B = newer plugin ([model generations](docs/concepts/model-generations.md)).

## Numbers

295 method strings found in the bundles: 248 base strings and 47 with the `user.` prefix. 229 of the 248 base strings have a call site in at least one plugin. Per-bundle counts are in the [methodology](docs/methodology.md#bundle-inventory).

## Vacuum Commands

The old command table of this page is replaced by the [command index](docs/commands/index.md).

## Generic MiIO Commands

See [generic miIO methods](docs/concepts/miio-protocol.md#generic-methods).

## Ruby variant commands

See the [`user.*` alternate table](docs/commands/alternate-table.md).

## Stable links

Pages that earlier lived at the repository root (`status.md`, `custom_mode.md`, `fw_features.md`, `Protocol.md`, ...) remain as short pointers to their new place; the files in `RRMapFile/` did not move.

## Contributing

Corrections, captures from real robots and plugin bundles for missing models are welcome; see [methodology](docs/methodology.md#contributing). The documentation is generated from data and curated text: edit the curated files in [`tools/curated/`](tools/curated/) rather than the generated pages, and regenerate with the scripts described in [`tools/README.md`](tools/README.md).

## License

See [LICENSE](LICENSE).
