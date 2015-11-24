# coding: utf-8
__author__ = 'Harald'

from group import Group
from server import Server


class Dataobject(object):
    ident = []
    data = []

    def __init__(self, ident, data):
        self.ident = ident
        self.data = data


def striplist(list):
    list = [x.replace(' ', '') for x in list]
    return [x.replace('\n', '') for x in list]


def readdata(filestring):
    dataobjects = []
    with open(filestring, 'r') as file:
        for line in file:
            if line == '':
                continue
            splitindex = line.find(': ')
            ident = striplist(line[:splitindex].strip().split(' '))
            data = striplist(line[splitindex + 1:].strip().split(' '))
            dataobjects.append(Dataobject(ident, data))
    return dataobjects


def readgroups():
    groups = {}
    readfile = readdata('config/groups')
    for dataobject in readfile:
        groups[dataobject.ident[0]] = Group(dataobject.ident[0], dataobject.ident[1],
                                            dataobject.data)
    return groups


# read servers
def readservers():
    servers = {}
    readfile = readdata('config/servers')
    for dataobject in readfile:
        servers[dataobject.ident[0]] = Server(dataobject.ident[0],
                                              dataobject.ident[1], dataobject.data[0],
                                              dataobject.data[1], dataobject.data[2])
    return servers


groups = readgroups()
servers = readservers()


def addusertogroup(user, groupname, recipient):
    if groupname not in groups.keys():
        return "Group " + groupname + " does not exist"
    groups[groupname].members.append(user)
    return "User " + user + " has been added to group " + groupname, recipient


def saveconfig():
    configfile = open("config/servers", "w")
    for host, serverobject in servers.items():
        configfile.write(serverobject.__str__() + '\n')
    configfile = open("config/groups", "w")
    for groupname, groupobject in groups.items():
        configfile.write(groupobject.__str__() + '\n')


def groupadd(groupname, creator):
    if groupname in groups:
        return False
    groups[groupname] = Group(groupname, creator, [creator])
    return True


def groupdel(groupname, executor):
    global groups
    if groupname not in groups:
        return False
    group = groups[groupname]
    if group.owner == executor:
        del groups[groupname]
        return True
    return False