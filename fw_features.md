# Firmware Features


This page tried to collect the capabilities for various robot models based on the fw_features command.  
Please contribute the response from your robot. As the response may be related to the specific firmware, 1 model may have multiple lines.

The features of a device can be queried using the `get_fw_features` command.  
Expect a response like `{"result":[101,102,104,105],"id":9416}`

## Model - Features matrix


| Model                 | Name                  | Firmware      |101|102|103|104|105|106|107|108|109|110|111|112|113|114|115|116|117|118|119|120|121|122|123|124|125|126|127|128|129|130|Remark    
| --------------------- | --------------------- | ------------- | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | ------- |
| rockrobo.vacuum.v1    | Mi Robot Vacuum       | 3.5.8_004018  | X | X |   | X | X |   |   |   |   |   | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |         |
| roborock.vacuum.a01   | Roborock E Series     |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.a08   | Roborock S6 Pure      |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.a09   | Roborock T7 Pro       |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.a10   | Roborock S6 MaxV      | 3.5.8_5850    |   |   |   |   |   |   |   |   |   |   | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |   |   |   |   |   |         |
| roborock.vacuum.a11   | Roborock T7           |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.a14   | Roborock T7S          |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.a15   | Roborock S7           | 4.1.2_1140    |   |   |   |   |   |   |   |   |   | X | X | X | X | X | X | X | X | X | X | X |   | X | X | X | X |   |   |   |   |   |         |
| roborock.vacuum.a19   | Roborock S4 Max       |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.a23   | Roborock T7S Plus     |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.a27   | Roborock S7 MaxV      | 4.3.5_5602    |   |   |   |   |   |   |   |   |   |   | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X |   |   |   |   |   |         |
| roborock.vacuum.a38   | Roborock Q7 Max+      | 4.3.5_0866    |   |   |   |   |   |   |   |   |   |   | X | X | X | X | X | X | X | X | X | X |   | X | X | X | X |   |   |   |   |   |         |
| roborock.vacuum.c1    | Xiaowa C1             |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.e2    | Roborock Xiaowa E Series Vacuum v2 |  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.m1s   | Mi Robot Vacuum 1S    | ?             |   |   |   |   | X |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.p5    | Roborock P5           |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.s4    | Roborock S4           |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.s5    | Roborock S5           | 3.5.8_002034  |   | X | X | X | X |   |   |   |   |   | X | X | X | X | X | X | X | X | X |   |   | X | X |   | X |   |   |   |   |   |         |
| roborock.vacuum.s5e   | Roborock S5 Max       |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.s6    | Roborock S6           |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.t4    | Roborock T4           |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.t6    | Roborock T6           |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| roborock.vacuum.t7    | Roborock Vacuum T7    |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |
| rockrobo.vacuum.s6    | Roborock Vacuum S6    |               |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |         |


## List of features functionality

| Feature | Functionality                                                                     |
| ------- | --------------------------------------------------------------------------------- |
| 101     |                                                                                   |
| 102     |                                                                                   |
| 103     | Clean Time Supported                                                                                  |
| 104     |                                                                                   |
| 105     |                                                                                   |
| 106     |                                                                                   |
| 107     |                                                                                   |
| 108     |                                                                                   |
| 109     |                                                                                   |
| 110     |                                                                                   |
| 111     | Supports FSEndPoint                                                               |
| 112     | Supports AutoSplitSegments                                                        |
| 113     | Supportrs Delete Map feature                                                      |
| 114     | Supports OrderSegmentClean                                                        |
| 115     | Spot Clean                                                                        |
| 116     | Map Segment Supported                                                             |
| 117     |                                                                                   |
| 118     |                                                                                   |
| 119     | Supports Led Status Switch                                                        |
| 120     | Multi Floor Supported                                                             |
| 121     |                                                                                   |
| 122     | Supports FetchTimer Summary                                                       |
| 123     | Orders Clean Supported                                                            |
| 124     | Analysis Supported                                                                |
| 125     | Remote Supported                                                                  |
| 126     |                                                                                   |
| 127     |                                                                                   |
| 128     |                                                                                   |
| 129     |                                                                                   |


## Command description
Retrieves a list of supported firmware features of the device.

## Get Firmware Features

### Command

| Key    | Value               | Comment                                                                             |
| ------ | ------------------- | ----------------------------------------------------------------------------------- |
| method | `"get_fw_features"` |                                                                                     |
| id     | `id`                | Random integer which is returned in the response used to link request and response. |

#### Example

```json
{
    "method": "get_fw_features",
    "id": 7177
}
```

### Response

| Key | Example | Description                                |
| --- | ------- | ------------------------------------------ |
| `-` | _111_   | Feature (see [list](#feature-codes) below) |

#### Example

```json
{
    "result": [111, 112, 113, 114, 115, 116, 117, 118, 119, 122, 125],
    "id": 7177
}
```
