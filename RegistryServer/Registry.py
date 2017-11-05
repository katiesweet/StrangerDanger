import sys
sys.path.append('../') # Start at root directory for all imports

import logging
logging.basicConfig(filename="Registry.log", level=logging.DEBUG, \
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

from CommunicationLibrary.CommunicationSubsystem import CommunicationSubsystem

class Registry:
    def __init__(self):
        comm = CommunicationSubsystem.CommunicationSubsystem()
        var = raw_input("Enter something to quit: ")

Registry()
