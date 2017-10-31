#!/usr/bin
from AbstractMessages.Request import Request


class AliveRequest(Request):

    def __init__(self):
        super(AliveRequest, self).__init__()
