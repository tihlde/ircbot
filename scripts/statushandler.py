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

commands = ['getstatus', 'gs',
            'groupadd', 'ga',
            'groupdel', 'gd',
            'grouplist', 'gls',
            'groupmemberadd', 'gma',
            'groupmembderdel', 'gmd',
            'groupmemberlist', 'gmls',
            'groupownerset', 'gos',
            'serveradd', 'sa',
            'serverdel', 'sd',
            'servernameset', 'sns',
            'servernotifyset', 'sngs',
            'serverstatusset', 'ssgs',
            'ping'
            ]


def getstatus(hostname):
    if os.system('ping -c 1 -i 0.2 ' + hostname) == 0:
        return upStatus
    else:
        return downStatus


for host, serverdata in ch.servers.items():
    serverdata.status = getstatus(host)


def getserverstatus(statusgroup, nick):
    msg = ''
    for host, serverdata in ch.servers.items():
        if ch.servers[2].find(statusgroup) != -1:
            msg += host + ' ' + serverdata.status + '  '
    return msg + "Last update: " + lastupdate


updatechanges = []


def minuteupdate():
    for host, serverdata in ch.servers.items():
        newstatus = getstatus(host)
        if newstatus != serverdata.status:
            serverdata.status = newstatus
            updatechanges.append([serverdata, newstatus])
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
        if command == 'getstatus' or command == 'gs':
            return readStatuses(args[0])

        elif command == 'groupadd' or command == 'ga':
            return ch.groupadd(args[0], executor)

        elif command == 'groupdel' or command == 'gd':
            return ch.groupdel(args[0], executor)

        elif command == 'grouplist' or command == 'gs':
            return ch.grouplist()

        elif command == 'groupmemberadd' or command == 'gma':
            return ch.groupmemberadd(args[0], executor, args[1])

        elif command == 'groupmemberdel' or command == 'gmd':
            return ch.groupmemberdel(args[0], executor, args[1])

        elif command == 'groupmemberlist' or command == 'gmls':
            return ch.groupmemberlist(args[0])

        elif command == 'groupownerset' or command == 'gos':
            return 'command not supported yet'

        elif command == 'serveradd' or command == 'sa':
            return ch.serveradd(args[0], executor, args[1], args[2], args[3])

        elif command == 'serverdel' or command == 'sd':
            return ch.serverdel(args[0], executor)

        elif command == 'serverlist' or command == 'sls':
            return ch.serverlist()

        elif command == 'serverdata' or command == 'sdt':
            return ch.serverdata(args[0])

        elif command == 'servernameset' or command == 'sns':
            return 'command not supported yet'

        elif command == 'servernotifyset' or command == 'sns':
            return 'command not supported yet'

        elif command == 'serverstatusset' or command == 'ssgs':
            return 'command not supported yet'

        elif command == 'ping':
            return ping(args[0])
        else:
            return 'Command ' + command + ' not supported. '

    except IndexError:
        return 'Incorrent number of arguments for command ' + command

def readStatuses(statusgroup):
    msg = statusgroup + ':'
    for hostname, serverdata in ch.servers.items():
        if serverdata.statusgroup == statusgroup:
            msg += '  ' + serverdata.prettyname + ": " + serverdata.status
    if len(msg) == len(statusgroup) + 1:
        msg = 'No registered servers have the statusgroup ' + statusgroup
    return msg

def ping(hostname):
    return hostname + ': ' + getstatus(hostname)

def savechanges():
    ch.saveconfig()