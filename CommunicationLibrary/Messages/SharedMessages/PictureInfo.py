#!/usr/bin
import numpy as np

class PictureInfo:

    def __init__(self, picture, timeStamp, cameraId, clusterId):
        self.picture = picture
        self.timeStamp = timeStamp
        self.cameraId = cameraId
        self.clusterId = clusterId
