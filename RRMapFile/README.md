# RR map file: format description and proof-of-concept reader

[Home](../README.md) / [Maps](../docs/maps/index.md) / RRMapFile

This folder keeps the binary assets (sample maps, viewers, Kaitai description) at their original paths. The format description is [RRFileFormat.md](RRFileFormat.md) (verified against the app parser, see [methodology](../docs/methodology.md)).

- [roborock_map_file.ksy](roborock_map_file.ksy) is a [Kaitai](https://kaitai.io) struct for the map format that can be used to generate parsing code or to inspect a file in the [web IDE](https://ide.kaitai.io/). It covers block types up to 19 and 1024; types 20-34 and 36 are described in [RRFileFormat.md](RRFileFormat.md) only.
- Offline viewer [roboMapViewer2.5.7.zip](roboMapViewer2.5.7.zip): `java -jar RoboMapviewer2.5.7.jar` (java in the path, viewer in the current directory, otherwise add the paths).
- [roboMapViewer2.5.9-1.zip](roboMapViewer2.5.9-1.zip): updated version that also decodes the identified obstacles. The latest viewer is on the [openHAB forum](https://community.openhab.org/t/xiaomi-vacuum-map-viewer-to-find-coordinates-for-zone-cleaning/103500).
- Source of the offline viewer (included in the openHAB miio binding): <https://github.com/openhab/openhab-addons/blob/2.5.x/bundles/org.openhab.binding.miio/src/test/java/org/openhab/binding/miio/internal/RoboMapViewer.java>

![example picture](DecodedSample.png "Decoded with concept reader with goto")
![example picture](decodedRegion.png "Decoded with concept reader with regions")

Decoded with concept reader for map v1.1

![example picture](rrmap-v11.jpg "Decoded with concept reader for map v1.1")
![example picture](robomapobjects.png "Decoded map with objects")

## See also

- [Maps overview](../docs/concepts/maps-overview.md)
- [Map commands](../docs/commands/maps.md)
