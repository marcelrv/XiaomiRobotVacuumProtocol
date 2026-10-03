# Dock types and dock status

[Home](../../README.md) / Reference / Dock

How the Mi Home plugin classifies the docking station. The robot reports `dock_type` in its [status](status-fields.md#switch-words); the plugin maps it to a dock class and, from the class, decides which dock controls ([dock commands](../commands/dock.md)) it offers. Source: a65 (plugin 1.0.95) `RobotStatusManager` module m10010, with the presence of the helper functions checked by identifier scan in all 42 bundles.

## `dock_type` values

| `dock_type` | Plugin helper | Class used by the app | Capabilities implied by the class (app code) |
|---:|---|---|---|
| 0 | `isO0Dock` | basic charging dock | none of the below |
| 1 | `isO1Dock` | collect dock (`isCollectDock`) | auto-empty ("dust collection"); `isCollectDustDock` is true |
| 2 | `isO2Dock` | wash dock (`isWashDock`) | mop washing; `hasConnectedWashDock` is true |
| 3 | `isO3Dock` | collect + wash dock (`isCollectWashDock`) | auto-empty and mop washing; `isCollectDustDock` and `hasConnectedWashDock` true |
| 5 | `isOCDock` (uses the *original* value) | collect dock (`isCollectDock`) | the plugin rewrites the value 5 to 1 before storing it (and to 0 when the series is `a15`); `isOCDock()` is true only if the original value was 5 and the series is not `a15` |
| 6 | `isO3PlusDock` | collect + wash + dry dock (`isCollectWashDryDock`) | auto-empty, mop washing and mop drying |
| 7 | `isO4Dock` | collect + wash + dry dock | same class as 6 |
| 8 | `isPearlDock` | collect + wash + dry dock | same class as 6 |

- ✅ Bundle · a65 m10010, `status.dock_type` handling and the `isO*Dock` / `is*Dock` methods. The names O0…O4 are the plugin's identifiers; the bundles do not link them to marketing names of docks, so no marketing names are given here. Value 4 and values above 8 are not handled in the readable bundles (the minified ones were not checked for the numbers).
- The last non-negative `dock_type` is stored in app storage (key `DockType`) and read at start-up to show dock UI before the first status arrives (`lastDockType`).
- Value `-1` is used by the plugin's map code for "no dock information" (`DockType.Other`), see below.
- Identifier scan: the helper functions are present in a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76. In a34 a37 a38 a40 and a62 only O0-O3 and the original-5 test exist; a52 additionally knows O3+ and O4 but not Pearl. They are absent from a01 a08 a09 a10 a11 a14 a15 a19 a23 c1 e2 m1s p5 s4 s5 s5e s6 t4 t6 v1 (the 17 generation-A bundles plus a14, a15 and a23). The older bundles that show the emptying state (22; s4, s6, a08 and others) detect the dock in a different way that was not traced.

## Map dock icon (`DockType` enumeration)

The map view uses a two-value enumeration, independent of the table above: `Normal = 0` and `Other = -1` (name and value as the app defines them; see [other enumerations](other-enums.md#docktype)). A dock type of 0 selects the "Normal" dock image, any other non-negative type the "Other" image.

## Dock supply status (`dss`)

The status field `dss` is a bit field of 2-bit groups (see [status fields](status-fields.md#switch-words)): water level, clean water box, dirty water box, dust bag, water-box filter, cleaning fluid. The plugin names the groups but not the meaning of the four values of each group, so they are ❓ Unknown here.

## Dock-related status fields

| Field | Meaning | Reference |
|---|---|---|
| `dock_type` | dock class, above | this page |
| `dock_error_status` | dock error code | [errors](errors.md) |
| `wash_status`, `wash_ready` | washing task status and readiness | [status fields](status-fields.md#switch-words) |
| `dry_status`, `rdt` | drying in progress, remaining drying time | [status fields](status-fields.md) |
| `auto_dust_collection` | `0` = automatic emptying off | [status fields](status-fields.md#switch-words) |
| `water_box_status`, `water_shortage_status`, `distance_off` | water box, shortage and distance-off | [status fields](status-fields.md) |

## Modes of the dock

Enumerations for dock settings are collected in [other enumerations](other-enums.md): `DustCollectionMode`, `WashTowelMode`, `BackWashMode`, `MoppingType`.

## See also

- [Dock commands](../commands/dock.md)
- [Status fields](status-fields.md)
- [States](states.md) (washing, emptying and drying states)
- [Other enumerations](other-enums.md)
