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
            data = [x.strip() for x in line.split(',')]
            print("DATA")
            print(data)
            print('')
            servers[data[0]] = data
    return servers


def saveconfig(servers):
    configfile = open("servers", "w")
    for _status in servers:
        newline = _status[1] + ',' + _status[2] + ',' + _status[3] + ',['
        for name in _status[4]:
            newline += name + ','
        newline = newline[:-1] + ']'
        configfile.write(newline + '\n')