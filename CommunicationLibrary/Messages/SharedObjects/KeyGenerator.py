#!/usr/bin/python
from Crypto.PublicKey import RSA
from Crypto import Random

class KeyGenerator:

    @staticmethod
    def generateKeyPair():
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator)
        # key holds a public key, the key itself is the private key
        return key
