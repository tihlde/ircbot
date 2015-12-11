# coding: utf-8
__author__ = 'Harald Floor Wilhelmsen'

from group import Group
from server import Server


class Dataobject(object):

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
            if not line:
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
    gottengroup = getdictelement(groupname, groups)
    if not gottengroup:
        return 'Group ' + groupname + ' does not exist'
    gottengroup.members.append(user)
    return 'User ' + user + ' has been added to group ' + groupname, recipient


def saveconfig():
    configfile = open('config/servers', 'w')
    for host, serverobject in servers.items():
        configfile.write(serverobject.__str__() + '\n')
    configfile = open('config/groups', 'w')
    for groupname, groupobject in groups.items():
        configfile.write(groupobject.__str__() + '\n')


def groupadd(args):
    executer = args[0]
    groupname = args[1]
    gottengroup = getdictelement(args[1], groups)
    if gottengroup:
        return 'Group ' + groupname + ' already exists'
    groups[groupname] = Group(groupname, executer, [executer])
    return 'Group ' + groupname + ' created'


def groupdel(args):
    executer = args[0]
    groupname = args[1]
    gottengroup = getdictelement(groupname, groups)
    if not gottengroup:
        return 'Group ' + groupname + ' does not exist'
    if gottengroup.owner.lower() == executer.lower():
        del groups[gottengroup.groupname]
        return 'Group ' + groupname + ' deleted'
    return 'You must be the owner of a group to delete it'


def groupmemberadd(args):
    executer = args[0]
    groupname = args[1]
    newmember = args[2]
    gottengroup = getdictelement(groupname, groups)
    if not gottengroup:
        return 'Group ' + groupname + ' does not exist'
    if executer != gottengroup.owner and executer != newmember:
        return 'You must be the owner of a group to add someone other than yourself. ' + gottengroup.owner + ' is the owner of the group ' + groupname
    if getindexofarrayelement(newmember, gottengroup.members) != -1:
        return 'Member ' + newmember + ' is already a part of group ' + groupname
    gottengroup.members.append(newmember)
    return 'Member ' + newmember + ' has been added to the group ' + groupname


def groupmemberdel(args):
    executer = args[0]
    groupname = args[1]
    member = args[2]
    gottengroup = getdictelement(groupname, groups)
    if not gottengroup:
        return 'Group ' + groupname + ' does not exist'
    executer = executer.lower()
    if executer == gottengroup.owner.lower() and executer == member.lower():
        return 'You cannot remove yourself from a group while you are still the owner, use .groupownerset to set a new owner'
    if executer != gottengroup.owner.lower() and executer != member.lower():
        return 'You must be the owner of a group to remove someone other than yourself'
    memberindex = getindexofarrayelement(member, gottengroup.members)
    if memberindex != -1:
        del gottengroup.members[memberindex]
        return 'Member ' + member + ' has been removed from the group ' + groupname
    return 'Member ' + member + ' does not exist in group ' + groupname


def grouplist(args):
    return ' '.join(group for group in groups)


def groupmemberlist(args):
    groupname = args[1]
    gottengroup = getdictelement(groupname, groups)
    if not gottengroup:
        return 'Group ' + groupname + ' does not exist'
    return ' -' + ' -'.join(member for member in gottengroup.members)


def groupownerset(args):
    return 'command not supported yet'


def serveradd(args):
    executer = args[0]
    hostname = args[1]
    prettyname = args[2]
    statusgroup = args[3]
    notifygroup = args[4]
    gottenserver = getdictelement(hostname, servers)
    if gottenserver:
        return 'Hostname ' + hostname + ' already exists'
    gottengroup = getdictelement(notifygroup, groups)
    if not gottengroup:
        return 'Group ' + notifygroup + ' does not exist'
    servers[hostname.lower()] = Server(hostname.lower(), executer, prettyname, statusgroup,
        notifygroup)
    return 'Server ' + hostname + ' added'


def serverdel(args):
    executer = args[0]
    hostname = args[1]
    gottenserver = getdictelement(hostname, servers)
    if not gottenserver:
        return 'Hostname ' + hostname + ' does not exist'
    if gottenserver.owner != executer:
        return 'You must be the creator of a server to delete it. Current owner is -' + gottenserver.owner
    del servers[gottenserver.hostname]
    return 'Server ' + hostname + ' deleted'


def serverlist(args):
    msg = 'Servers:'
    for hostname in servers.keys():
        msg += '  ' + hostname
    return msg


def serverdata(args):
    hostname = args[1]
    gottendata = getdictelement(hostname, servers)
    if not gottendata:
        return 'Hostname ' + hostname + ' does not exist'
    return gottendata.__str__()


def servernameset(args):
    return 'command not supported yet'


def servernotifysetset(args):
    return 'command not supported yet'


def serverstatusset(args):
    return 'command not supported yet'


def getdictelement(get, dict):
    for key, value in dict.items():
        if get.lower() == key.lower():
            return value
    return None


def getindexofarrayelement(get, array):
    i = 0
    for element in array:
        if element.lower() == get.lower():
            return i
        i += 1
    return -1