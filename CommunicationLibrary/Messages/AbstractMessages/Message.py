#!/usr/bin
from abc import ABCMeta, abstractmethod

class Message:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, messageId, conversationId):
        self.messageId = messageId
        self.conversationId = conversationId
