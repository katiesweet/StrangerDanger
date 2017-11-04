import socket
import thread

class UdpConnection:
    # QUESTION: HOW SHOULD IP ADDRESS AND PORT BE ASSIGNED???
    def __init__(self, outgoingMessageQueue, incomingMessageQueue):
        self.outgoingMessageQueue = outgoingMessageQueue
        self.incomingMessageQueue = incomingMessageQueue

        self.shouldListen = True
        thread.start_new_thread(self.__run, ())


    def __del__(self):
        self.shouldListen = False
        # Join thread?

    # def sendMessage(self, envelope):
    #     self.outgoingQueue.put(envelope)

    def __run(self):
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSocket.setblocking(False)
        #endpoint = (socket.gethostname(), 0)
        endpoint = ('localhost', 0)
        udpSocket.bind(endpoint)
        print udpSocket.getsockname()

        while self.shouldListen:

            # If there is a message waiting to be sent, send it
            if not self.outgoingMessageQueue.empty():
                envelope = self.outgoingMessageQueue.get()
                encodedMessage = envelope.message.encode() # QUESTION: SHEM
                try:
                    print "Sending message", envelope.message, " to ", envelope.endpoint
                    udpSocket.sendto(encodedMessage, envelope.endpoint)
                    #udpSocket.sendTo(encodedMessage, envelope.endpoint)
                except:
                    #logging.error("Could not send message to server.")
                    print "Could not send message to server"

            # See if there is a message to be received
            try:
                data, addr = udpSocket.recvfrom(1024)
                if data:
                    print "Received message: ", data
                    #udpSocket.sendto(data, addr)
                    #message = Message.decode (data) # QUESTION: SHEM
                    #envelope = Envelope(addr, message)
                    #self.incomingMessageQueue.put(envelope)
            except:
                continue
