# coding: utf-8
__author__ = 'Harald Floor Wilhelmsen'

import time

class Contract(object):

    idincrement = 0

    def __init__(self, operation, args, id):
        self.expiration = time.time() + 86400
        self.args = args
        self.operation = operation
        self.contractid = id

    def sign(self, args):
        if args[0] == self.args[1]:
            return self.operation(self.args)

    def isexpired(self):
        return time.time() > self.expiration

    def __str__(self): # id op exp: arg1 arg2 arg3 argn
        return ": ".join([" ".join([str(self.contractid), self.operation, str(self.expiration)]), " ".join(self.args)])

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def getnew(operation, args):
        contract = Contract(operation, args, Contract.idincrement)
        Contract.idincrement += 1
        return contract