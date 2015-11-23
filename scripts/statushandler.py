# coding: utf-8
__author__ = 'Harald'

import threading
import os
import time

import bot
import confighandler as ch


upStatus = '\x033,1oppe\x03'
downStatus = '\x030,4NEDE\x03'

lastupdate = time.localtime()
updateMinute = time.strftime('%M')
updateDay = time.strftime('%d')

newStatuses = {}  # format: hostname, status
oldStatuses = {}


def getstatus(hostname):
    if os.system('ping -c 1 -i 0.2 ' + hostname + '.tihlde.org') == 0:
        return upStatus
    else:
        return downStatus


for host, serverdata in ch.servers.items():
    status = getstatus(host)
    newStatuses[host] = status
    oldStatuses[host] = status


def sendserverstatus(statusgroup, nick):
    msg = ''
    for host, value in ch.servers.items():
        if ch.servers[2].find(statusgroup) != -1:
            msg += host + ' ' + newStatuses[host] + '  '
    if len(msg) > 0:
        bot.sendtext(msg + "Last update: " + lastupdate, nick)


def threadpings():
    for key in newStatuses:
        newStatuses[key] = getstatus(key)
    lastupdate = time.localtime()


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
            msg += newstatus[2] + ' er nå ' + newstatus[0] + '  '
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
    ch.saveconfig()