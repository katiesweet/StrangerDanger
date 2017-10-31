#!/usr/bin
from abc import ABCMeta, abstractmethod
from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem


class Message:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        self.messageId = CommunicationSubsystem.getMessageId()
        self.conversationId = CommunicationSubsystem.getConversationId()

    @abstractmethod
    def encode():
        pass

    @abstractmethod
    def decode():
        pass
