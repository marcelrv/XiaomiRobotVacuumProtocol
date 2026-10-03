# Sound, voice packs and voice features

[Home](../../README.md) / [Commands](index.md) / Sound, voice packs and voice features

Volume, voice packs, audio playback and the voice-chat feature.

Voice packs are downloaded by the **robot itself** from a URL the app passes in. The app polls the progress once per
second ([`get_sound_progress`](#get_sound_progress)). The catalogue of packs (ids, languages, URLs, MD5) is a JSON file
shipped inside the generation-B bundles (`setting_soundpackage_info_info.json`; the plugin downloads the live list from a server, the shipped copy is a test fixture); its structure is described in
[voice packs](../reference/voice-packs.md).

## Commands in this category

| Method | Summary | Evidence |
|---|---|---|
| [`get_sound_volume`](#get_sound_volume) | Returns the current speaker volume. | ✅ Bundle |
| [`change_sound_volume`](#change_sound_volume) | Sets the speaker volume. | ✅ Bundle |
| [`test_sound_volume`](#test_sound_volume) | Makes the robot play a sound at the current volume. | ✅ Bundle |
| [`get_current_sound`](#get_current_sound) | Returns which voice pack is installed. | ✅ Bundle |
| [`dnld_install_sound`](#dnld_install_sound) | Orders the robot to download and install a pack. | ✅ Bundle |
| [`get_sound_progress`](#get_sound_progress) | Polled every second during an installation. | ✅ Bundle |
| [`play_audio`](#play_audio) | Sends an audio clip to be played by the robot. | ✅ Bundle |
| [`set_voice_chat_volume`](#set_voice_chat_volume) | Sets the volume used during a call. | ✅ Bundle |
| [`start_voice_chat`](#start_voice_chat) | Opens the robot audio channel for a call. | ✅ Bundle |
| [`stop_voice_chat`](#stop_voice_chat) | Closes the audio channel. | ✅ Bundle |
| [`enable_homesec_voice`](#enable_homesec_voice) | Turns the robot microphone on or off for the monitoring feature. | ✅ Bundle |

<a id="get_sound_volume"></a>
### `get_sound_volume` — Get the volume

Returns the current speaker volume.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` volume as an integer (the plugin `parseInt`s it).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_sound_volume", "params": []}
```

**Legacy documentation**

⚪ Legacy [sound_volume.md](../../sound_volume.md); the legacy README marks `change_sound_volume` / `test_sound_volume` "s5e only" — the bundles call both in all 42 bundles.

**Related:** [`change_sound_volume`](sound.md#change_sound_volume), [`test_sound_volume`](sound.md#test_sound_volume)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getSoundVolume`); call sites m14153, m14636; table key `GetSoundVolume` · anchor `"GetSoundVolume"`
- `a65@1.0.95` · wrapper m10115 (`getSoundVolume`); call sites m14123, m14582; table key `GetSoundVolume` · anchor `"GetSoundVolume"`
- `t4@1.0.32` · wrapper m10010 (`getSoundVolume`); call sites m11441, m11459; table key `GetSoundVolume` · anchor `"GetSoundVolume"`

</details>

<a id="change_sound_volume"></a>
### `change_sound_volume` — Set the volume

Sets the speaker volume.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `[<int>]`. The slider rounds to an integer; the value range per product comes from the bundle's volume table
(`Volumes`: default 30–90, Type1 30–100, Type2 50–90, Type3 20–90, Type4 5–90; ✅ Bundle · a65 m10139). The product-to-range
assignment is on the [device pages](../devices/index.md).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "change_sound_volume", "params": [50]}
```

**Behaviour in the app**

The slider calls `change_sound_volume` and then [`test_sound_volume`](#test_sound_volume) so that the robot plays a sample.

**Related:** [`get_sound_volume`](sound.md#get_sound_volume), [`test_sound_volume`](sound.md#test_sound_volume)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setSoundVolume`); call sites m14153, m14408, m14636; table key `SetSoundVolume` · anchor `"SetSoundVolume"`
- `a65@1.0.95` · wrapper m10115 (`setSoundVolume`); call sites m14123, m14378, m14582; table key `SetSoundVolume` · anchor `"SetSoundVolume"`
- `t4@1.0.32` · wrapper m10010 (`setSoundVolume`); call sites m11441, m11459; table key `SetSoundVolume` · anchor `"SetSoundVolume"`

</details>

<a id="test_sound_volume"></a>
### `test_sound_volume` — Play the volume test sound

Makes the robot play a sound at the current volume.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "test_sound_volume", "params": []}
```

**Related:** [`change_sound_volume`](sound.md#change_sound_volume)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`testSoundVolume`); call sites m14153, m14408; table key `TestSoundVolume` · anchor `"TestSoundVolume"`
- `a65@1.0.95` · wrapper m10115 (`testSoundVolume`); call sites m14123, m14378; table key `TestSoundVolume` · anchor `"TestSoundVolume"`
- `t4@1.0.32` · wrapper m10010 (`testSoundVolume`); call sites m11441, m11459; table key `TestSoundVolume` · anchor `"TestSoundVolume"`

</details>

<a id="get_current_sound"></a>
### `get_current_sound` — Current voice pack

Returns which voice pack is installed.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` = `{"sid_in_use": <pack id>, "sid_version": <int>, …}` (✅ Bundle · a65 m14117).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_current_sound", "params": []}
```

**Legacy documentation**

⚪ Legacy [current_sound.md](../../current_sound.md).

**Related:** [`dnld_install_sound`](sound.md#dnld_install_sound), [`get_sound_progress`](sound.md#get_sound_progress)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getCurrentSoundPackage`); call sites m14138, m14147, m14636; table key `GetCurrentSoundPackage` · anchor `"GetCurrentSoundPackage"`
- `a65@1.0.95` · wrapper m10115 (`getCurrentSoundPackage`); call sites m14108, m14117, m14582; table key `GetCurrentSoundPackage` · anchor `"GetCurrentSoundPackage"`
- `t4@1.0.32` · wrapper m10010 (`getCurrentSoundPackage`); call sites m10013, m11006, m11426; table key `GetCurrentSoundPackage` · anchor `"GetCurrentSoundPackage"`

</details>

<a id="dnld_install_sound"></a>
### `dnld_install_sound` — Download and install a voice pack

Orders the robot to download and install a pack.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 39: a08 a09 a10 a11 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 m1s p5 s4 s5 s5e s6 t4 t6 v1 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: one object `{"sid": <pack id>, "url": "<https url of the .pkg>", "md5": "<md5 of the file>", "sver": <int version>}`
(✅ Bundle · a65 m14108; `url` is built from the host of the pack list and the path in the catalogue; pack id `9999`
uses the directory URL only). In the alternate (`saphire`) table the same call is spelled `user.dnld_install_sound`; the
`tanos` table, which is the active table of the a01/c1/e2 bundles, also uses that spelling.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "dnld_install_sound", "params": {"sid": 1, "url": "https://example.invalid/file.pkg", "md5": "0123456789abcdef0123456789abcdef", "sver": 1}}
```

**Legacy documentation**

⚪ Legacy [install_sound.md](../../install_sound.md).

**Related:** [`get_sound_progress`](sound.md#get_sound_progress), [`get_current_sound`](sound.md#get_current_sound)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setSoundPackage`); call sites m14138; table key `SetSoundPackage` · anchor `"SetSoundPackage"`
- `a65@1.0.95` · wrapper m10115 (`setSoundPackage`); call sites m14108; table key `SetSoundPackage` · anchor `"SetSoundPackage"`
- `t4@1.0.32` · wrapper m10010 (`setSoundPackage`); call sites m11426; table key `SetSoundPackage` · anchor `"SetSoundPackage"`

</details>

<a id="get_sound_progress"></a>
### `get_sound_progress` — Installation progress

Polled every second during an installation.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of all 42 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`[]`).

**Response**

`result[0]` = `{"progress": 0–100, "state": <int>, "error": <int>, "sid_in_progress": <pack id>}`.
The app treats `state == 4` as failure (`error` 13 or 2 → "download failed", otherwise "install failed"),
`progress == 100` or `state == 3` or `sid_in_progress <= 0` as the end of the task (✅ Bundle · a65 m14108).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "get_sound_progress", "params": []}
```

**Related:** [`dnld_install_sound`](sound.md#dnld_install_sound)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`getSoundPackageProgress`); call sites m14138; table key `GetSoundPackageProgress` · anchor `"GetSoundPackageProgress"`
- `a65@1.0.95` · wrapper m10115 (`getSoundPackageProgress`); call sites m14108; table key `GetSoundPackageProgress` · anchor `"GetSoundPackageProgress"`
- `t4@1.0.32` · wrapper m10010 (`getSoundPackageProgress`); call sites m11426; table key `GetSoundPackageProgress` · anchor `"GetSoundPackageProgress"`

</details>

<a id="play_audio"></a>
### `play_audio` — Play a recorded message

Sends an audio clip to be played by the robot.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 32: a08 a09 a10 a14 a15 a19 a23 a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 s4 s5e s6 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"security": {"cipher_suite": 1}, "audio": <prepared encrypted data>}` (a65 m14657). The encryption steps use the key from [`get_random_pkey`](maps.md#get_random_pkey) and are not described here.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Related:** [`get_random_pkey`](maps.md#get_random_pkey)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`playAudio`); call sites m14711, m14714 · anchor `"play_audio"`
- `a65@1.0.95` · wrapper m10115 (`playAudio`); call sites m14657, m14660 · anchor `"play_audio"`
- `a08@1.0.47` · wrapper m10013 (`playAudio`); call sites m12671, m12674 · anchor `"play_audio"`

</details>

<a id="set_voice_chat_volume"></a>
### `set_voice_chat_volume` — Voice-chat volume

Sets the volume used during a call.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 21: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"volume": <int>}` (default 50 when nothing is stored).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "set_voice_chat_volume", "params": {"volume": 50}}
```

**Related:** [`start_voice_chat`](sound.md#start_voice_chat)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`setVoiceChatVolume`); call sites m14639, m14669 · anchor `"set_voice_chat_volume"`
- `a65@1.0.95` · wrapper m10115 (`setVoiceChatVolume`); call sites m14585, m14615 · anchor `"set_voice_chat_volume"`
- `a34@1.0.70` · wrapper m10109 (`setVoiceChatVolume`); call sites m14114, m14144 · anchor `"set_voice_chat_volume"`

</details>

<a id="start_voice_chat"></a>
### `start_voice_chat` — Start a voice call

Opens the robot audio channel for a call.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"play": true, "record": <bool>}`; `record` is false while the robot moves when remote control during calls is supported (`isSupportRemoteControlInCall`, high bit 19).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "start_voice_chat", "params": {"play": true, "record": true}}
```

**Behaviour in the app**

While a call is active the robot state is 28 ("In call…").

**Related:** [`stop_voice_chat`](sound.md#stop_voice_chat), [`start_camera_preview`](camera.md#start_camera_preview)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`startVoiceChat`); call sites m14639 · anchor `"start_voice_chat"`
- `a65@1.0.95` · wrapper m10115 (`startVoiceChat`); call sites m14585 · anchor `"start_voice_chat"`
- `a62@1.0.69` · wrapper m10109 (`startVoiceChat`); call sites m14051 · anchor `"start_voice_chat"`

</details>

<a id="stop_voice_chat"></a>
### `stop_voice_chat` — End a voice call

Closes the audio channel.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: none (`{}`).

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "stop_voice_chat", "params": {}}
```

**Related:** [`start_voice_chat`](sound.md#start_voice_chat)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`stopVoiceChat`); call sites m14639 · anchor `"stop_voice_chat"`
- `a65@1.0.95` · wrapper m10115 (`stopVoiceChat`); call sites m14585 · anchor `"stop_voice_chat"`
- `a62@1.0.69` · wrapper m10109 (`stopVoiceChat`); call sites m14051 · anchor `"stop_voice_chat"`

</details>

<a id="enable_homesec_voice"></a>
### `enable_homesec_voice` — Robot microphone switch

Turns the robot microphone on or off for the monitoring feature.

| | |
|---|---|
| Evidence | ✅ Bundle — called by the plugin of 22: a26 a27 a29 a30 a34 a37 a38 a40 a46 a51 a52 a62 a64 a65 a66 a69 a70 a72 a73 a74 a75 a76 model(s) |
| Transport | miIO RPC through the plugin call wrapper (`asyncCallMethod` / `RRMISDK.callMethod`) |

**Request**

`params`: `{"enable": <bool>}`.

**Response**

The app reads no reply field at the call sites checked (it ignores the reply, or reads it in another function). Reply shape: ❓ Unknown ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#response)).

**Example** — constructed from app code (typed sample values)

```json
{"id": 1, "method": "enable_homesec_voice", "params": {"enable": true}}
```

**Related:** [`start_voice_chat`](sound.md#start_voice_chat)

<details><summary>Sources</summary>

- `a74@1.0.96` · wrapper m10115 (`enableHomeSecVoice`); call sites m14639 · anchor `"enable_homesec_voice"`
- `a65@1.0.95` · wrapper m10115 (`enableHomeSecVoice`); call sites m14585 · anchor `"enable_homesec_voice"`
- `a62@1.0.69` · wrapper m10109 (`enableHomeSecVoice`); call sites m14051 · anchor `"enable_homesec_voice"`

</details>

## See also

- [Command index](index.md)
- [Evidence legend](../../README.md#evidence-legend)
