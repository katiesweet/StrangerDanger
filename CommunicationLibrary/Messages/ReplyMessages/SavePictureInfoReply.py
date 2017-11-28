#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Reply import Reply

class SavePictureInfoReply(Reply):

    def __init__(self, success):
        super(SavePictureInfoReply, self).__init__(success)
