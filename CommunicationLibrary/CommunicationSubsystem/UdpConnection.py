import socket
import thread
import logging
#import sys
from CommunicationLibrary.Messages.AbstractMessages import * # Message
from CommunicationLibrary.Messages.SharedObjects.Envelope import Envelope
from Crypto.Cipher import AES

class UdpConnection:
    def __init__(self, outgoingMessageQueue, incomingMessageQueue, myEndpoint):
        logging.info("Creating UDP Socket")
        self.outgoingMessageQueue = outgoingMessageQueue
        self.incomingMessageQueue = incomingMessageQueue

        self.shouldListen = True
        thread.start_new_thread(self.__run, (myEndpoint,))

    def __del__(self):
        # TODO: This destructor isn't getting called
        logging.info("Destroying UDP Socket")
        self.shouldListen = False
        # Join thread?

    def encryptMessage(self, message):
        # generate key for encryption based on the passphrase and Initialization Vector
        key = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
        return key.encrypt(message)

    def decryptMessage(self, message):
        # generate key for decryption based on the passphrase and Initialization Vector
        key = AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
        return key.decrypt(message)

    def __sendMessage(self, udpSocket, envelope):
        encodedMessage = envelope.message.encode()
        encryptedMessage = self.encryptMessage(encodedMessage)
        try:
            #print "Sending message", envelope.message, " to ", \
            #    envelope.endpoint
            logging.debug("Sending message " + repr(envelope.message) \
                + " to " + repr(envelope.endpoint))
            #print 'length of message is {}'.format(len(encodedMessage))
            udpSocket.sendto(encryptedMessage, envelope.endpoint)
        except socket.error, msg:
            logging.error("Could not send message to server.")
            #print socket.error, msg

    def __receiveMessage(self, udpSocket):
        try:
            data, addr = udpSocket.recvfrom(32768)
            if data:
                decryptedData = self.decryptMessage(data)
                message = Message.decode(decryptedData)
                #print "Received message: ", message, " from ", addr
                logging.debug("Received message " + repr(message) + \
                    " from " + repr(addr))
                envelope = Envelope(addr, message)
                self.incomingMessageQueue.put(envelope)
        except:
            return

    def __run(self, myEndpoint):
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSocket.setblocking(False)
        try:
            udpSocket.bind(myEndpoint)
        except:
            logging.error("Binding error")

        logging.debug("UDP Socket listening at endpoint " + \
            repr(udpSocket.getsockname()))

        while self.shouldListen:

            # If there is a message waiting to be sent, send it
            if not self.outgoingMessageQueue.empty():
                logging.info("There are messages to be sent on queue")
                self.__sendMessage(udpSocket, self.outgoingMessageQueue.get())

            # See if there is a message to be received
            self.__receiveMessage(udpSocket)
