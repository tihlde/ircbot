# coding: utf-8
__author__ = 'Harald'

from group import Group


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
            ident = striplist(line[:splitindex].split(' '))
            data = striplist(line[splitindex + 1:].split(' '))
            dataobjects.append(Dataobject(ident, data))
    return dataobjects


def readgroups():
    groups = {}
    readfile = readdata('config/groups')
    for dataobject in readfile:
        groups[dataobject.ident[0]] = Group(dataobject.ident[0], dataobject.ident[1], dataobject.data)
    return groups


# read servers
def readservers():
    servers = {}
    with open('config/servers', 'r') as file:
        for line in file:
            if line.find('#') == 0 or line == '':
                continue
            split = line.find(':')
            servername = line[:split]
            data = [x.strip(' ') for x in (line[split + 1:].split(','))]
            servers[servername] = data
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
        configfile.write(serverobject + '\n')
    configfile = open("config/groups", "w")
    for groupname, groupobject in groups.items():
        configfile.write(groupobject + '\n')