#!/usr/bin/python
import sys
import threading
from LocalProcessInfo import LocalProcessInfo

class MessageId:
    nextSequenceNumber = 0
    threadLock = threading.Lock()

    def __init__(self):
        self.sequenceNumber = 0
        self.processId = 0

    @staticmethod
    def create():
        messageId = MessageId()
        messageId.processId = LocalProcessInfo.getProcessId()
        messageId.sequenceNumber = MessageId.getNextSequenceNumber()
        return messageId

    @staticmethod
    def getNextSequenceNumber():
        with MessageId.threadLock:
            if MessageId.nextSequenceNumber == sys.maxint:
                MessageId.nextSequenceNumber = 0
            MessageId.nextSequenceNumber += 1
        return MessageId.nextSequenceNumber

    def __str__(self):
        return '({},{})'.format(self.processId, self.sequenceNumber)

    def __eq__(self, other):
        if self.sequenceNumber == other.sequenceNumber and self.processId == other.processId:
            return True
        return False
