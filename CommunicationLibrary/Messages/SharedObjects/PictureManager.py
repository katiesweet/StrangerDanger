#!/usr/bin/python
import math
import numpy as np

class PictureManager:

    @staticmethod
    def splitPicture(picture, splitSize):
        rows = picture.shape[0]
        numberOfParts = math.ceil(rows/splitSize)
        splitFrames = np.array_split(picture, numberOfParts)
        return splitFrames, numberOfParts

    @staticmethod
    def combinePicture(splitFrames):
        return np.concatenate(splitFrames)
