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
        return "Group " + groupname + " does not exist"
    groups[groupname] = Group(groupname, creator, [creator])
    return "Group " + groupname + " created"


def groupdel(groupname, executer):
    global groups
    if groupname not in groups:
        return "Group " + groupname + " does not exist"
    group = groups[groupname]
    if group.owner == executer:
        del groups[groupname]
        return "Group " + groupname + " deleted"
    return "You must be the owner of a group to delete it"


def groupmemberadd(groupname, executer, newmember):
    if groupname not in groups:
        return "Group " + groupname + " does not exist"
    group = groups[groupname]
    if executer != group.owner and executer != newmember:
        return "You must be the owner of a group to add someone other than yourself. " + group.owner + " is the owner of the group " + groupname
    if newmember in group.members:
        return "Member " + newmember + " is already a part of group " + groupname
    group.members.append(newmember)
    return "Member " + newmember + " has been added to the group " + groupname

def groupmemberdel(groupname, executer, member):
    if groupname not in groups:
        return "Group " + groupname + " does not exist"
    group = groups[groupname]
    if executer == group.owner and executer == member:
        return "You cannot remove yourself from a group while you are still the owner, use .groupownerset to set a new owner"
    if executer != group.owner and executer != member:
        return "You must be the owner of a group to remove someone other than yourself"
    if member in group.members:
        group.members.remove(member)
    return "Member " + member + " has been removed from the group " + groupname