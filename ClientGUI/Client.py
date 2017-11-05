import sys
sys.path.append('../')

import logging
logging.basicConfig(filename="Client.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem
from CommunicationLibrary.Messages.RequestMessages import * # AliveRequest
from CommunicationLibrary.Messages.SharedObjects.Envelope import Envelope

class Client:
    def __init__(self):
        logging.info("Creating client process")
        comm = CommunicationSubsystem.CommunicationSubsystem()
        registrationServer = ('localhost', 50000)

        for i in range(3):
            message = Envelope(registrationServer, AliveRequest())
            comm.sendMessage(message)
            logging.debug("Sending message " + repr(message))

        var = raw_input("Enter something to quit.\n")

Client()
