# Corrections to the earlier documentation, and conflicts between sources

[Home](../../README.md) / [Appendix](index.md) / Corrections

What changed relative to the earlier content of this repository (⚪ Legacy, as of commit `be636c7`) because the plugin bundles say something different, where the bundles and the openHAB binding disagree, and what was only clarified. The bundle wins; the evidence is on the linked page.

## Corrections of statements in the old pages

| # | Old statement (⚪ Legacy) | Bundle finding (✅) | Where |
|---|---|---|---|
| 1 | `get_status` is a method that returns the status | No bundle sends `get_status` as a method. The app polls `get_prop` with the parameter `["get_status"]` every 2 s. Whether firmware also answers `get_status` directly is not shown by the bundles. | [`get_prop`](../commands/status.md#get_prop), [`get_status`](../commands/status.md#get_status) |
| 2 | README column "Only available for" (for example `s5e` only for `get_fw_features`, `app_get_init_status`, `get_network_info`, `change_sound_volume`, ...) | That list is not how the app gates: `app_get_init_status` is called by almost every bundle, `change_sound_volume` by all 42. `get_fw_features` is called only by the bundles of a01, c1, e2, s5 and v1; newer bundles read the same list from `feature_info` of `app_get_init_status`. The real gates (firmware feature codes, feature bits, product lines) are in [feature flags](../concepts/feature-flags.md) and on the device pages. | [command index](../commands/index.md), [devices](../devices/index.md) |
| 3 | `app_rc_move` parameter is a nested array `[[{...}]]`, `omega` +-3.1, `velocity` +-0.3 | Every bundle that sends it builds a single-level array `[{...}]`; the app never sends a negative velocity (0 to 0.29), and omega stays within +-1.05. | [`app_rc_move`](../commands/remote-control.md#app_rc_move) |
| 4 | Error code 20 is "Unknown Error" (old `status.md`; openHAB 🔶 agrees) | The a01, c1 and e2 bundles map code 20 to `Mouse`: "Please clean the motion tracking sensor and place the robot back to its original location and start it." No other bundle has an entry for 20. | [errors](../reference/errors.md) |
| 5 | Error 254 is "Bin full" | In the bundles 254 is an *internal error* entry present in the newer bundles; the "bin full" entry is code 644. | [errors](../reference/errors.md) |
| 6 | Map file digest block carries a 12-byte hash | The app validates a 20-byte SHA-1 (the last 20 bytes of the file against all bytes before them). | [map file format](../../RRMapFile/RRFileFormat.md#file-header-and-validation) |
| 7 | File header "data length points to the footer" | Header length + payload length equals the file length; the payload length is the length of everything after the file header. | [map file format](../../RRMapFile/RRFileFormat.md#file-header-and-validation) |
| 8 | Image pixel `00` outside, `01` wall, `FF` inside | Low 3 bits are the pixel type (0 outside, 1 wall/obstacle, others floor), upper 5 bits the room id 0-31; `FF` is floor of room 31. | [map file format](../../RRMapFile/RRFileFormat.md#pixel-values-of-the-image-block-type-2) |
| 9 | Status fields `msg_seq`, `clean_mode`, `begin_time`, `clean_trigger`, `back_trigger`, `clean_strategy`, `map_present` | No bundle reads them (identifier scan over all 42 bundles). They may still be returned by firmware. | [status fields](../reference/status-fields.md#legacy-only-fields) |
| 10 | Firmware feature code `115` is "Spot Clean" | No bundle tests code 115. Codes `113` (delete-map button), `118` and `130` are tested; `118` and `130` were unnamed. | [feature flags](../concepts/feature-flags.md#feature-codes) |
| 11 | Summary and record area (`clean_summary+record.md`) are in cm^2 | The app divides the value by 1 000 000 to show square metres, so the unit is **mm^2** (the legacy example 650425000 would be about 6.5 ha in cm^2 but 650 m^2 in mm^2). The old `status.md` already said mm^2 for the status field `clean_area`. | [clean record](../reference/clean-record.md), [units](../reference/units.md) |
| 12 | README typo `load_multi_map}` and the pair `GETSTATUS = app_get_status` | The method is `load_multi_map`; `app_get_status` exists only in the alternate table. | [`load_multi_map`](../commands/maps.md#load_multi_map) |

## Clarifications and extensions (not errors)

- **The `user.*` table.** The old README says "a few models take the same commands preceded by `user.`". The bundles **support** this: every bundle carries a second `Methods` table with the `user.` prefix, selected only for the models in the plugin's `saphireModelList`. That list names the Xiaowa/Sapphire line: `roborock.vacuum.e2`, `roborock.sweeper.e2v2`, `roborock.sweeper.e2v3`, `roborock.vacuum.c1`, `roborock.sweeper.c1v2`, `roborock.sweeper.c1v3` (and, in the a01-family plugins, `a01`, `a01v2`, `a01v3`, `a04`, `a04v2`, `a04v3`). No analysed bundle activates the table for its own model: the bundles of a01, c1 and e2 select a third table (`tanosMethods`) that only spells `user.dnld_install_sound`; every other bundle is built for a model outside the list. See [alternate table](../commands/alternate-table.md).
- **Command coverage.** 295 method strings were found in the bundles (248 without the `user.` prefix); most were not documented before (docks, camera, carpet, map editing, smart plans, ...).
- **Maps.** Blocks 20-34 and the new block 36 are documented from the app's parser; the charger block carries an angle only in newer parsers; the image header has an extra `blockNum` in all parsers except the first generation ([map file format](../../RRMapFile/RRFileFormat.md)).
- **Enumerations.** State, error, fan, water, mop, dock and clean-record tables with the app's English strings, including the second error table `ErrorsCodeToastMap` of the a01 family.
- **Feature words.** Two feature words (`new_feature_info`, `new_feature_info_str`) are decoded ([feature flags](../concepts/feature-flags.md)).
- **Old pages** were turned into pointer pages that keep the old anchors; the old JSON captures are kept in [legacy captures](legacy-captures.md).

<a id="bundle-vs-openhab-conflicts"></a>
## Bundle vs openHAB binding conflicts

Compared by script ([openHAB comparison](openhab-comparison.md), against the openHAB miio binding at commit `8d09a0997f` of `main`, 2026-10-02; the commit is recorded in `data/openhab_models.json`): the binding's `StatusType`, `VacuumErrorType`, `FanModeType`, `ConsumablesType` and `DockStatusType` against the bundle tables, plus the model names. Everything not listed agrees in meaning; the binding's error codes 25-45 and 126-150 agree with the bundles (only the wording differs, and the bundles map most of 126-150 to generic dock/inner-error texts).

| Topic | openHAB 🔶 | Bundles ✅ | Verdict |
|---|---|---|---|
| State 4 and 7 | 4 = "Remote Control", 7 = "Manual Mode" | The display map has 7 = remote control and no entry for 4; the app's own `RobotStateCode` constants list `REMOTE: 4`, `SEARCH_FOR_DOCK: 7`. | **Conflict between two tables inside the app**; the display map, which produces the shown text, says 7. Firmware behaviour for 4 is not shown by the bundles. |
| State 22 | "Returning Home" | "Emptying" (`COLLECTING_DUST`) | bundle wins |
| States 23-30, 202, 6301-6310 | not present | present | extended |
| Error 20 | "Unknown Error" | `Mouse` (a01, c1, e2) | bundle wins |
| Error 254 | "Bin full" | internal error; bin full is 644 | bundle wins |
| Error 21 | "Laser pressure sensor problem" | internal name `Lds`; newest title "Vertical Bumper Error", older plugins "Laser cover error" | wording (the bundles disagree among themselves) |
| Fan mode 105 | `MOB` | "Gentle", also the "mop only" marker (`NoClean`) | consistent in meaning |
| Fan mode 90 ("Full") | present | not in any bundle table | openHAB only |
| Fan mode 77 | "Power" | "Medium" (m1s) / 79 "power" in the sapphire table | codes differ by product |
| Consumable lives 300/200/150/30 h | main brush, side brush, filter, sensor | same nominal lives in the plugin | agree |
| Dock status 34, 38, 39 | suction, fresh water, dirty water | errors 34 (dock dustbin or air duct jammed), 38, 39 (tank checks) | agree |
| Dock status 46 | "Missing dust container/dust bag" | no error 46 in the bundles' table | openHAB only |
| Marketing name of `e2` | "Roborock Xiaowa E Series Vacuum v2" | "Xiaowa E Series" (catalog) | name |
| `a01` | no entry in the binding's model list | bundle exists | extended |
| Names of `a38`, `a40` | "Roborock Q7 Max" / "Roborock Q7" | catalog: same; the legacy text had "Q7 Max+" / "Q7+" | legacy names differ |

<a id="url-stability"></a>
## URL stability

Every page that existed at the repository root is still there as a short pointer to the new location that keeps the old section headings, so deep links to named old anchors (`status.md#error-codes`, `custom_mode.md#regular-modes`, ...) still land on a page. The generic old anchors (`#command`, `#example-1`, `#response`, ...) were dropped. The files in `RRMapFile/` stayed where they were; `RRMapFile/RRFileFormat.md` was rewritten in place. `Protocol.md` moved to [miIO protocol](../concepts/miio-protocol.md).

## See also

- [Methodology](../methodology.md)
- [Open questions](open-questions.md)
- [Glossary](glossary.md)
