#!/usr/bin/python
from abc import ABCMeta, abstractmethod
from Message import Message


class Request(Message):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(Request, self).__init__()
