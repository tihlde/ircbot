# coding: utf-8
__author__ = 'Harald'

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
            'groupmemberadd', 'gma',
            'groupmembderdel', 'gmd'
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
    for host, serverdata in ch.servers:
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
    if command == 'getstatus' or command == 'gs':
        return 'command not supported yet'

    elif command == 'groupadd' or command == 'ga':
        return ch.groupadd(args[0], executor)

    elif command == 'groupdel' or command == 'gd':
        return ch.groupdel(args[0], executor)

    elif command == 'grouplist' or command == 'gs':
        return 'command not supported yet'

    elif command == 'groupmemberadd' or command == 'gma':
        return ch.groupmemberadd(args[0], executor, args[1])

    elif command == 'groupmemberdel' or command == 'gmd':
        return ch.groupmemberdel(args[0], executor, args[1])

    elif command == 'groupmemberlist' or command == 'gmls':
        return 'command not supported yet'

    elif command == 'groupownerset' or command == 'gos':
        return 'command not supported yet'

    elif command == 'serveradd' or command == 'sa':
        return 'command not supported yet'

    elif command == 'serverdel' or command == 'sd':
        return 'command not supported yet'

    elif command == 'servernameset' or command == 'sns':
        return 'command not supported yet'

    elif command == 'servernotifyset' or command == 'sns':
        return 'command not supported yet'

    elif command == 'serverstatusset' or command == 'ssgs':
        return 'command not supported yet'
        # elif command == '' or command == '':


def savechanges():
    ch.saveconfig()