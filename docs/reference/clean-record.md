# Clean record fields

[Home](../../README.md) / Reference / Clean record

The fields of one cleaning-history record as the plugin reads them, with units and the app's own labels. The calls are in [cleaning history](../commands/clean-history.md); enumerations for start types and finish reasons are in [other enumerations](other-enums.md#clean-record-start-types-start_type). Source: a65 (plugin 1.0.95) module m14012 (history page), `fetchRecordDetail`; the shape of the fixture file `*_unittest_ut_clean_record_data.json` shipped with the plugin.

## Two response layouts

[`get_clean_record`](../commands/clean-history.md#get_clean_record) returns `result[0]` in one of two layouts. The plugin picks the layout from `FeatureManager.isNewDataForCleanHistoryDetail()` ([feature word bit 23](../concepts/feature-flags.md#new_feature_info)).

| Meaning | Array position (older layout) | Object key (newer layout) | Unit / values |
|---|---:|---|---|
| start | 0 | `begin` | Unix time, seconds; also the record id |
| end | 1 | `end` | Unix time, seconds |
| duration | 2 | `duration` | seconds (list shows `<60` as "Ns", otherwise minutes, rounded) |
| area | 3 | `area` | square millimetres; the list shows `area / 1 000 000` with one decimal below 1 m², otherwise rounded square metres |
| error | 4 | `error` | error code, [errors](errors.md) |
| complete | 5 | `complete` | `0` = not finished, anything else = finished (`isCleanFinished: status != 0`) |
| start type | 6 | `start_type` | [start types](other-enums.md#clean-record-start-types-start_type); unknown values show "Unknown" |
| clean type | 7 | `clean_type` | `1` Full, `2` Zones, `3` Rooms (the app's labels `home_bottom_menu_global`, `_draw_zone`, `_select_zone`) |
| finish reason | 8 | `finish_reason` | [finish reasons](other-enums.md#clean-record-finish-reasons-finish_reason) |
| dust collected | - | `dust_collection_status` | non-zero adds "Dust collected" to the list line (only with the detail bit) |
| obstacle count | - | `avoid_count` | number of avoided obstacles |
| cleaning method | - | `clean_mop` | `0` / absent "Clean", `1` "Mop", `2` and `3` "Vac followed by Mop" |
| wash count | - | `wash_count` | mop washes during the run |
| wash time | - | `wash_time` | wash duration |
| map flag | - | `map_flag` | `-2` when absent (the app's default) |

✅ Bundle · a65 m14012. The unit of `wash_time` and the meaning of non-zero `map_flag` values are ❓ Unknown (the code only forwards them to the detail page).

After fetching, the plugin sorts the records by start time, newest first.

## Internal record shape and the fixture

After parsing, the plugin keeps every record as an object with the keys `start`, `stop`, `time`, `area`, `error`, `status`, `startType`, `cleanType` (plus `avoidCount`, `finishReasonCode`, `dustCollectionStatus`, `cleanMop`, `washCount`, `washTime`, `mapFlag`). The unit-test fixture shipped in the plugin uses this **internal** shape, not the robot's reply, so it matches neither reply layout. Example from the fixture (first entry; ✅ Bundle fixture data of the plugin authors, not a capture):

```json
{"start": 1554970378, "stop": 1554973516, "time": 1060, "area": 11432500, "error": 3, "status": 0, "startType": 2, "cleanType": 1}
```

## Summary totals

[`get_clean_summary`](../commands/clean-history.md#get_clean_summary) delivers `total_time` (seconds), `total_area` (square millimetres) and `total_count`; the history page shows the area as square metres (one decimal below 1 m²) and formats the time with its own unit helper (`getTimeUnit`). Newer layout names: `clean_time`, `clean_area`, `clean_count`, plus `dust_collection_count`, `mop_count`, `wash_count` on dock models.

## See also

- [Cleaning history commands](../commands/clean-history.md)
- [Other enumerations](other-enums.md)
- [Units and conventions](units.md)
