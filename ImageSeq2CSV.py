#!/usr/bin/env python

from PIL import Image
import glob
import sys

from Image2CSV import *

EXCEL_MAX_COLUMNS = 2**14

#[(x, y, (r, g, b), frame)]
#returns True if any diffs were found
def GetImageDiffs(frameNumber, diffs, lastImageData, PATH, FRAME_WIDTH, FRAME_HEIGHT):
    img = Image.open(PATH.format(frameNumber))
    pxData = img.load()
    diffsFound = False
    for x in range(0, FRAME_WIDTH):
        for y in range(0, FRAME_HEIGHT):
            if not PixelsEqual(lastImageData[x][y], pxData[x,y]):
                lastImageData[x][y] = (pxData[x,y][0], pxData[x,y][1], pxData[x,y][2])
                diffs.append( (x,y, lastImageData[x][y], frameNumber ) )
                diffsFound = True
    return diffsFound
    

def CopyFrameToImageData(frameNumber, lastImageData, PATH, FRAME_WIDTH, FRAME_HEIGHT):
    img = Image.open(PATH.format(frameNumber))
    pxData = img.load()
    for x in range(0, FRAME_WIDTH):
        for y in range(0, FRAME_HEIGHT):
            lastImageData[x][y] = (pxData[x,y][0], pxData[x,y][1], pxData[x,y][2])

#returns the number of frames with diffs
def GenerateAllFrameDiffs(FRAME_COUNT, PATH, FRAME_WIDTH, FRAME_HEIGHT, diffs):
    #generate blank image
    lastImageData = []
    for x in range(0, FRAME_WIDTH):
        lastImageData.append([])
        for y in range(0, FRAME_HEIGHT):
            lastImageData[x].append((0,0,0))
    #fill image with initial image colors
    CopyFrameToImageData(0, lastImageData, PATH, FRAME_WIDTH, FRAME_HEIGHT)
    #populate diffs
    framesWithDiffs = 0
    for frame in range(1, FRAME_COUNT):
        if frame % 100 == 0:
            print("Generating diffs: frame {}/{}".format(frame, FRAME_COUNT))
        framesWithDiffs+=GetImageDiffs(frame, diffs, lastImageData, PATH, FRAME_WIDTH, FRAME_HEIGHT)

    return framesWithDiffs

#OUTPUT file format:
#meta:          width, height, FRAME_0_RANGE, OTHER_FRAME_RANGE
#frame1 image:  color, color,....
#frameN diff:   coord, color, coord, color,....
def ImageSeq2CSVFile(PATH, FILE_NAME, OUTPUT):
    FRAME_COUNT = len(glob.glob1(PATH, FILE_NAME+"*.png"))
    if FRAME_COUNT==0:
        print("No frames found")
        return
    GENERAL_PATH = PATH+"/"+FILE_NAME+"{}.png"
    WIDTH, HEIGHT = GetImageSize(GENERAL_PATH.format(0))
    diffs = []
    framesWithDiffs = GenerateAllFrameDiffs(FRAME_COUNT, GENERAL_PATH, WIDTH, HEIGHT, diffs)

    pixelsinFrame = 0
    frameNumber = 0
    framesFinishedCount = 0
    csvCode = ""
    metaWFrame1 = Image2CSVString(GENERAL_PATH.format(0), framesWithDiffs)

    print("Saving diffs to file")
    file = open(OUTPUT, 'w+')
    file.write(metaWFrame1)

    for i in range(1, len(diffs)):
        if diffs[i][3] != frameNumber:
            frameNumber = diffs[i][3]
            if pixelsinFrame > EXCEL_MAX_COLUMNS/2:
                print("Warning, frame {} has too much data.".format(i))
                print("Information will be lost")
            csvCode+='\n'
            pixelsinFrame = 0
            framesFinishedCount+=1
            #writes 10 frames at a time to file
            if framesFinishedCount%10==0:
                file.write(csvCode)
                csvCode=""
        pixelsinFrame+=1
        csvCode +="{},{},".format(diffs[i][1]*WIDTH+diffs[i][0], GetColorValue(diffs[i][2]))

    file.write(csvCode)
    file.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Directory needs to contain files with names: NAME<0,1,2,...>.png")
        print("Usage: ImageSeq2CSV.py <file NAME> <directory> <output.csv>")
        exit()
    ImageSeq2CSVFile(sys.argv[2], sys.argv[1], sys.argv[3])
    print("Done, success")