__author__ = 'Harald'

import threading
import os
import time

import bot
import confighandler as ch


upStatus = '\x033,1oppe\x03'
downStatus = '\x030,4NEDE\x03'

servers = ch.readservers()
groups = ch.readgroups()
newStatuses = {}  # format: hostname, status
oldStatuses = {}


def getstatus(hostname):
    if os.system('ping -c 1 -i 0.2 ' + hostname + '.tihlde.org') == 0:
        return upStatus
    else:
        return downStatus


for server in servers:
    status = getstatus(server[0])
    newStatuses[server[0]] = status
    oldStatuses[server[0]] = status


def sendserverstatus(statusgroup, nick):
    msg = ''
    for host, value in servers.items():
        if servers[3].find(statusgroup) != -1:
            msg += value[1] + ' ' + newStatuses[host] + '  '
    bot.sendtext(msg, nick)


def threadpings():
    for key in newStatuses:
        newStatuses[key] = getstatus(key)


def updatestatuses():
    t = threading.Thread(target=threadpings, args=())
    t.daemon = True
    t.start()


def minutewarning():
    for i in range(len(newStatuses)):
        msg = ''
        newstatus = newStatuses[i]
        oldstatus = oldStatuses[i]
        if newstatus[0] != oldstatus[0]:  # status has changed
            oldstatus[0] = newstatus[0]
            msg += newstatus[2] + ' er n� ' + newstatus[0] + '  '
        if len(msg) > 0:
            for name in newstatus[4]:
                bot.sendtext(msg, name)


def midnightreminder():
    for i in range(len(newStatuses)):
        msg = ''
        newstatus = newStatuses[i]
        if newstatus[0].find(downStatus) != -1:  # status indicates it is down
            msg += newstatus[2] + ' er ' + newstatus[0] + '  '
        if len(msg) > 0:
            for name in newstatus[4]:
                bot.sendtext(msg, name)


updateMinute = time.strftime('%M')
updateDay = time.strftime('%d')


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


def savechanges():
    ch.saveconfig(servers)

    # def parsemsg(msg):