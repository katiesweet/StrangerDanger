#!/usr/bin
from LoginRequest import LoginRequest

class CameraLoginRequest(LoginRequest):

    def __init__(self, messageId, conversationId, processType, processLabel, identity, name, clusterId, clusterIdPassword):
        super(CameraLoginRequest,self).__init__(messageId, conversationId, processType, processLabel, identity)
        self.name = name
        self.clusterId = clusterId
        self.clusterIdPassword = clusterIdPassword
