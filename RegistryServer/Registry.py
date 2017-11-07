import sys
sys.path.append('../') # Start at root directory for all imports

import logging
logging.basicConfig(filename="Registry.log", level=logging.DEBUG, \
    format='%(asctime)s - %(levelname)s - %(module)s - Thread: %(thread)d -\
    %(message)s')

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem

class Registry:
    def __init__(self):
        logging.info("Creating registry process")
        myEndpoint = ('localhost', 50000)
        comm = CommunicationSubsystem.CommunicationSubsystem(myEndpoint)
        var = raw_input("Enter something to quit.\n")

Registry()
