#!/usr/bin
from abc import ABCMeta, abstractmethod
from Message import Message


class Reply(Message):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, success):
        super(Reply, self).__init__()
        self.success = success
