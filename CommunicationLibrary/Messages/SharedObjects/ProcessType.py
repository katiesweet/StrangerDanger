#!/usr/bin/python
from enum import Enum

class ProcessType(Enum):
    Registry = 1
    MainServer = 2
    StatisticsServer = 3
    ClientProcess = 4
    CameraProcess = 5
