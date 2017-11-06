#!/usr/bin/python
from abc import ABCMeta, abstractmethod
import cPickle as pickle
import copy
from CommunicationLibrary.Messages.SharedObjects.MessageId import MessageId

class Message:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.messageId = None
        self.conversationId = None

    # def setMessageIdConversationId(self):
    #     self.setMessageIdConversationId(MessageId.create())
    #
    def setMessageId(self, messageId=MessageId.create()):
        self.setMessageIdConversationId(messageId, copy.deepcopy(messageId))

    def setMessageIdConversationId(self, messageId, conversationId):
        self.messageId = messageId
        self.conversationId = conversationId

    def encode(self):
        return pickle.dumps(self)

    @staticmethod
    def decode(encodedMsg):
        return pickle.loads(encodedMsg)
