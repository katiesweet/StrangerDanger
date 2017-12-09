#!/usr/bin/python
from Crypto.PublicKey import RSA

class KeyManager:

    @staticmethod
    def saveKey(filename, key):
        with open(filename, 'wb') as f:
            f.write(key.exportKey('PEM'))

    @staticmethod
    def loadKey(filename):
        with open(filename, 'rb') as f:
            key = RSA.importKey(f.read())
        return key

    @staticmethod
    def encryptMessage(key, msg):
        # need to split string because of encrypt size limit (~120)
        pieces = KeyManager.splitString(msg,120)

        # encode each piece of the msg
        for i in xrange(0,len(pieces)):
            pieces[i] = key.encrypt(pieces[i], 32)
        # encoding results in a Tuple('eachPiece',)
        # convert to string
        pieces = [x[0] for x in pieces]

        # combine pieces
        encryptedMsg = ''.join(pieces)
        return encryptedMsg

    @staticmethod
    def decryptMessage(key, msg):
        # need to split string because of decrypt size limit (128 because encrypt = 120)
        pieces = KeyManager.splitString(msg,128)
        # convert back to Tuples
        pieces = [(x,) for x in pieces]

        # decode each piece of the msg
        for i in xrange(0,len(pieces)):
            pieces[i] = key.decrypt(pieces[i])
        # combine pieces
        decryptedString = ''.join(pieces)
        return decryptedString

    @staticmethod
    def splitString(string, pieceSize):
        return [string[i:i+pieceSize] for i in range(0, len(string), pieceSize)]
