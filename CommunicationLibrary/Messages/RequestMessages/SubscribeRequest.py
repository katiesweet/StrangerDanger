#!/usr/bin
from AbstractMessages.Request import Request


class SubscribeRequest(Request):

    def __init__(self, clusterId):
        super(SubscribeRequest, self).__init__()
        self.clusterId = clusterId
