# Voice packs

[Home](../../README.md) / Reference / Voice packs

What the plugin knows about robot voice packs and how it installs one. The robot-side calls are in [sound commands](../commands/sound.md); this page documents the **catalogue** the plugin works from and the flow it builds around it. Source: a65 (plugin 1.0.95) modules m14117 (`SoundPackageManager`) and m14108 (`SoundPackagePage`), and the resource `*_setting_soundpackage_info_info.json` that ships in the plugin.

## Where the catalogue comes from

- At run time the plugin downloads a file named `info` from the content server of the robot's server region (path `DMM.soundPackageFilePath`, a per-product constant; a cache-busting `?time=` query is added) and parses it as JSON (✅ Bundle · a65 m14117 `getListDataFromServer`).
- The copy that ships inside the plugin (`*_setting_soundpackage_info_info.json`) is used only when `RRMISDK.isAutoTestSupported()` is true, that is as a test fixture. It is a build-time snapshot, not the live list. It exists in the 25 generation-B bundles (a14 a15 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76) and is **identical in all of them** (same ids, languages and versions; checked by script).
- Filtering: `voice_list` entries whose `applicable` array contains the robot location (`deviceLocation`, with `cn` replaced by `prc`) are kept and sorted by `voice_pri` ascending. Packs with `voice_id <= 999` are shown as standard packs, packs with `voice_id >= 1000` as personalized packs. Entries of `special_voice_list` are filtered the same way and additionally offered only if the Mi Home voice-package service lists them for the robot's serial number (`getVoicePackageList(sn)`, matched on `bizId == voice_id`); the service's `validEndTime` is attached to the entry.
- The plugin also downloads the preview audio of every listed pack and caches it under the name `<product bucket>_pre_<voice_id>_<version>.wav`.

The download locations inside the file are deliberately not reproduced here: they are addresses of Roborock content servers, and the plugin rewrites the host according to the robot's server region.

## Catalogue structure

| Key | Type | Meaning |
|---|---|---|
| `voice_pkg_version` | int | version of the catalogue (`1` in all bundles) |
| `voice_push_pic` | string | banner image address (not used by the commands) |
| `voice_list` | array | normal packs |
| `special_voice_list` | array | special packs; the plugin treats entries with `voice_id > 2000` as special (`isSpecialVoice`) |

Fields of every pack entry:

| Field | Type | Meaning |
|---|---|---|
| `voice_id` | int | pack id; sent as `sid` |
| `version` | int | pack version; sent as `sver`; the UI shows an update button when the installed version (`sid_version` from [`get_current_sound`](../commands/sound.md#get_current_sound)) is lower |
| `applicable` | string array | locations in which the pack is offered (`prc`, `tw`, `us`, `de`, `kr`, `ru`, `jp`); compared with the robot location |
| `lang` | string | language code (`prc`, `tw`, `en`); absent for the character packs |
| `voice_pri` | int | sort key, ascending |
| `voice_title`, `voice_sub_title` | string | display names (in the language of the pack; not localized through the string tables) |
| `bg_pic` | string | background picture address |
| `voice_pkg_url` | string | pack file address |
| `voice_pkg_md5` | string | md5 of the pack file; sent as `md5`. The value is identical for the first three entries, so it is not a per-pack digest there |
| `voice_pre_listen` | string | preview audio address |
| `validEndTime` | int | only in `special_voice_list`; the plugin overwrites it with the value returned by the voice-package service |

## Packs in the catalogue

| `voice_id` | Language / region key | Title as written in the file (gloss by the editor) |
|---:|---|---|
| 1 | `prc` | 标准普通话版 (standard Mandarin, classic female voice) |
| 2 | `tw` | 臺灣普通話版 (Taiwan Mandarin) |
| 3 | `en` | English (female voice) |
| 1001 | - | 粤语版 (Cantonese) |
| 1002 | - | 播音员版 (announcer, male voice) |
| 1003 | - | 后宫嫔妃版 (character voice) |
| 1004 | - | 动漫儿童版 (anime child) |
| 1005 | - | 机器人版 (robot voice) |
| 1006 | - | 萌妹子版 (cute girl) |
| 1007 | - | 妲己版 (character voice) |
| 2001 | - | Italiano (special) |
| 2002 | - | 日本語 (special) |

Packs 1001-1007 are offered for the locations `prc` and `tw` only; the glosses are the editor's translation, the plugin has no English names for them. Pack `9999` is handled specially by the installer (below) but is not part of the catalogue.

## Installing a pack

The plugin builds the request for [`dnld_install_sound`](../commands/sound.md#dnld_install_sound) from a catalogue entry (✅ Bundle · a65 m14108 `_onPressUseButton`):

- normal pack: `{"sid": voice_id, "url": "<https address on the regional server host>", "md5": voice_pkg_md5, "sver": version}`;
- reset to the built-in voice: `{"sid": voice_id, "default": <flag>, "sver": version}` (no `url`, no `md5`);
- for `voice_id == 9999` the address is the directory of the packs instead of a file.

While an installation runs the plugin polls [`get_sound_progress`](../commands/sound.md#get_sound_progress) every second; completion, failure and the meaning of `state` / `error` are described there. A second install request while one runs is refused by the UI with a toast.

## See also

- [Sound commands](../commands/sound.md)
- [Units and conventions](units.md)
