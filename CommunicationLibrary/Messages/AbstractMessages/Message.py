#!/usr/bin/python
from abc import ABCMeta, abstractmethod
#from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
import cPickle as pickle


class Message:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def initConversationIdMessageId(self, conversationId, messageId):
        self.conversationId = conversationId
        self.messageId = messageId

    def encode(self):
        return pickle.dumps(self)

    @staticmethod
    def decode(encodedMsg):
        return pickle.loads(encodedMsg)
