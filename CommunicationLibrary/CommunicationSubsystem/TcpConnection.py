import socket


# TODO: Make like UdpConnection class
# NOTE: Shem, use the UdpConnection class to see the encoding and d
class TcpConnection:

    def __init__(self, incomingMessageQueue, endpoint):
        self.outgoingQueue = Queue()
        self.incomingMessageQueue = incomingMessageQueue

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(endpoint) # QUESTION : Is this best way?
        self.mySocket.listen(1)
        conn, addr = self.mySocket.accept()

    # def receiveMessage(self):
    #     BUFFER_SIZE = 20 # Normally 1024, but we want fast response
    #     while True:
    #         data = conn.recv(BUFFER_SIZE)
    #         if not data: continue
    #         print "revieved data:", data
#
# # while 1:
# #     data = conn.recv(BUFFER_SIZE)
# #     if not data: break
# #     print "received data:", data
# #     conn.send(data)  # echo
#     conn.close()
