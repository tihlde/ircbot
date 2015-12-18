# coding: utf-8
__author__ = 'Harald Floor Wilhelmsen'

import time


class Contract(object):
    idincrement = 0

    def __init__(self, operation, args, id, expiration):
        self.expiration = expiration
        self.args = args
        self.operation = operation
        self.contractid = id

    def sign(self, args):
        if args[0] == self.args[1]:
            return self.operation(self.args)

    def isexpired(self):
        return time.time() > self.expiration

    def __str__(self):  # id op exp: arg1 arg2 arg3 argn
        return ": ".join(
                [" ".join([str(self.contractid), self.operation.__name__, str(self.expiration)]),
                 " ".join(self.args)])

    def __repr__(self):
        return self.__str__()

    def prettyprint(self):
        return ' '.join(['id:' + self.contractid, 'expires:' +
                         time.strftime('%H:%M-%d.%m.%y', time.localtime(self.expiration)),
                         'arguments: ' + ' '.join(self.args)])

    @staticmethod
    def getnew(operation, args, bot):
        contract = Contract(operation, args, Contract.idincrement, time.time() + 86400)
        Contract.idincrement += 1
        bot.sendtext(' '.join(
                [args[0], 'wants you to sign a contract, to sign it use the command >sign <id>.',
                 'To find the id of a contract use the command >contracts']), args[1])
        return contract
