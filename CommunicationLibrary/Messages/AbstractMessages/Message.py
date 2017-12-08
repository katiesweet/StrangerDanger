#!/usr/bin/python
from abc import ABCMeta, abstractmethod
import cPickle as pickle
import copy
from CommunicationLibrary.Messages.SharedObjects.MessageId import MessageId
from Crypto.Cipher import AES

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
        encodedMsg = pickle.dumps(self)
        # generate key for encryption based on the passphrase and Initialization Vector
        key = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
        encryptedMsg = key.encrypt(encodedMsg)
        return encryptedMsg

    @staticmethod
    def decode(encodedMsg):
        # generate key for decryption based on the passphrase and Initialization Vector
        key = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
        decryptedMsg = key.decrypt(encodedMsg)
        decodedMsg = pickle.loads(decryptedMsg)
        return decodedMsg
