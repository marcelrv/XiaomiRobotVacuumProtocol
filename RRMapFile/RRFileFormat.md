RR Files send to the device and found in the robot.db file

These files consist of a header and several blocks.
The file is gzipped, hence needs to be unzipped before reading.

Coordinates to be divided by 50 to match map pixels

| Datablock              |  Id  | Code Id       | Remark                              | 
| -----------------------| ---- | ------------- | ----------------------------------- | 
| Charger location       | 	1   | charger       |                                     | 
| Image 			      	   |  2   | map           |                                     | 
| Vacuum Path			       |  3   | path          |                                     | 
| Go-To Path             |  4   | pathGoto      | Only exist with newer firmware      | 
| Predicted Path         |  5   | pathGotoPlan  | Only exist with newer firmware      | 
| Cleaned Zones          |  6   | zones         | Only exist with newer firmware      | 
| Goto Target            |  7   | target        | Only exist with newer firmware      | 
| Robot Position         |  8   | robot         |                                     | 
| No go areas            |  9   | fbzs          | Only exist with newer firmware      | 
| Virtual Walls          | 10   | walls         | Only exist with newer firmware      | 
| Blocks                 | 11   | blocks        | Only exist with map v1.1            | 
| No mob zonem-fbzs      | 12   | mfbzs         | Only exist with map v1.1            | 
| Obstacles              | 13   | obstaclesOld  | Only exist with map v1.1            | 
| Ignored Obstacles      | 14   | ignoredObstaclesOld | Only exist with map v1.1      | 
| Obstacles III          | 15   | obstacles     | Only exist with map v1.1            | 
| Ignored Obstacles      | 16   | ignoredObstacles |  Only exist with map v1.1        | 
| Carpet Map             | 17   |  carpetMap    | Only exist with map v1.1            | 
| Mop Path               | 18   | mopPath       | Only exist with map v1.1            |
| Carpet Forbidden area  | 19   | cfbzs         | Only exist with map v1.1            |
| Smart zones path type  | 20   | pathType      | Reports itself as v1.0, but newer models (mid 2022) only |
| Smart Zones            | 21   | smartZones    | Reports itself as v1.0, but newer models (mid 2022) only |
| Custom Carpet          | 22   | customCarpet  | Reports itself as v1.0, but newer models (mid 2022) only |
| CL forbiden zones      | 23   | clfbzs        | Reports itself as v1.0, but newer models (mid 2022) only |
| Floor Map              | 24   | floorMap      | Reports itself as v1.0, but newer models (mid 2022) only |
| Furnitures             | 25   | furnitures    | Reports itself as v1.0, but newer models (mid 2022) only |
| Dock Type              | 26   | dockType      | Reports itself as v1.0, but newer models (mid 2022) only |
| Enemies                | 27   | enemies       | Reports itself as v1.0, but newer models (mid 2022) only |
| door zones ?           | 28   | dsfbz         | function uncertain. First seen with S8 Ultra    |
| stuck points           | 29   | stuckpts      | First seen with S8 Ultra                        |
| cliff zones            | 30   | clffbz        | First seen with S8 Ultra                        |
| Smart ds               | 31   | smartds       | Function unknown first seen with S8 Ultra       |
| flDirec      ??        | 32   | flDirec       | Function unknown first seen with S8 Ultra       |
| Date                   | 33   | date          | First seen with S8 Ultra                        |
| Nonce Data             | 34   | nonceData     | Function unknown first seen with S8 Ultra       |
| Digest    			       | 1024 | digest        |                                                 | 

NB, older models use map version 1.0
Newer models e.g 5 firmware 3.5.7 use maptype 1.1, this map has additional information (blocks 9,10,11,12)

### File Header
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | "RR"                                                    |
| 0x02			    |  2		 | Length of the header                                    |
| 0x04          |  4     | Data length (points to location of the footer           |
| 0x08		      |  2		 | Major Version                                           |
| 0x0A			    |  2  	 | Minor Version                                           |
| 0x0C          |  4     | Map Index                                               |
| 0x10          |  4     | Map Sequence                                            | 
| 0x14          |  ..    | Start first datablock                                   |

Data block type  1 (Charger)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  4		 | Charger X pos                                           |
| 0x0C			    |  4  	 | Charger Y pos                                           |

Data block type  2 (Image)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08          |  4     | map v1.1 has extra block here... all other blocks re shifted in that case  |
| 0x08		      |  4		 | Top Pos                                                 |
| 0x0C			    |  4  	 | Left Pos                                                |
| 0x10		      |  4		 | Image height                                            |
| 0x14			    |  4  	 | Image width                                             |
| 0x1C		      |  4		 | Image Data      00=outside, 01=wall FF=inside area      |
note map v1.1 model S5 firmware 3.5.7  has lenght of 0x1C, img height & width are mo
This version has many more values for the image data

bit   76543210
LSB 0 = outside 
bit 1 : 1=wall

Data block type 3 (vacuum path)
Data block type 4 (goto path)
Data block type 5 (predicted goto path)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  4		 | setPointLength (amount of position pairs)               |
| 0x0C			    |  4  	 | setPointSize                                            |
| 0x10          |  4     | setAngle                                                |
| 0x14          |  ..    | Pairs of 2 Byte UInt16LE x/y coordinates in mm          |

Data block type 6 (zones)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  2		 | # of zones   uInt32LE                                   |
| 0x0C          |  ..    | Pairs of 2 Byte UInt16LE x1/y1 x2/y2 coordinates in mm  |
X1 and Y2 are the left top point, X2 and Y2 are the right bottom point of the rectangle


Data block type  7 (Target Position)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  2		 | Robot X pos UInt16LE                                    |
| 0x0A			    |  2  	 | Robot Y pos UInt16LE                                    |


Data block type  8 (Robot Position)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  4		 | Robot X pos UInt32LE                                    |
| 0x0C			    |  4  	 | Robot Y pos UInt32LE                                    |
| 0x10			    |  4  	 | Robot angle UInt32LE  (Only newer models, maptype 1.1   |

Data block type  9  (nogo zones / fbzs)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  ..		 | blocks of 8x UInt16LE, coordinates of corners           |

Data block type  10  (walls)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  ..		 | blocks of 4x UInt16LE (coordines of corners)            |


Data block type  11 (blocks)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  ..		 | 1 byte blocks                                           |


Data block type  12  (mfbzs/No mob zones)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  ..		 | blocks of 8x UInt16LE                                   |

Data block type  13  (obstacles)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  ..		 | blocks of 2x UInt16LE + 1x byte  (Position X,Y, ?       |


Data block type  14  (obstacles)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  ..		 | blocks of 3x UInt16LE (Position X,Y, object Type)       |

Data block type  15  (obstacles)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  ..		 | blocks of 3x UInt16LE (Position X,Y, object Type)  + In case of photo objects confidence level (Uint32LE) and reference strning      |


Data block type  15  (obstacles)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  ..		 | blocks of 2x UInt16LE + 1x byte                         |


Data block type  0x0400 (1024) (digest)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08          |  12    | SHA1 hash of file until this block                      |

