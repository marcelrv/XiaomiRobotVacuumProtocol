RR Files send to the device and found in the robot.db file

These files consist of a header and several blocks.
The file is gzipped, hence needs to be unzipped before reading.

Coordinates to be divided by 50 to match map pixels

| Datablock        |  Id  | Remark                         |
| -----------------| ---- | ------------------------------ |
| Charger location | 	1   |                                | 
| Image 				   |  2   |                                |
| Vacuum Path			 |  3   |                                |
| Go-To Path       |  4   | Only exist with newer firmware | 
| Predicted Path   |  5   | Only exist with newer firmware | 
| Cleaned Zones    |  6   | Only exist with newer firmware | 
| Goto Target      |  7   | Only exist with newer firmware | 
| Robot Position   |  8   |                                | 
| No go areas      |  9   | Only exist with newer firmware | 
| Virtual Walls    | 10   | Only exist with newer firmware | 
| Unknown          | 11   | Only exist with latest S5 firmware 3.5.7 | 
| Digest    			 | 1024 |                                |

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
| 0x08          |  4     | S5 has extra block here... all other blocks re shifted in that case |
| 0x08		      |  4		 | Top Pos                                                 |
| 0x0C			    |  4  	 | Left Pos                                                |
| 0x10		      |  4		 | Image height                                            |
| 0x14			    |  4  	 | Image width                                             |
| 0x1C		      |  4		 | Image Data      00=outside, 01=wall FF=inside area      |
note model S5 firmware 3.5.7  has lenght of 0x1C, img height & width are mo
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

Data block type  11 (??)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08		      |  2		 | # of datapoints                                         |


Data block type  0x0400 (1024) (digest)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | Block type                                              |
| 0x02			    |  2		 | Length of the block header                              |
| 0x04          |  4     | Length of block data  (header not included)             |
| 0x08          |  12    | SHA1 hash of file until this block                      |

