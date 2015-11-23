__author__ = 'Harald'

from group import Group


def readgroups():
    groups = {}
    with open('config/groups', 'r') as file:
        for line in file:
            if line.find('#') == 0:
                continue
            splitindex = line.find(':')
            groupident = [x.strip() for x in line[:splitindex].split(' ')]
            groupMembers = [x.strip() for x in line[splitindex + 1:].split(' ')]
            groups[groupident[0]] = Group(groupident[0], groupident[1], groupMembers)
    return groups


# read servers
def readservers():
    servers = {}
    with open('config/servers', 'r') as file:
        for line in file:
            if line.find('#') == 0:
                continue
            split = line.find(':')
            servername = line[:split]
            data = [x.strip() for x in line[split + 1:].split(',')]
            servers[servername] = data
    return servers


servers = readservers()
groups = readgroups()


def addusertogroup(user, groupname, recipient):
    if groupname not in groups.keys():
        return "Group " + groupname + " does not exist"
    groups[groupname].members.append(user)
    return "User " + user + " has been added to group " + groupname, recipient


def saveconfig():
    configfile = open("config/servers", "w")
    for host, serverdata in servers.items():
        newline = host + ": "
        for datapiece in serverdata:
            newline += datapiece + ', '
        configfile.write(newline[:-2] + '\n')
    configfile = open("config/groups", "w")
    for groupname, groupobject in groups.items():
        newline = groupname + ", " + groupobject.owner + ": "
        for member in groupobject.members:
            newline += member + ", "
        configfile.write(newline[:-2] + '\n')