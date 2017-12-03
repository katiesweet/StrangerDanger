#!/usr/bin/python
import math
# import numpy as np

class PictureManager:

    @staticmethod
    def splitPicture(picture, sizeOfParts):
        # rows = picture.shape[0]
        # numberOfParts = math.ceil(rows/sizeOfParts)
        # splitFrames = np.array_split(picture, numberOfParts)
        # return splitFrames, numberOfParts
        return [1,2,3,4,5], 5

    @staticmethod
    def combinePicture(splitFrames):
        # return np.concatenate(splitFrames)
        return 'hi'
