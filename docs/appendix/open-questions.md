# Open questions

[Home](../../README.md) / Appendix / Open questions

Things the plugin bundles do not settle, with what was checked. Contributions with captures from real robots (model, firmware, exact request and reply) are the most useful way to close them.

## Protocol

- **Which firmware answers which method.** A call site proves only that the app can send it. No bundle contains robot replies other than unit-test fixtures.
- **Direct `get_status`.** The app polls `get_prop ["get_status"]`; whether firmware also answers `get_status` as a method is not shown ([`get_status`](../commands/status.md#get_status)).
- **MIoT tunnel.** The bundles use MIoT action 7/1 only for a14, a15 and a19; whether other models implement it is unknown ([transports](../concepts/transports.md#miot-tunnel-mispec)).
- **Retry protocol on firmware without the feature bit.** Not shown ([transports](../concepts/transports.md#retry-protocol)).
- **Local vs cloud routing.** Decided by the Mi Home host SDK; not visible in the bundles.
- **Error numbers `-97` and `-12`.** The app ignores them in some map flows without naming them ([JSON-RPC envelope](../concepts/json-rpc-envelope.md#errors)).
- **Generic `miIO.*` methods.** Only legacy documentation ([miIO protocol](../concepts/miio-protocol.md#generic-methods)).

## Features and gates

- **Relation of `new_feature_info` and `new_feature_info_str`.** Whether the string repeats the number is unknown; the bundles give the same bit numbers different meanings in the two words ([feature flags](../concepts/feature-flags.md#feature-word-new_feature_info_str)).
- **Which codes and bits a given robot sets.** Only the user-contributed captures in [feature flags](../concepts/feature-flags.md#legacy-captures) exist.
- **Feature codes without a literal test** (101, 102, 104-110, 115, 117, 121, 126-129): meaning unknown; legacy captures report some of them (for example 117 and 121 on several robots, [feature flags](../concepts/feature-flags.md#legacy-captures)).
- **Predicates classified `N`.** They are false in the sandbox; some may depend on inputs the sandbox lacks. They are not interpreted.
- **Account allow lists.** Some predicates test the Mi Home account id against lists inside the plugin; the lists are deliberately not recorded.

## Enumerations and fields

- **`dss` values.** The 2-bit values of each supply group are not named in the code ([dock](../reference/dock.md#dock-supply-status-dss)).
- **Dock types 4 and above 8**, and marketing names of dock classes O0-O4 / Pearl.
- **Clean-record `wash_time` unit and `map_flag` values** ([clean record](../reference/clean-record.md)).
- **Status fields only in the old documentation** (`msg_seq`, `clean_mode`, ...) ([status fields](../reference/status-fields.md#legacy-only-fields)).
- **Water-box distance (`distance_off`) unit** ([units](../reference/units.md)).

## Maps

- **Which block ids a firmware writes.** The bundles show only what the app can decode ([map file format](../../RRMapFile/RRFileFormat.md#parser-generations)).
- **Maximum number of walls and zones** the editor allows (limits not extracted).
- **Meaning of forbidden-zone type 3** (`FBZ_TYPE_CLEANING`) beyond the plugin's own name ([maps overview](../concepts/maps-overview.md#virtual-walls-and-forbidden-zones)).
- **Blocks 28-34** (door sills, stuck points, cliff zones, floor direction, date, nonce): layouts are taken from the parser; the function of some is only inferable from the editing calls.
- **`.ksy` file.** Covers block types up to 19; it was left unchanged.

## Bundles and sources

- **Meaning of the second and third number in the cloud file name** ([methodology](../methodology.md#how-the-bundles-were-obtained)).
- **Minified bundles.** a26, a27, a29, a30, a46, a51, a66, a69, a70, a76 are minified; identifier-level checks that depend on names (for example the dock helper functions) were only run on the readable ones where stated.
- **Native v1 plugins** (17 files) were not analysed.
- **openHAB comparison.** Status types and model names were compared; error tables, fan modes and capability flags of the binding were not compared item by item.
- **Models without a bundle** are listed in [unverified models](unverified-models.md).

## See also

- [Corrections](corrections.md)
- [Methodology](../methodology.md)
