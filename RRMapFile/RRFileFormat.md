RR Files send to the device and found in the robot.db file

These files consist of a header and several blocks.
The file is gzipped, hence needs to be unzipped before reading.


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
| Digest    			 | 1024 |                                |

### File Header
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | "RR"                                                    |
| 0x02			    |  2		 | Lenght of the header                                    |
| 0x04          |  4     | Data length (points to location of the footer           |
| 0x08		      |  2		 | Major Version                                           |
| 0x0A			    |  2  	 | Minor Version                                           |
| 0x0C          |  4     | Map Index                                               |
| 0x10          |  4    | Map Sequence                                             | 
| 0x14          |  ..    | Start first datablock                                   |



```

Data block type 1 (Charger)
Position(hex)   Length  Information
===================================================
0x00      2       block type ( 01 00)
0x02			2		    Lenght of the header
0x04      4       Length of datablock 08 00 ( 8 bytes of header not counted)
0x08			4		Charger X pos
0x0C			4		Charger Y pos


Data block type 2 (Image)
Position(hex)   Length  Information
===================================================
0x00      2       block type
0x02			2		    Lenght of the header
0x04      4       Length of datablock ( 8 bytes of header not counted) = image size
0x08			4		Top Pos
0x0C			4		Left Pos
0x10            4       Image height
0x14            4       Image width
0x18             ..       grayscale image data (each pixel 1 byte) 
```

Data block type 3 (vacuum path)
| Position(hex) | Length | Information                                             |
| ------------- | ------ | --------------------------------------------------------|
| 0x00          |  2     | block type                                              |
| 0x02			    |  2		 | Lenght of the header                                    |
| 0x04          |  4     | Length of datablock ( 8 bytes of header not counted)    |
| 0x08		      |  4		 | setPointLength (amount of position pairs)               |
| 0x0C			    |  4  	 | setPointSize                                            |
| 0x10          |  4     | setAngle                                                |
| 0x14          |  ..    | Pairs of 2 Byte UInt16LE x/y coordinates in mm          |


```
Data block type 4 (digest)
Position(hex)   Length  Information
===================================================
0x00            2       block type
0x02		      	4		CRC32 code?

Data block type 8 (Robot Position)
Position(hex)   Length  Information
===================================================
0x00            2       block type
0x02			      2		    Lenght of the header
0x04            4       Length of datablock ( 8 bytes of header not counted) 
0x08            4       x UInt32LE
0x0c            4       y UInt32LE



```


