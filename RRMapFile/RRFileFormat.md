RR Files send to the device and found in the robot.db file

These files consist of a header, grayscale image and robot movement data.
The file is gzipped, hence needs to be unzipped before reading


```
Position(hex)   Length   Information
===================================================
0x00             2        header magic (RR)
0x04             4        Data length (points to location of the footer (checksum data?)
0x28             1        Image size
0x34             4        Image height
0x38             4        Image width
0x3A             ..       grayscale image data (each pixel 1 byte) 
???              ..        robot movement data


```


