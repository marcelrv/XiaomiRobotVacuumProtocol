# Consumables

[Home](../../README.md) / [Commands](index.md) / Consumables

Wear counters of brushes, filters and sensors.

The app shows each consumable as "time spent / life" and offers a reset. The reset parameter is the key name of the
counter. The keys the plugin reads (✅ Bundle · a65 m14060 `fetchData`) are listed under
[`get_consumable`](#get_consumable).

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`get_consumable`](#get_consumable) | Returns the wear counters of brushes, filters and sensors. | ✅ Bundle |
| [`reset_consumable`](#reset_consumable) | Resets the counter named by the parameter. | ✅ Bundle |

<a id="get_consumable"></a>
### `get_consumable` — Read consumable counters

Returns the wear counters of brushes, filters and sensors.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` is an object. Keys read by the plugin:

| Key | Meaning in the app | Unit |
|---|---|---|
| `main_brush_work_time` | main brush | seconds (the red-point check divides by 3600, a65 m13970) |
| `side_brush_work_time` | side brush | seconds |
| `filter_work_time` | dust filter | seconds |
| `filter_element_work_time` | filter element (the app uses this key as "strainer/filter element" depending on product) | seconds |
| `sensor_dirty_time` | time since the sensors were cleaned | seconds |
| `moproller_work_time` | mop roller (dock models) | seconds |
| `strainer_work_times` | water strainer (clamped to ≥ 0) | cleaning counts |
| `cleaning_brush_work_times` | dock cleaning brush (clamped to ≥ 0) | counts |
| `dust_collection_work_times` | dust-collection uses; `-1` hides the row | counts |
| `dust_bag_work_times` | dust bag (dock models); no life value in most plugins | counts |
| `floor_cleaning_fluid` | floor cleaning fluid (dock models) | counts (nominal 300) |
| `mopSwabSupplies` | mop cloth entry of the supplies page (a pseudo key without a counter) | not stated |

Nominal lives (300 h main brush, 200 h side brush, 150 h filter, 30 h sensors, 100 h filter element, 300 h mop roller; counts for the others) are in [consumable keys and lives](../reference/consumables.md).

An entry whose value is `-1` is removed from the list shown to the user.

**Example** — legacy capture (unverified)

```json
{"result": [{"main_brush_work_time": 32030, "side_brush_work_time": 32030, "filter_work_time": 32030,
             "filter_element_work_time": 7037, "sensor_dirty_time": 34922}], "id": 3457}
```

**Behaviour in the app**

On failure the plugin retries after 1 s a limited number of times, then shows an error toast.

**Legacy documentation**

⚪ Legacy [consumable.md](../../consumable.md) lists the first five keys — confirmed; the other keys are new.
The unit `seconds` is confirmed indirectly: the app divides the time keys by 3600 to show hours.

**Related:** [`reset_consumable`](consumables.md#reset_consumable)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getSupplies`); call sites m13985, m14090; table key `GetSupplies` · anchor `"GetSupplies"`
- `a65@1.0.95` · wrapper m10115 (`getSupplies`); call sites m13970, m14060; table key `GetSupplies` · anchor `"GetSupplies"`
- `t4@1.0.32` · wrapper m10010 (`getSupplies`); call sites m11204, m11333; table key `GetSupplies` · anchor `"GetSupplies"`

</details>

<a id="reset_consumable"></a>
### `reset_consumable` — Reset a consumable counter

Resets the counter named by the parameter.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<key>]` — one of the key names of [`get_consumable`](#get_consumable) (the app passes the `suppliesKey` of the selected row).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code

```json
{"id": 111, "method": "reset_consumable", "params": ["filter_work_time"]}
```

**Related:** [`get_consumable`](consumables.md#get_consumable)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`resetSupplies`); call sites m14099; table key `ResetSupplies` · anchor `"ResetSupplies"`
- `a65@1.0.95` · wrapper m10115 (`resetSupplies`); call sites m14069; table key `ResetSupplies` · anchor `"ResetSupplies"`
- `t4@1.0.32` · call sites m11339; table key `ResetSupplies` · anchor `"ResetSupplies"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
