#!/usr/bin/python
from LoginRequest import LoginRequest


class CameraLoginRequest(LoginRequest):

    def __init__(self, processType, processLabel, identity, name, clusterId, clusterIdPassword):
        super(CameraLoginRequest, self).__init__(processType, processLabel, identity)
        self.name = name
        self.clusterId = clusterId
        self.clusterIdPassword = clusterIdPassword
