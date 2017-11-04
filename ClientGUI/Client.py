import sys
sys.path.append('../CommunicationLibrary/CommunicationSubsystem')
sys.path.append('../CommunicationLibrary/Messages')

import CommunicationSubsystem
import RequestMessages.AliveRequest as AliveRequest

class Envelope:
    def __init__(self, endpoint, message):
        self.endpoint = endpoint
        self.message = message

class Client:
    def __init__(self):
        comm = CommunicationSubsystem.CommunicationSubsystem()
        registrationServer =('127.0.0.1', 61725)
        message = AliveRequest.AliveRequest()
        comm.sendMessage(message)

        # var = ""
        # while var != "q":
        #     var = raw_input("Enter something to send: ")
        #     message = Envelope(registrationServer, var)
        #     comm.sendMessage(message)

Client()
