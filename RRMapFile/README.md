RR Map file format and proof of concept file reader

File format description here [RRFileFormat.md](RRFileFormat.md)

[roborock_map_file.ksy](roborock_map_file.ksy) contains a [Kaitai](https://kaitai.io) struct for the map format,
which can be used to autogenerate parsing code in the programming language of your choice or evaluate a file using [the web IDE](https://ide.kaitai.io/)

Offline viewer  [roboMapViewer2.5.7.zip](roboMapViewer2.5.7.zip) To run the viewer `java -jar RoboMapviewer2.5.7.jar` (assuming java is in your path, and the viewer is in the current dir, otherwise add the paths appropriately)
Robo

[roboMapViewer2.5.9-1.zip](roboMapViewer2.5.9-1.zip) updated version that also decodes the identified obstacles

Source of offline viewer (included in openHAB miio binding): https://github.com/openhab/openhab-addons/blob/2.5.x/bundles/org.openhab.binding.miio/src/test/java/org/openhab/binding/miio/internal/RoboMapViewer.java 

![example picture](DecodedSample.png "Decoded with concept reader with goto")
![example picture](decodedRegion.png "Decoded with concept reader with regions")

Decoded with concept reader for map v1.1

![example picture](rrmap-v11.jpg "Decoded with concept reader for map v1.1")
