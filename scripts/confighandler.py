# coding: utf-8
__author__ = 'Harald Floor Wilhelmsen'

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
        servers[dataobject.ident[0]] = Server(dataobject.ident[0], dataobject.ident[1],
                                              dataobject.data[0], dataobject.data[1],
                                              dataobject.data[2])
    return servers


groups = readgroups()
servers = readservers()


def addusertogroup(user, groupname, recipient):
    gottengroup = getElement(groupname, groups)
    if gottengroup == None:
        return "Group " + groupname + " does not exist"
    gottengroup.members.append(user)
    return "User " + user + " has been added to group " + groupname, recipient


def saveconfig():
    configfile = open("config/servers", "w")
    for host, serverobject in servers.items():
        configfile.write(serverobject.__str__() + '\n')
    configfile = open("config/groups", "w")
    for groupname, groupobject in groups.items():
        configfile.write(groupobject.__str__() + '\n')


def groupadd(groupname, creator):
    gottengroup = getElement(groupname, groups)
    if gottengroup != None:
        return "Group " + groupname + " already exists"
    groups[groupname] = Group(groupname, creator, [creator])
    return "Group " + groupname + " created"


def groupdel(groupname, executer):
    gottengroup = getElement(groupname, groups)
    if gottengroup == None:
        return "Group " + groupname + " does not exist"
    if gottengroup.owner.lower() == executer.lower():
        del groups[gottengroup.groupname]
        return "Group " + groupname + " deleted"
    return "You must be the owner of a group to delete it"


def groupmemberadd(groupname, executer, newmember):
    gottengroup = getElement(groupname, groups)
    if gottengroup == None:
        return "Group " + groupname + " does not exist"
    if executer != gottengroup.owner and executer != newmember:
        return "You must be the owner of a group to add someone other than yourself. " + gottengroup.owner + " is the owner of the group " + groupname
    gottenmember = getElement(newmember, gottengroup.members)
    if gottenmember != None:
        return "Member " + newmember + " is already a part of group " + groupname
    gottengroup.members.append(newmember)
    return "Member " + newmember + " has been added to the group " + groupname


def groupmemberdel(groupname, executer, member):
    gottengroup = getElement(groupname, groups)
    if gottengroup == None:
        return "Group " + groupname + " does not exist"
    executer = executer.lower()
    if executer == gottengroup.owner.lower() and executer == member.lower():
        return "You cannot remove yourself from a group while you are still the owner, use .groupownerset to set a new owner"
    if executer != gottengroup.owner.lower() and executer != member.lower():
        return "You must be the owner of a group to remove someone other than yourself"
    gottenmember = getElement(member, gottengroup.members)
    if gottenmember != None:
        gottengroup.members.remove(member)
        return "Member " + member + " has been removed from the group " + groupname
    return "Member " + member + " does not exist in group " + groupname


def grouplist():
    string = ''
    for groupname, group in groups.items():
        string += groupname + ' '
    return string


def groupmemberlist(groupname):
    gottengroup = getElement(groupname, groups)
    if gottengroup == None:
        return "Group " + groupname + " does not exist"
    string = ''
    for member in gottengroup.members:
        string += "-" + member + " "
    return string


def serveradd(hostname, executor, prettyname, statusgroup, notifygroup):
    gottenserver = getElement(hostname, servers)
    if gottenserver != None:
        return "Hostname " + hostname + " already exists"
    gottengroup = getElement(notifygroup, groups)
    if gottengroup == None:
        return "Group " + notifygroup + " does not exist"
    servers[hostname.lower()] = Server(hostname.lower(), executor, prettyname, statusgroup, notifygroup)
    return "Server " + hostname + " added"


def serverdel(hostname, executor):
    gottenserver = getElement(hostname, servers)
    if gottenserver != None:
        return "Hostname " + hostname + " does not exist"
    if gottenserver.owner != executor:
        return "You must be the creator of a server to delete it. Current owner is -" + gottenserver.owner
    del servers[gottenserver.hostname]
    return "Server " + hostname + " deleted"


def serverlist():
    msg = 'Servers:'
    for hostname in servers.keys():
        msg += '  ' + hostname
    return msg


def serverdata(hostname):
    gottendata = getElement(hostname, servers)
    if gottendata == None:
        return "Hostname " + hostname + " does not exist"
    return gottendata.__str__()


def getElement(get, dict):
    for key, value in dict.items():
        if get.lower() == key.lower():
            return value
    return None