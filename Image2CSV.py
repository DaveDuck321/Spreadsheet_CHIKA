#!/usr/bin/env python

from PIL import Image
import sys

EXCEL_MAX_COLUMNS = 2**14

def PixelsEqual(t1, t2):
    return abs(t1[0]-t2[0])<10 and abs(t1[1]-t2[1])<10 and abs(t1[2]-t2[2])<10

def GetColorValue(rgbColor):
    return rgbColor[0] + rgbColor[1]*256 + rgbColor[2]*256*256

def GetImageSize(path):
    img = Image.open(path)
    return img.size

def GetColumnFromNumber(number):
    columnName = ""
    while number>=0:
        columnName+=chr(ord('A')+number%26)
        number = number//26-1
    return columnName[::-1]

#OUTPUT file format:
#meta:          width, height, FRAME_0_RANGE, OTHER_FRAME_RANGE
#frame1 image:  color, color,....
def Image2CSVString(PATH, frameLengthMeta):
    img = Image.open(PATH)
    width, height = img.size

    pxData = img.load()

    csvString = "{}, {}, A2:{}{}, A{}:XFD{}\n"
    pixelCount = 0
    rows = 1

    for y in range(0, height):
        for x in range(0, width):
            pixelCount+=1
            if pixelCount>EXCEL_MAX_COLUMNS:
                pixelCount = 1
                rows+=1
                csvString+="\n"
            csvString+="{},".format(GetColorValue(pxData[x,y]))
    if rows!=1:
        pixelCount = EXCEL_MAX_COLUMNS-1
    return csvString.format(width, height, GetColumnFromNumber(pixelCount), 1+rows, 2+rows, 1+rows+frameLengthMeta)

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Usage: Image2CSV.py <input.png> <output.csv>")
        exit()
    imageString = Image2CSVString(sys.argv[1], 1)
    file = open(sys.argv[2], 'w+')
    file.write(imageString)
    file.close()
    print("Done")