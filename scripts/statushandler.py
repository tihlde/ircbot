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

newStatuses = {}
oldStatuses = {}


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
    status = getstatus(host)
    newStatuses[host] = status
    oldStatuses[host] = status


def getserverstatus(statusgroup, nick):
    msg = ''
    for host, value in ch.servers.items():
        if ch.servers[2].find(statusgroup) != -1:
            msg += host + ' ' + newStatuses[host] + '  '
    return msg + "Last update: " + lastupdate



def threadpings():
    for key in newStatuses:
        newStatuses[key] = getstatus(key)
    lastupdate = time.localtime()


def updatestatuses():
    t = threading.Thread(target=threadpings, args=())
    t.daemon = True
    t.start()


def minutewarning():
    msgs = {}
    for i in range(len(newStatuses)):
        msg = ''
        newstatus = newStatuses[i]
        oldstatus = oldStatuses[i]
        if newstatus[0] != oldstatus[0]:  # status has changed
            oldstatus[0] = newstatus[0]
            msg += newstatus[2] + ' er nå ' + newstatus[0] + '  '
        if len(msg) > 0:
            for name in newstatus[4]:
                msgs[name] = msg
    return msgs


def midnightreminder():
    msgs = {}
    for i in range(len(newStatuses)):
        msg = ''
        newstatus = newStatuses[i]
        if newstatus[0].find(downStatus) != -1:  # status indicates it is down
            msg += newstatus[2] + ' er ' + newstatus[0] + '  '
        if len(msg) > 0:
            for name in newstatus[4]:
                msgs[name] = msg
    return msgs


def update():
    minute = time.strftime('%M')
    global updateMinute
    if minute != updateMinute:
        updatestatuses()
        minutewarning()
        updateMinute = minute

    day = time.strftime('%d')
    global updateDay
    if day != updateDay:
        midnightreminder()
        updateDay = day


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