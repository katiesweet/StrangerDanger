#!/usr/bin/python
import math
import numpy as np

class PictureManager:

    @staticmethod
    def splitPicture(picture, sizeOfParts):
        rows = picture.shape[0]
        numberOfParts = math.ceil(rows/sizeOfParts)
        splitFrames = np.array_split(picture, numberOfParts)
        return splitFrames, numberOfParts

    @staticmethod
    def combinePicture(splitFrames):
        return np.concatenate(splitFrames)
