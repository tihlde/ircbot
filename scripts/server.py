# coding: utf-8
__author__ = 'Harald'


class Server(object):
    owner = ""
    hostname = ""
    prettyname = ""
    statusgroup = ""
    notifygroup = ""

    def __init__(self, owner, hostname, prettyname, statusgroup, notifygroup):
        self.owner = owner
        self.hostname = hostname
        self.prettyname = prettyname
        self.statusgroup = statusgroup
        self.notifygroup = notifygroup

    def __str__(self):
        string = self.hostname + " " + self.owner + ": " + self.prettyname + " " + self.statusgroup + " " + self.notifygroup
        return string

    def __repr__(self):
        return self.__str__()