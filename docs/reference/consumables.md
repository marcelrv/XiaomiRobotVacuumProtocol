# Consumables: keys and nominal lives

[Home](../../README.md) / [Reference](index.md) / Consumables

The consumables the plugin shows on its supplies page, with the key of the [`get_consumable`](../commands/consumables.md#get_consumable) reply, the nominal life written in the plugin and the English name. Generated from [`data/consumables.json`](../../data/consumables.json) (`tools/js/extract_consumables.mjs`). The 22 RAM-bundle plugins with a `suppliesKey` table list all consumables; the 20 older plugins (a01 a08 a09 a10 a11 a14 a15 a19 a23 c1 e2 m1s p5 s4 s5 s5e s6 t4 t6 v1) use an older page layout with five time-based consumables whose lives are read from the layout by index.

| Reply key | English name | Nominal life | Unit | Defined in |
|---|---|---:|---|---|
| `filter_work_time` | Filter | 150 | hours (time keys) | all 42 |
| `side_brush_work_time` | Side brush | 200 | hours (time keys) | 10: a01 a11 c1 e2 m1s p5 s5 t4 t6 v1 |
| `side_brush_work_time` | Side Brush | 200 | hours (time keys) | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| `main_brush_work_time` | Main brush | 300 | hours (time keys) | 10: a01 a11 c1 e2 m1s p5 s5 t4 t6 v1 |
| `main_brush_work_time` | Main Brush | 300 | hours (time keys) | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| `sensor_dirty_time` | Sensors | 30 | hours (time keys) | all 42 |
| `filter_element_work_time` | Water tank filters | 100 | hours (time keys) | 7: a01 a11 c1 e2 p5 s5 t4 |
| `filter_element_work_time` | Water Tank Filter | 100 | hours (time keys) | 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 |
| `filter_element_work_time` | Water tank filter | 100 | hours (time keys) | 3: m1s t6 v1 |
| `moproller_work_time` | Wash Roller | 300 | hours (time keys) | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `mopSwabSupplies` | Mop |  | not stated (no life value) | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `strainer_work_times` | Water Filter | 150 | counts | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `cleaning_brush_work_times` | High-speed maintenance brush | 300 | counts | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `dust_collection_work_times` | Dustbin | 90 | counts | 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `dust_bag_work_times` | Dust bag |  | not stated (no life value) | 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 |
| `dust_bag_work_times` | Dust bag | 90 | counts | 1: a62 |
| `floor_cleaning_fluid` | Floor Cleaning Fluid | 300 | counts | 19: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a66 a69 a70 a72 a73 a75 a76 |
| `floor_cleaning_fluid` | Floor Cleaning Solution | 300 | counts | 3: a64 a65 a74 |

The unit column follows the plugin's `isUnitsTime` flag: time keys are shown in hours (the app divides the reported seconds by 3600), the other keys count uses. The life of a consumable is the value the progress bar is drawn against; whether a robot enforces it is not shown by the bundles.

## See also

- [Consumable commands](../commands/consumables.md)
- [Units](units.md)
