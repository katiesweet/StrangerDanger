#!/usr/bin/python
from abc import ABCMeta, abstractmethod
import cPickle as pickle
import copy
from CommunicationLibrary.Messages.SharedObjects.MessageId import MessageId

class Message:
    __metaclass__ = ABCMeta

    #def __init__(self, messageId=MessageId.create()):
    def __init__(self):
        self.messageId = MessageId()
        self.conversationId = copy.deepcopy(self.messageId)

    def setConversationId(self, conversationId):
        self.conversationId = conversationId

    def setMessageIdConversationId(self, messageId, conversationId):
        self.messageId = messageId
        self.conversationId = conversationId

    def encode(self):
        return pickle.dumps(self)

    @staticmethod
    def decode(encodedMsg):
        return pickle.loads(encodedMsg)
