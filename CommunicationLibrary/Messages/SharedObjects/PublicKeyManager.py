#!/usr/bin/python
import cPickle as pickle

class PublicKeyManager:

    @staticmethod
    def savePublicKey(filename, publicKey):
        pickle.dump( publicKey, open(filename, "wb") )

    @staticmethod
    def loadPublicKey(filename):
        publicKey = pickle.load( open(filename, "rb") )
