import TcpConnection
import UdpConnection
import thread

# TODO: Set up a TCP listener that is always listening for new connections
class SocketManager:
    """Transport Layer Communication Protocol Manager"""
    def __init__(self, toSocketQueue, fromSocketQueue):
        self.toSocketQueue = toSocketQueue
        self.fromSocketQueue = fromSocketQueue # Used by sockets directly

        self.udpConnections = UdpConnection.UdpConnection(self.fromSocketQueue)
        self.tcpConnections = {}

        self.shouldRun = True
        thread.startNewThread(self.__run)

    def __run(self):
        while self.shouldRun:
            # Send message
            if not self.toSocketQueue.empty():
                # Message to send
                envelope = self.toSocketQueue.get()
                if envelope.messageType == 'UDP':
                    self.udpConnection.sendMessage(envelope)
                else:
                    # We need to check and see if TCP Connection exists
                    endpoint = envelope.endpoint
                    if endpoint in tcpConnections:
                        self.tcpConnections[endpoint].sendMessage(envelope)
                    else:
                        newTcpConnection = TcpConnection.TcpConnection(self.fromSocketQueue)

                        self.tcpConnections[endpoint] = newTcpConnection
                        newTcpConnection.sendMessage(message)
