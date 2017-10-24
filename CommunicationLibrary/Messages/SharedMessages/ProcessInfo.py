#!/usr/bin
import numpy as np

class ProcessInfo:

    def __init__(self, processId, processType, endPoint, label, status, aliveTimeStamp):
        self.processId = processId
        self.processType = processType
        self.endPoint = endPoint
        self.label = label
        self.status = status
        self.aliveTimeStamp = aliveTimeStamp
