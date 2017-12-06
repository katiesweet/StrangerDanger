#!/usr/bin/python
import math
import numpy as np

class PictureManager:

    @staticmethod
    def splitPicture(picture):
        rows,cols = picture.shape
        sizeOfParts = int(30000.0/(40*cols))
        numberOfParts = int(math.ceil(rows/sizeOfParts))
        splitFrames = np.array_split(picture, numberOfParts)
        return splitFrames, numberOfParts

    @staticmethod
    def combinePicture(splitFrames):
        return np.concatenate(splitFrames)
