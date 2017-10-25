#!/usr/bin
from abc import ABCMeta, abstractmethod
from Message import Message

class Request(Message):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, messageId, conversationId):
        super(Request, self).__init__(messageId, conversationId)
