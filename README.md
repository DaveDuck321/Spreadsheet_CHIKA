# Spreadsheet CHIKA!
## Overview
Draw images or play image sequences in excel by changing cell colors

![alt text](https://github.com/DaveDuck321/Spreadsheet_CHIKA/blob/master/Screenshots/screenshot1.png "Chika Dancing in Excel")
## Requirements
- Python 3.3+
- Pillow
- Excel (tested on 2016 and 365)

## Usage

An image sequence should be made up of a directory of `.png` images with the file name `NAME#.png` where `NAME` can be specified and `#` should increment from 0 to n.

Resize the image sequence using `ImageSeqResizer.py`:

```
./ImageSeqResizer.py FILE_NAME DIRECTORY_PATH OUTPUT_PATH NEW_WIDTH NEW_HEIGHT
```

Convert the image sequence to a `.csv` file using `ImageSeq2CSV.py`:
```
./ImageSeq2CSV.py FILE_NAME DIRECTORY_PATH OUTPUT_FILE.CSV
```

This `.csv` file can be opened with excel. Copy the data from this file into `animation.xlsm` overwriting the data in the `CodeOutput` sheet and enabling macros. Alternatively, without using `animation.xlsm` a new excel file can be generated using the code in `VBACode.vba` as a macro, this should have two sheets: `Canvas` and `CodeOutput`.

Run the macro `FillVideo` to view the animation.

Single images can also be displayed using `Image2CSV.py` to generate the `.csv` file and the `FillImage` macro to display them:
```
./Image2CSV.py INPUT.PNG OUTPUT.CSV
```
