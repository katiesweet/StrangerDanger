#!/usr/bin/python
from abc import ABCMeta, abstractmethod
import cPickle as pickle


class Message:
    __metaclass__ = ABCMeta

    processId = 0
    messageNum = 0

    def __init__(self):
        self.messageId = (Message.processId, Message.messageNum)
        Message.messageNum += 1
        pass

    def initConversationIdMessageId(self, conversationId, messageId):
        self.conversationId = conversationId
        self.messageId = messageId

    def encode(self):
        return pickle.dumps(self)

    @staticmethod
    def decode(encodedMsg):
        return pickle.loads(encodedMsg)
