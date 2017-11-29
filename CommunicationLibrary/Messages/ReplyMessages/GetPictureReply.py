#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Reply import Reply


class GetPictureReply(Reply):

    def __init__(self, success, picture):
        super(GetPictureReply, self).__init__(success)
        self.picture = picture
