import sys
sys.path.append('../')
from Tkinter import *

import logging
logging.basicConfig(filename="Client.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - Thread: %(thread)d -\
    %(message)s')

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
from CommunicationLibrary.Messages.RequestMessages import * # AliveRequest
from CommunicationLibrary.Messages.ReplyMessages import *
# from CommunicationLibrary.Messages.SharedObjects.Envelope import Envelope
# from CommunicationLibrary.Messages.SharedObjects.ProcessType import ProcessType
from CommunicationLibrary.Messages.SharedObjects import *

class Client:
    def __init__(self, master):
        logging.info("Creating client process")
        self.master = master
        master.title("Client")
        self.comm = CommunicationSubsystem.CommunicationSubsystem()
        self.registrationServerAddress = ("34.209.72.192" , 50000)
        #self.registrationServerAddress = ("localhost", 50000)
        self.mainServerAddress = (None, None)
        self.canStartSending = False

        self.sendRegisterRequest()
        self.sendServerListRequest()
        self.checkForMessagesPeriodically()

        #self.sendServerListRequest()

    ###### Messages Client Needs to Send #####
    def sendRegisterRequest(self):
        message = Envelope(self.registrationServerAddress, RegisterRequest(ProcessType.ClientProcess))
        self.comm.sendMessage(message)
        logging.debug("Sending message " + repr(message))

    def sendServerListRequest(self):
        if not self.canStartSending:
            self.master.after(50, self.sendServerListRequest)
        else:
            envelope = Envelope(self.registrationServerAddress, ServerListRequest())
            self.comm.sendMessage(envelope)
            logging.debug("Sending message " + repr(envelope))

    def sendStatisticsRequest(self):
        """ Message user sends when they want statistics -> button click handler? """
        if self.mainServerAddress == (None, None):
            print "No main server to send to. Please try again later"
        else:
            print "Message not implemented yet"

    def checkForMessagesPeriodically(self):
        try:
            haveMessage, envelope = self.comm.getMessage()
            if haveMessage:
                self.processNewMessage(envelope)
            self.master.after(50, self.checkForMessagesPeriodically)
        except:
            return

    def processNewMessage(self, envelope):
        if isinstance(envelope.message, RegisterReply):
            self.handleRegisterReply(envelope)
        elif isinstance(envelope.message, ServerListReply):
            self.handleServerListReply(envelope)

    def handleRegisterReply(self, envelope):
        processId = envelope.message.processId

        LocalProcessInfo.setProcessId(processId)
        Label(self.master, text="Process Id: " + str(processId)).grid(row=1, column=1)
        self.canStartSending = True

    def handleServerListReply(self, envelope):
        mainServers = envelope.message.servers
        if not mainServers:
            print "Reponse contained no main servers"
            self.mainServerAddress = (None, None)
        else:
            self.mainServerAddress = mainServers[0]

if __name__ == '__main__':
    root = Tk()
    client = Client(root)
    root.mainloop()
