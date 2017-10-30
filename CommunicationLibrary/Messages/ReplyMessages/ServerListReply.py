#!/usr/bin
from AbstractMessages.Reply import Reply


class ServerListReply(Reply):

    def __init__(self, success, servers):
        super(ServerListReply, self).__init__(success)
        self.servers = servers
