# coding: utf-8
__author__ = 'Harald Floor Wilhelmsen'

import threading
import os
import time

import confighandler as ch
from command import Command
from helpparser import Helpparser


upStatus = '\x033,1oppe\x03'
downStatus = '\x030,4NEDE\x03'

lastupdate = time.localtime()
updateMinute = time.strftime('%M')


def gethelp(args):
    command = args[1]
    if command not in commands:
        return 'No helpmessage exists for ' + command
    return commands[command].helpmsg


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


parser = Helpparser('helpmsg')

commands = {
    'help': Command(gethelp, parser.gethelp('help')),
    'getstatus': Command(readStatuses, parser.gethelp('getstatus')),
    'ping': Command(ping, parser.gethelp('ping'))
}
commands.update(commands.fromkeys(
    ['groupadd', 'ga'], Command(ch.groupadd, parser.gethelp('groupadd'))))
commands.update(commands.fromkeys(
    ['groupdel', 'gd'], Command(ch.groupdel, parser.gethelp('groupdel'))))
commands.update(commands.fromkeys(
    ['grouplist', 'gls'], Command(ch.grouplist, parser.gethelp('grouplist'))))
commands.update(commands.fromkeys(
    ['groupmemberadd', 'gma'], Command(ch.groupmemberadd, parser.gethelp('groupmemberadd'))))
commands.update(commands.fromkeys(
    ['groupmemberdel', 'gmd'], Command(ch.groupmemberdel, parser.gethelp('groupmemberdel'))))
commands.update(commands.fromkeys(
    ['groupmemberlist', 'gmls'], Command(ch.groupmemberlist, parser.gethelp('groupmemberlist'))))
commands.update(commands.fromkeys(
    ['groupownerset', 'gos'], Command(ch.groupownerset, parser.gethelp('groupownerset'))))
commands.update(commands.fromkeys(
    ['serveradd', 'sa'], Command(ch.serveradd, parser.gethelp('serveradd'))))
commands.update(commands.fromkeys(
    ['serverdel', 'sd'], Command(ch.serverdel, parser.gethelp('serverdel'))))
commands.update(commands.fromkeys(
    ['serverlist', 'sls'], Command(ch.serverlist, parser.gethelp('serverlist'))))
commands.update(commands.fromkeys(
    ['serverdata', 'sdt'], Command(ch.serverdata, parser.gethelp('serverdata'))))
commands.update(commands.fromkeys(
    ['servernameset', 'sns'], Command(ch.servernameset, parser.gethelp('servernameset'))))
commands.update(commands.fromkeys(
    ['servernotifyset', 'sngs'], Command(ch.servernotifysetset, parser.gethelp('servernotifyset'))))
commands.update(commands.fromkeys(
    ['serverstatusset', 'ssgs'], Command(ch.serverstatusset, parser.gethelp('serverstatusset'))))

parser = None  # parse is no longer needed


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


def executecommand(command, args, executor):
    try:
        command = command.lower()
        if command not in commands:
            return 'Invalid command ' + command
        args.insert(0, executor)
        return commands[command].execute(args)

    except IndexError:
        return 'Incorrent number of arguments for command ' + command


def savechanges():
    ch.saveconfig()