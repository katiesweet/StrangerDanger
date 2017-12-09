import socket
import thread
import logging
from CommunicationLibrary.Messages.AbstractMessages import * # Message
from CommunicationLibrary.Messages.ReplyMessages import *
from CommunicationLibrary.Messages.RequestMessages import *
from CommunicationLibrary.Messages.SharedObjects.Envelope import Envelope
from CommunicationLibrary.Messages.SharedObjects.KeyManager import KeyManager
from CommunicationLibrary.Messages.SharedObjects.KeyGenerator import KeyGenerator

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

    def encryptRegisterRequest(self, message):
        logging.debug('Encrypting Register Request')
        key = KeyManager.loadKey('RegistryPublicKey.pem')
        return KeyManager.encryptMessage(key, message)

    def decryptRegisterRequest(self, message):
        logging.debug('Decrypting Register Request')
        key = KeyManager.loadKey('RegistryPrivateKey.pem')
        return KeyManager.decryptMessage(key, message)

    def encryptRegisterReply(self, message, key):
        logging.debug('Encrypting Register Reply')
        return KeyManager.encryptMessage(key, message)

    def decryptRegisterReply(self, message):
        logging.debug('Decrypting Register Reply')
        key = KeyManager.loadKey('ProcessPrivateKey.pem')
        return KeyManager.decryptMessage(key, message)

    def generateAndSaveKeys(self):
        logging.debug('Generating Public/Private keys')
        key = KeyGenerator.generateKeyPair()
        public_key = key.publickey()
        KeyManager.saveKey('ProcessPrivateKey.pem', key)
        KeyManager.saveKey('ProcessPublicKey.pem', public_key)
        return public_key

    def __sendMessage(self, udpSocket, envelope):
        try:
            if isinstance(envelope.message, RegisterRequest):
                public_key = self.generateAndSaveKeys()
                envelope.message.key = public_key
                message = envelope.message.encode()
                logging.debug('Encrypting Register Request message')
                message = self.encryptRegisterRequest(message)
                message = 'encryptedRequest{}'.format(message)
            elif isinstance(envelope.message, RegisterReply):
                message = envelope.message.encode()
                logging.debug('Encrypting Register Reply message')
                message = self.encryptRegisterReply(message, envelope.message.key)
                message = 'encryptedReply{}'.format(message)
            else:
                message = envelope.message.encode()
            #print "Sending message", envelope.message, " to ", \
            #    envelope.endpoint
            logging.debug("Sending message " + repr(envelope.message) \
                + " to " + repr(envelope.endpoint))
            #print 'length of message is {}'.format(len(encodedMessage))
            udpSocket.sendto(message, envelope.endpoint)
        except socket.error, msg:
            logging.error("Could not send message to server: {}".format(msg))
            #print socket.error, msg

    def __receiveMessage(self, udpSocket):
        try:
            data, addr = udpSocket.recvfrom(32768)
            if data:
                if (data[0:16] == 'encryptedRequest'):
                    logging.debug('Decrypting Register Request message')
                    data = self.decryptRegisterRequest(data[16:])
                if (data[0:14] == 'encryptedReply'):
                    logging.debug('Decrypting Register Request message')
                    data = self.decryptRegisterReply(data[14:])
                message = Message.decode(data)
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
