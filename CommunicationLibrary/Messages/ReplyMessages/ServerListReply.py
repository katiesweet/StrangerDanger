#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Reply import Reply


class ServerListReply(Reply):

    def __init__(self, success, processType, servers):
        super(ServerListReply, self).__init__(success)
        self.processType = processType
        self.servers = servers
