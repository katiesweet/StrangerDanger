#!/usr/bin/python
import cPickle as pickle

class KeyManager:

    @staticmethod
    def saveKey(filename, key):
        pickle.dump( key, open(filename, "wb") )

    @staticmethod
    def loadKey(filename):
        key = pickle.load( open(filename, "rb") )
        return key
