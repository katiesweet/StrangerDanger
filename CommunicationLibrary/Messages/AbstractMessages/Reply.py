#!/usr/bin
from abc import ABCMeta, abstractmethod
from Message import Message

class Reply(Message):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, messageId, conversationId, success):
        super(Reply, self).__init__(messageId, conversationId)
        self.success = success
