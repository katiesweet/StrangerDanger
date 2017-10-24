#!/usr/bin
from Message import Message

class Request(Message):

    def __init__(self, messageId, conversationId):
        super(Request, self).__init__(messageId, conversationId)
