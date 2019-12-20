RR Files send to the device and found in the robot.db file

These files consist of a header, grayscale image and robot movement data.
The file is gzipped, hence needs to be unzipped before reading


```
0x02			2		header length
0x04      4       Data length (points to location of the footer (checksum data?)
0x08			2		Major Version
0x0A			2		Minor Version
0x0C			4		Map Index
0x10			4		Map Sequence

0x14			Start First datablock


Datablock type
Charger location  	1
Image 				      2
Vacuum path			    3
Digest				     1024


Data block type 1 (Charger)
Position(hex)   Length  Information
===================================================
0x00      2       block type ( 01 00)
0x02			2		unknown
0x04      4       Length of datablock 08 00 ( 8 bytes of header not counted)
0x08			4		Charger X pos
0x0C			4		Charger Y pos


Data block type 2 (Image)
Position(hex)   Length  Information
===================================================
0x00      2       block type
0x02			2		unknown
0x04      4       Length of datablock ( 8 bytes of header not counted) = image size
0x08			4		Top Pos
0x0C			4		Left Pos
0x10            4       Image height
0x14            4       Image width
0x18             ..       grayscale image data (each pixel 1 byte) 

Data block type 3 (vacuum path)
Position(hex)   Length  Information
===================================================
0x00            2       block type
0x02			      2		unknown
0x04            4       Length of datablock ( 8 bytes of header not counted) 
0x08		      	4		setPointLength
0x0C			      4		setPointSize
0x10            4       setAngle
0x14             ..     Pairs of 2 Byte UInt16LE x/y coordinates in mm

Data block type 4 (digest)
Position(hex)   Length  Information
===================================================
0x00            2       block type
0x02		      	4		CRC32 code?

Data block type 8 (Robot Position)
Position(hex)   Length  Information
===================================================
0x00            2       block type
0x02			      2		unknown
0x04            4       Length of datablock ( 8 bytes of header not counted) 
0x08            4   x UInt32LE
0x0c            4   y UInt32LE



```


