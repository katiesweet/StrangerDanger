#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Request import Request


class AliveRequest(Request):

    def __init__(self):
        super(AliveRequest, self).__init__()
