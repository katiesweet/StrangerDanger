#!/usr/bin/python
import math
# import numpy as np

class PictureManager:

    @staticmethod
    def splitPicture(picture, sizeOfParts):
        # rows = picture.shape[0]
        # numberOfParts = int(math.ceil(rows/sizeOfParts))
        # splitFrames = np.array_split(picture, numberOfParts)
        return [1,2], 2
        # return splitFrames, numberOfParts

    @staticmethod
    def combinePicture(splitFrames):
        # return np.concatenate(splitFrames)
        return 'hi'
