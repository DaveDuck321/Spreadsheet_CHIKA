#!/usr/bin/env python

from PIL import Image
import glob
import sys, os

def resizeFrame(WIDTH, HIEGHT, INPUT_FILE_GENERIC, OUTPUT_FILE_GENERIC, frameNumber):
    img = Image.open(INPUT_FILE_GENERIC.format(frameNumber))
    resizedImg = img.resize((WIDTH, HIEGHT), Image.NEAREST)
    resizedImg.save(OUTPUT_FILE_GENERIC.format(frameNumber))

def resizeSequence(WIDTH, HIEGHT, INPUT_PATH, FILE_NAME, OUTPUT_PATH):
    GENERIC_INPUT = INPUT_PATH+"/{}{}.png".format(FILE_NAME, "{}")
    FRAME_COUNT = len(glob.glob1(INPUT_PATH, FILE_NAME+"*.png"))
    for i in range(0, FRAME_COUNT):
        print("Resizing image "+str(i))
        resizeFrame(WIDTH, HIEGHT, GENERIC_INPUT, OUTPUT_PATH+"/frame{}.png", i)


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Directory needs to contain files with names: NAME<0,1,2,...>.png")
        print("Usage: ImageSeqResizer.py <input file NAME> <input path> <output dir> <WIDTH> <HEIGHT>")
        exit()
    
    os.makedirs(sys.argv[3], exist_ok=True)
    resizeSequence( int(sys.argv[4]), int(sys.argv[5]),  sys.argv[2], sys.argv[1], sys.argv[3])
    print("Done")