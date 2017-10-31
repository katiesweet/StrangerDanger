import socket
import Queue
import thread

class UdpConnection:
    # QUESTION: HOW SHOULD IP ADDRESS AND PORT BE ASSIGNED???
    def __init__(self, incomingMessageQueue):
        self.outgoingQueue = Queue()
        self.incomingMessageQueue = incomingMessageQueue

        self.shouldListen = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        self.socket.bind((socket.gethostname(), 0)) # Tells to give external hostname and port ?
        thread.startNewThread(self.__run)

    def __del__(self):
        self.shouldListen = False
        # Join thread?

    def sendMessage(self, envelope):
        self.outgoingQueue.append(envelope)

    def __run(self):
        while self.shouldListen:

            # If there is a message waiting to be sent, send it
            if not self.outgoingQueue.empty():
                envelope = self.outgoingQueue.get()
                encodedMessage = envelope.message.encode() # SHEM!!!!
                try:
                    self.socket.sendTo(encodedMessage, envelope.endpoint)
                except:
                    logging.error("Could not send message to server.")

            # See if there is a message to be received
            data, addr = self.socket.recvfrom(1024):
                if data:
                    message = decodeMessage(data) # SHEM!!!!!
                    envelope = Envelope(addr, message)
                    self.incomingMessageQueue.append(envelope)
