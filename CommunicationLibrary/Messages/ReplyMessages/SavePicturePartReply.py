#!/usr/bin/python
from CommunicationLibrary.Messages.AbstractMessages.Reply import Reply

class SavePicturePartReply(Reply):

    def __init__(self, success, partNumber, cameraName):
        super(SavePicturePartReply, self).__init__(success)
        self.partNumber = partNumber
        self.cameraName = cameraName
