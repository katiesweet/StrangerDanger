#!/usr/bin/python
import threading

class LocalProcessInfo:
    processId = 0
    threadLock = threading.Lock()

    @staticmethod
    def setProcessId(processId):
        with LocalProcessInfo.threadLock:
            LocalProcessInfo.processId = processId

    @staticmethod
    def getProcessId():
        with LocalProcessInfo.threadLock:
            return LocalProcessInfo.processId
