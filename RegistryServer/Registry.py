import sys
sys.path.append('../CommunicationLibrary/CommunicationSubsystem')

import CommunicationSubsystem

class Envelope:
    def __init__(self, endpoint, message):
        self.endpoint = endpoint
        self.message = message

class Registry:
    def __init__(self):
        comm = CommunicationSubsystem.CommunicationSubsystem()
        var = raw_input("Enter something to quit: ")

Registry()
