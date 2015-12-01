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
    if not strindict(groupname, groups):
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
    if strindict(groupname, groups):
        return "Group " + groupname + " already exists"
    groups[groupname] = Group(groupname, creator, [creator])
    return "Group " + groupname + " created"


def groupdel(groupname, executer):
    global groups
    if strindict(groupname, groups):
        return "Group " + groupname + " does not exist"
    group = groups[groupname]
    if group.owner.lower() == executer.lower():
        del groups[groupname]
        return "Group " + groupname + " deleted"
    return "You must be the owner of a group to delete it"


def groupmemberadd(groupname, executer, newmember):
    if not strinarray(groupname, groups):
        return "Group " + groupname + " does not exist"
    group = groups[groupname]
    if executer != group.owner and executer != newmember:
        return "You must be the owner of a group to add someone other than yourself. " + group.owner + " is the owner of the group " + groupname
    if strinarray(newmember, group.members):
        return "Member " + newmember + " is already a part of group " + groupname
    group.members.append(newmember)
    return "Member " + newmember + " has been added to the group " + groupname


def groupmemberdel(groupname, executer, member):
    if not strindict(groupname, groups):
        return "Group " + groupname + " does not exist"
    group = groups[groupname]
    executer = executer.lower()
    if executer == group.owner.lower() and executer == member.lower():
        return "You cannot remove yourself from a group while you are still the owner, use .groupownerset to set a new owner"
    if executer != group.owner.lower() and executer != member.lower():
        return "You must be the owner of a group to remove someone other than yourself"
    if strinarray(member, group.members):
        group.members.remove(member)
        return "Member " + member + " has been removed from the group " + groupname
    return "Member " + member + " does not exist in group " + groupname


def grouplist():
    string = ''
    for groupname, group in groups.items():
        string += groupname + ' '
    return string


def groupmemberlist(groupname):
    if not strindict(groupname, groups):
        return "Group " + groupname + " does not exist"
    string = ''
    for member in groups[groupname].members:
        string += "-" + member + " "
    return string


def serveradd(hostname, executor, prettyname, statusgroup, notifygroup):
    hostname = hostname.lower()
    if strindict(hostname, servers):
        return "Hostname " + hostname + " already exists"
    if not strindict(notifygroup, groups):
        return "Group " + notifygroup + " does not exist"
    servers[hostname] = Server(hostname, executor, prettyname, statusgroup, notifygroup)
    return "Server " + hostname + " added"


def serverdel(hostname, executor):
    hostname = hostname.lower()
    if not strindict(hostname, servers):
        return "Hostname " + hostname + " does not exist"
    server = servers[hostname]
    if server.owner != executor:
        return "You must be the creator of a server to delete it. Current owner is -" + server.owner
    del servers[hostname]
    return "Server " + hostname + " deleted"


def serverlist():
    msg = 'Servers:'
    for hostname in servers.keys():
        msg += '  ' + hostname
    return msg


def serverdata(hostname):
    if not strindict(hostname, servers):
        return "Hostname " + hostname + " does not exist"
    return servers[hostname].__str__()


def strinarray(string, array):
    return string.lower() in (element.lower() for element in array)

def strindict(string, dict):
    return string.lower() in (key.lower() for key in dict.keys())