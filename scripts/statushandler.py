# coding: utf-8
__author__ = 'Harald Floor Wilhelmsen'

import threading
import os
import time

import confighandler as ch


upStatus = '\x033,1oppe\x03'
downStatus = '\x030,4NEDE\x03'

lastupdate = time.localtime()
updateMinute = time.strftime('%M')
updateDay = time.strftime('%d')


def readStatuses(args):
    statusgroup = args[1]
    msg = statusgroup + ':'
    for hostname, serverdata in ch.servers.items():
        if serverdata.statusgroup.lower() == statusgroup.lower():
            msg += '  ' + serverdata.prettyname + ':' + serverdata.status
    if len(msg) == len(statusgroup) + 1:
        msg = 'No registered servers have the statusgroup ' + statusgroup
    return msg


def ping(args):
    hostname = args[1]
    return hostname + ': ' + getstatus(hostname)


helpmsgs = {
    'getstatus': 'Returns a string representing with the statuses of the servers in the given statusgroup.',
    'ping': 'Returns the status of the given hostname',
    'help': 'Privilege: A hash ("#") signifies a privilege, for example "#owner" would signify you must be the owner to execute the command. '
            + 'Format: A cash ("$") signifies the formatting of the arguments of the command.'
}
helpmsgs.update(helpmsgs.fromkeys(
    ['groupadd', 'ga'],
    'Adds a group with the given name. You are automatically added to the group and set as the owner. $groupname'))
helpmsgs.update(helpmsgs.fromkeys(
    ['groupdel', 'gd'],
    'Deletes the group with the given name. #owner'))
helpmsgs.update(helpmsgs.fromkeys(
    ['grouplist', 'gls'],
    'A list of the groups that exist'))
helpmsgs.update(helpmsgs.fromkeys(
    ['groupmemberadd', 'gma'],
    'Adds the given username to the given group. $groupname username'))
helpmsgs.update(helpmsgs.fromkeys(
    ['groupmemberdel', 'gmd'],
    'Removes the given user from the given group. $groupname username'))
helpmsgs.update(helpmsgs.fromkeys(
    ['groupmemberlist', 'gmls'],
    'Lists the members of the given group. $groupname'))
helpmsgs.update(helpmsgs.fromkeys(
    ['groupownerset', 'gos'],
    'Sets a new owner to the given group. #owner $groupname newowner'))
helpmsgs.update(helpmsgs.fromkeys(
    ['serveradd', 'sa'],
    'Adds a new server with the given data. $hostname prettyname statusgroup membergroup'))
helpmsgs.update(helpmsgs.fromkeys(
    ['serverdel', 'sa'],
    'Deletes the server with the given hostname. #owner'))
helpmsgs.update(helpmsgs.fromkeys(
    ['serverdata', 'sdt'],
    'Lists the data for the given server. $hostname'))
helpmsgs.update(helpmsgs.fromkeys(
    ['servernameset', 'sns'],
    'Sets a new name for the given server. #owner'))
helpmsgs.update(helpmsgs.fromkeys(
    ['servernotifyset', 'sngs'],
    'Sets the notifygroup of the given server. #owner $hostname newgroup'))
helpmsgs.update(helpmsgs.fromkeys(
    ['serverstatusset', 'ssgs'],
    'Sets the statugroup of the given server. #owner $hostname newgroup'))


def gethelp(args):
    command = args[1]
    if command not in helpmsgs:
        return 'No helpmessage exists for ' + command
    return helpmsgs[command]


commands = {
    'getstatus': readStatuses,
    'ping': ping,
    'help': gethelp
}
commands.update(commands.fromkeys(['groupadd', 'ga'], ch.groupadd))
commands.update(commands.fromkeys(['groupdel', 'gd'], ch.groupdel))
commands.update(commands.fromkeys(['grouplist', 'gls'], ch.grouplist))
commands.update(commands.fromkeys(['groupmemberadd', 'gma'], ch.groupmemberadd))
commands.update(commands.fromkeys(['groupmemberdel', 'gmd'], ch.groupmemberdel))
commands.update(commands.fromkeys(['groupmemberlist', 'gmls'], ch.groupmemberlist))
commands.update(commands.fromkeys(['groupownerset', 'gos'], ch.groupownerset))
helpmsgs.update(helpmsgs.fromkeys(['serveradd', 'sa'], ch.serveradd))
helpmsgs.update(helpmsgs.fromkeys(['serverdel', 'sd'], ch.serverdel))
commands.update(commands.fromkeys(['serverdata', 'sdt'], ch.serverdata))
commands.update(commands.fromkeys(['servernameset', 'sns'], ch.servernameset))
commands.update(commands.fromkeys(['servernotifyset', 'sngs'], ch.servernotifysetset))
commands.update(commands.fromkeys(['serverstatusset', 'ssgs'], ch.serverstatusset))


def getstatus(hostname):
    if os.system('ping -c 1 -i 0.2 ' + hostname) == 0:
        return upStatus
    else:
        return downStatus


for host, serverdata in ch.servers.items():
    serverdata.status = getstatus(host)

updatechanges = []


def minuteupdate():
    for host, serverdata in ch.servers.items():
        newstatus = getstatus(host)
        if newstatus != serverdata.status:
            serverdata.status = newstatus
            updatechanges.append(serverdata)
    global lastupdate
    lastupdate = time.localtime()


def threadupdate():
    t = threading.Thread(target=minuteupdate, args=())
    t.daemon = True
    t.start()


def getgroup(groupname):
    return ch.groups[groupname]


def update():
    minute = time.strftime('%M')
    global updateMinute
    if minute != updateMinute:
        threadupdate()
        updateMinute = minute

        # day = time.strftime('%d')
        # global updateDay
        # if day != updateDay:
        #     midnightreminder()
        #     updateDay = day


def executecommand(command, args, executor):
    try:
        command = command.lower()
        if command not in commands:
            return 'Invalid command ' + command
        args.insert(0, executor)
        return commands[command](args)

    except IndexError:
        return 'Incorrent number of arguments for command ' + command


def savechanges():
    ch.saveconfig()