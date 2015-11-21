__author__ = 'Harald'


def readgroups():
    groups = {}
    with open('config/groups', 'r') as file:
        for line in file:
            if line.find('#') == 0:
                continue
            split = line.find(':')
            groupName = line[:split]
            groupMembers = [x.strip() for x in line[split + 1:].split(',')]
            groups[groupName] = groupMembers
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


def saveconfig():
    configfile = open("config/servers", "w")
    for host, serverdata in servers.items():
        newline = host + ": "
        for datapiece in serverdata:
            newline += datapiece + ', '
        newline = newline[:-2] + ']'
        configfile.write(newline + '\n')
    configfile = open("config/groups", "w")
    for groupname, groupmembers in groups.items():
        newline = groupname + ": "
        for member in groupmembers:
            newline += member + ", "
        configfile.write(newline[:-2] + '\n')