import sys
sys.path.append('../')
from Tkinter import *
from ttk import Separator, Scrollbar, Sizegrip
from PIL import Image, ImageTk
import cv2
import DateEntry

import logging
logging.basicConfig(filename="Client.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - Thread: %(thread)d -\
    %(message)s')

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
from CommunicationLibrary.Messages.RequestMessages import * # AliveRequest
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.SharedObjects import *

class Client:
    def __init__(self, master):
        logging.info("Creating client process")
        self.master = master
        self.comm = CommunicationSubsystem.CommunicationSubsystem()
        self.registrationServerAddress = ("localhost" , 50000)
        #self.registrationServerAddress = ("192.168.0.23" , 50000)
        self.mainServerAddress = (None, None)
        self.cameraSelection = {}
        self.picReportItems = {}
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

        self.setupCameraSection()
        self.setupPictureReportSection()
        self.setupStatisticsReportSection()
        Separator(self.master, orient="horizontal").grid(row=3, columnspan=3, sticky="ew", pady=(10,0))
        self.setupReportSection()

    def setupCameraSection(self):
        self.cameraFrame = Frame(self.master)
        self.cameraFrame.grid(row=2, sticky='n', padx=50)

        Label(self.cameraFrame, text="Select Camera(s)", font=("Calibri", 16)).pack()

    def setupPictureReportSection(self):
        picReportSection = Frame(self.master)
        picReportSection.grid(row=2, column=1)

        Label(picReportSection, text="Picture Report", font=("Calibri", 16)).pack()

        self.picReportChoice = IntVar()
        Radiobutton(picReportSection, text="Most Recent", variable=self.picReportChoice, value=1).pack(anchor='w')

        Radiobutton(picReportSection, text="Date Range:", variable=self.picReportChoice, value=2).pack(anchor='w')

        self.startDate = DateEntry.DateEntry(picReportSection, "Start Date: ")
        self.startDate.pack()
        self.endDate = DateEntry.DateEntry(picReportSection, "End Date:  ")
        self.endDate.pack()

        Button(picReportSection, text="GenerateReport", command=self.generatePicReport).pack()


    def setupStatisticsReportSection(self):
        statsFrame = Frame(self.master)
        statsFrame.grid(row=2, column=2, sticky='n', padx=50)

        Label(statsFrame, text="Statistics Report", font=("Calibri", 16)).pack()

    def setupReportSection(self):
        reportFrame = Frame(self.master)
        reportFrame.grid(row=4, column=0, columnspan=3, sticky="we")

        scrollbar = Scrollbar(reportFrame)
        self.mylist = Listbox(reportFrame, yscrollcommand = scrollbar.set, bd=0)
        self.mylist.bind('<<ListboxSelect>>', self.selectedReportItem)
        #self.setupDummyList()
        self.mylist.pack(side = LEFT, fill = BOTH, padx=(10, 0), pady=10)
        scrollbar.pack(side = LEFT, fill = Y, pady=10)
        scrollbar.config( command = self.mylist.yview )

        picFrame = Frame(reportFrame, width=320, height=288)
        picFrame.pack_propagate(0)
        self.reportVisualLabel = Label(picFrame)
        self.reportVisualLabel.pack()
        #self.loadImageFromFile()
        picFrame.pack(side=LEFT, fill=BOTH, padx=10, pady=10)

    def loadImageFromFile(self):
        path = "/Users/katiesweet/Desktop/KatieCam_2017-11-30 21:19:05.192955.jpg"
        image = cv2.imread(path)
        self.displayPicture(image)

    def displayPicture(self, picture):
        im = Image.fromarray(picture)
        imgtk = ImageTk.PhotoImage(image=im)
        self.reportVisualLabel.configure(image=imgtk)
        self.reportVisualLabel.image = imgtk

    def setupDummyList(self):
        camData = [{"camName": "KatieCam", "timeStamp": "ts1", "picLocation": "location1"},{"camName": "SarahCam", "timeStamp": "ts2", "picLocation": "location2"}]
        msg = RawQueryReply(True, camData)
        envelope = Envelope(self.registrationServerAddress, msg)
        self.handlePictureReportReply(envelope)
    #######
    def generatePicReport(self):
        #self.loadImageFromFile()
        reportType = self.picReportChoice.get()
        if reportType == 0:
            return
        cameras = []
        for cam, isSelected in self.cameraSelection.items():
            if isSelected.get() == 1:
                cameras.append(cam)
        mostRecent = True if reportType == 1 else False
        isValid1, startDate = self.startDate.getDate()
        isValid2, endDate = self.endDate.getDate()
        if not isValid1 or not isValid2:
            print "Invalid date"
            return
        timePeriod = DateRange(startDate, endDate)
        # msg = RawQueryRequest(mostRecent, timePeriod, cameras)
        # env = Envelope(self.mainServerAddress, msg)
        # self.comm.sendMessage(env)

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
        elif isinstance(envelope.message, RawQueryReply):
            self.handlePictureReportReply(envelope)
        elif isinstance(envelope.message, GetPictureReply):
            self.handleGetPictureReply(envelope)

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
        for camera in cameraNames:
            camVar = IntVar()
            self.cameraSelection[camera] = camVar
            Checkbutton(self.cameraFrame, text = camera, variable = camVar, \
                 onvalue = 1, offvalue = 0).pack()

    def handlePictureReportReply(self, envelope):
        picReportItems = envelope.message.data
        self.picReportItems = {}
        self.mylist.delete(0, END)
        for picture in picReportItems:
            print picture
            camName = picture["camName"]
            timeStamp = picture["timeStamp"]
            picLocation = picture["picLocation"]
            listItemVal = camName + ": " + timeStamp
            self.picReportItems[listItemVal] = picLocation
            self.mylist.insert(END, listItemVal)

    def selectedReportItem(self, evt):
        index = self.mylist.curselection()
        if not index:
            return
        reportItem = self.mylist.get(index)
        pictureLocation = self.picReportItems[reportItem]
        envelope = Envelope(self.mainServerAddress, GetPictureRequest(pictureLocation))
        print envelope.message
        #self.comm.sendMessage(envelope)

    def handleGetPictureReply(self, envelope):
        picture = envelope.message.picture
        self.displayPicture(picture)


if __name__ == '__main__':
    root = Tk()
    client = Client(root)
    root.mainloop()
