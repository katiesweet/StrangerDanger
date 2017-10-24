#!/usr/bin
from abc import ABCMeta, abstractmethod
from AbstractMessages.Message import Message

class Reply(Message):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, success, messageId, conversationId):
        super(Reply, self).__init__(messageId, conversationId)
        self.success = success
