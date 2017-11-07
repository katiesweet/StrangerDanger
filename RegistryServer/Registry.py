import sys
import threading
sys.path.append('../') # Start at root directory for all imports

import logging
logging.basicConfig(filename="Registry.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - Thread: %(thread)d -\
    %(message)s')

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem

class Registry:
    nextProcessId = 0
    threadLock = threading.Lock()

    def __init__(self):
        logging.info("Creating registry process")
        myEndpoint = ('localhost', 50000)
        comm = CommunicationSubsystem.CommunicationSubsystem(myEndpoint)
        var = raw_input("Enter something to quit.\n")

    @staticmethod
    def getProcessId():
        with Registry.threadLock:
            if Registry.nextProcessId == sys.maxint:
                Registry.nextProcessId = 0
            Registry.nextProcessId += 1
        return Registry.nextProcessId

Registry()
