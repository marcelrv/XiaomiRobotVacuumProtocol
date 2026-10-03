# Units and conventions

[Home](../../README.md) / Reference / Units

The units the plugin assumes for numeric values on the wire. All entries were read from conversion code in the plugin (a65, plugin 1.0.95, unless another bundle is named); a unit that is not shown by a conversion is marked ❓ Unknown.

| Quantity | Wire unit | Evidence in the app | Where |
|---|---|---|---|
| Cleaned area (`clean_area`, clean-record `area`, summary `total_area` / `clean_area`) | square millimetres | divided by 1 000 000 (`fromSqmmToSqm`) | [status fields](status-fields.md), [clean record](clean-record.md) |
| Cleaning time (`clean_time`, record `duration`, summary time) | seconds | `fromSecToMin` for the display | [status fields](status-fields.md) |
| Unix timestamps (record `begin`/`end`, `last_clean_t`) | seconds since 1970-01-01 UTC | record ids must be larger than 1451577600 | [clean record](clean-record.md) |
| Map coordinates (zones, go-to targets, walls, map blocks) | millimetres | `x 50` on writes, `/ 50` on reads (one map pixel = 50 mm) | [map file format](../../RRMapFile/RRFileFormat.md#coordinates) |
| Consumable work times (`main_brush_work_time`, …) | seconds | divided by 3600 for hours | [consumables](../commands/consumables.md) |
| Battery | percent | `parseInt(status.battery)` | [status fields](status-fields.md) |
| Do-not-disturb start/end | hour and minute, 24 h | four separate integers | [timers](../commands/timers.md) |
| Timer schedule | cron string `"<min> <hour> <day> <month> <weekday>"` | see timer commands | [timers](../commands/timers.md) |
| Fan power, water flow, mop mode | enumerated codes | no physical unit | [fan, water and mop values](fan-water-mop.md) |
| Sound volume | integer 0-100 | the volume slider range | [sound commands](../commands/sound.md) |
| Water-box distance (`distance_off`) | ❓ Unknown | stored as `waterBoxDistance` without a conversion | [status fields](status-fields.md) |

Display units chosen by the user in the app (square metres or square feet, 12/24 h clock) are not part of the protocol.

## Conventions

- Booleans are integers `0` / `1` in almost every call and status field.
- Replies carry the payload in `result`, a one-element array for most queries (`result[0]`); a few queries return the object or array directly (the command pages say which).
- Parameters are positional arrays (`[…]`) for the older calls and objects (`{…}`) for the newer ones; the retry protocol wraps arrays in an object ([transports](../concepts/transports.md#retry-protocol)).

## See also

- [Status fields](status-fields.md)
- [Clean record fields](clean-record.md)
- [JSON-RPC envelope](../concepts/json-rpc-envelope.md)
