#!/usr/bin
from AbstractMessages.Reply import Reply

class ServerListReply(Reply):

    def __init__(self, messageId, conversationId, success, servers):
        super(ServerListReply,self).__init__(messageId, conversationId, success)
        self.servers = servers
