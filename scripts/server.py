__author__ = 'Harald'

class Server(object):
    def __init__(self, owner, hostname, prettyname, statusgroup, notifygroup):
        self.owner = owner
        self.hostname = hostname
        self.prettyname = prettyname
        self.statusgroups = statusgroup
        self.notifygroup = notifygroup