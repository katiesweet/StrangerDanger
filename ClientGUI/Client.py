import sys
sys.path.append('../')
from Tkinter import *
from ttk import Separator, Scrollbar, Sizegrip

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
        self.comm = CommunicationSubsystem.CommunicationSubsystem()
        self.registrationServerAddress = ("34.209.66.116" , 50000)
        self.mainServerAddress = (None, None)
        self.cameraSelection = {}
        self.canStartSending = False
        self.setupGui()

        self.sendRegisterRequest()
        self.sendServerListRequest()
        self.checkForMessagesPeriodically()

        #self.sendServerListRequest()

    def setupGui(self):
        self.master.title("Stranger Danger")

        Label(self.master, text="Stranger Danger: Distributed Home Monitoring System", font=("Calibri", 20)).grid(columnspan=3)
        Separator(self.master, orient="horizontal").grid(row=1, columnspan=3, sticky="ew")

        Label(self.master, text="Select Camera(s)", font=("Calibri", 16)).grid(row=2)
        #rowIndex = self.handleCameraListReply("dummy")

        self.setupPictureReportSection()

        Label(self.master, text="Statistics Report", font=("Calibri", 16)).grid(row=2, column=2)
        Separator(self.master, orient="horizontal").grid(row=8, columnspan=3, sticky="ew", pady=(10,0))
        self.setupReportSection()

    def setupReportSection(self):
        reportFrame = Frame(self.master)
        reportFrame.grid(row=9, column=0, columnspan=3, sticky="we")

        scrollbar = Scrollbar(reportFrame)
        mylist = Listbox(reportFrame, yscrollcommand = scrollbar.set, bd=0)
        for line in range(100):
           mylist.insert(END, "Report Item " + str(line))

        mylist.pack(side = LEFT, fill = BOTH, padx=(10, 0), pady=10)
        scrollbar.pack(side = LEFT, fill = Y, pady=10)
        scrollbar.config( command = mylist.yview )

        self.reportVisualFrame = Frame(reportFrame, bg="blue", width=640, height=480)
        self.reportVisualFrame.pack(side=LEFT, fill=BOTH, padx=10, pady=10)

    def setupPictureReportSection(self):
        Label(self.master, text="Picture Report", font=("Calibri", 16)).grid(row=2, column=1)
        self.picReportChoice = IntVar()
        Radiobutton(self.master, text="Most Recent", variable=self.picReportChoice, value=1).grid(row=3, column=1, sticky="w")

        Radiobutton(self.master, text="Date (MM/DD/YY) Range:", variable=self.picReportChoice, value=2).grid(row=4, column=1, sticky="w")
        self.startDate = Text(self.master, relief=GROOVE, height=1, width=10, borderwidth=2)
        self.startDate.insert(END, "StartDate")
        self.startDate.grid(row=5, column=1)
        self.endDate = Text(self.master, relief=GROOVE, height=1, width=10, borderwidth=2)
        self.endDate.insert(END, "EndDate")
        self.endDate.grid(row=6, column=1)

        #
        # self.startDate = StringVar()
        # self.endDate = StringVar()
        #
        #
        # Label(self.master, textvariable=self.startDate).grid(row=5, column=1)
        # Label(self.master, textvariable=self.endDate).grid(row=6, column =1)

        Button(self.master, text="GenerateReport", command=self.generatePicReport).grid(row=7, column=1)
    #######
    def generatePicReport(self):
        for cam, isSelected in self.cameraSelection.items():
            if isSelected.get() == 1:
                print cam

    ###### Messages Client Needs to Send #####
    def sendRegisterRequest(self):
        message = Envelope(self.registrationServerAddress, RegisterRequest(ProcessType.ClientProcess))
        self.comm.sendMessage(message)
        logging.debug("Sending message " + repr(message))

    def sendServerListRequest(self):
        if not self.canStartSending:
            self.master.after(50, self.sendServerListRequest)
        else:
            envelope = Envelope(self.registrationServerAddress, ServerListRequest(ProcessType.MainServer))
            logging.debug("Sending message " + repr(envelope))
            self.comm.sendMessage(envelope)

            envelope = Envelope(self.registrationServerAddress, ServerListRequest(ProcessType.CameraProcess))
            logging.debug("Sending message " + repr(envelope))
            self.comm.sendMessage(envelope)

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
            self.handleProcessListResponse(envelope)

    def handleRegisterReply(self, envelope):
        processId = envelope.message.processId

        LocalProcessInfo.setProcessId(processId)
        # Label(self.master, text="Process Id: " + str(processId)).grid(row=1, column=1)
        self.canStartSending = True

    def handleProcessListResponse(self, envelope):
        processType = envelope.message.processType
        if processType == ProcessType.MainServer:
            self.handleMainServerReply(envelope)
        elif processType == ProcessType.CameraProcess:
            self.handleCameraListReply(envelope)

    def handleMainServerReply(self, envelope):
        #self.handleCameraListReply(envelope)
        mainServers = envelope.message.servers
        if not mainServers:
            logging.info("Reponse contained no main servers")
            self.mainServerAddress = (None, None)
        else:
            server = mainServers[0]
            print "Corresponding with main server: ", repr(server)
            logging.info("Now corresponding with main server:" + repr(server))
            self.mainServerAddress = server
            message = Envelope(self.mainServerAddress, AliveRequest())
            self.comm.sendMessage(message)

    def handleCameraListReply(self, envelope):
        cameraNames = envelope.message.servers
        rowIndex = 3
        for camera in cameraNames:
            camVar = IntVar()
            self.cameraSelection[camera] = camVar
            Checkbutton(self.master, text = camera, variable = camVar, \
                 onvalue = 1, offvalue = 0).grid(row=rowIndex)
            rowIndex += 1
        return rowIndex


if __name__ == '__main__':
    root = Tk()
    client = Client(root)
    root.mainloop()
