# coding: utf-8
__author__ = 'Harald'

import socket
import time
import os
import threading
import atexit

import serial

discoActive = True
maxDiscoTime = 3000
standardDiscoTime = 20

updateMinute = time.strftime('%M')
updateDay = time.strftime('%d')

upStatus = '\x033,1oppe\x03'
downStatus = '\x030,4NEDE\x03'

ser = serial.Serial('/dev/ttyACM0', 9600)

server = 'irc.freenode.net'
channel = '#tihlde-drift'
botnick = 'hal-9001'
password = open('pw').read()
mods = []


def updatemods(names):
    print('MSG BEFORE SPLIT')
    print(names)
    namelist = names.split(' ')
    print('MSG AFTER SPLIT')
    print(namelist)
    mods[:] = []
    for name in namelist:
        if name.find('@') != -1 and name.find('ChanServ') == -1:
            mods.append(name)
    print('MOD-LIST')
    print(mods)


def getstatus(hostname):
    if os.system('ping -c 1 -i 0.2 ' + hostname + '.tihlde.org') == 0:
        return upStatus
    else:
        return downStatus

# read config
config = {}
with open('config', 'r') as file:
    for line in file:
        if line.find('#') == 0:
            continue
        data = [x.strip() for x in line.split(',')]
        print("DATA")
        print(data)
        print('')
        config[data[0]] = data

groups = {}
# read groups
with open('groups', 'r') as file:
    for line in file:
        if line.find('#') == 0:
            continue
        split = line.find(':')
        groupName = line[:split]
        groupMembers = [x.strip() for x in line[split + 1:].split(',')]
        print('GROUP')
        print(groupName)
        print(groupMembers)
        print()
        groups[groupName] = groupMembers

# create dicts
newStatuses = {}
oldStatuses = {}
for server in config:
    status = getstatus(server[0])
    newStatuses[server[0]] = status
    oldStatuses[server[0]] = status


def send(msg):
    msg += '\r\n'
    print('SENDING')
    print(msg)
    ircsock.send(msg)


def sendtext(msg, rec):
    send('PRIVMSG ' + rec + ' :' + msg)


def sendserverstatus(statusgroup, nick):
    msg = ''
    for host, value in config.items():
        if config[3].find(statusgroup) != -1:
            msg += value[1] + ' ' + newStatuses[host] + '  '
    sendtext(msg, nick)


def updatestatuses():
    t = threading.Thread(target=threadpings, args=())
    t.daemon = True
    t.start()


def threadpings():
    for key in newStatuses:
        newStatuses[key] = getstatus(key)


def minutewarning():
    msg = ''
    for i in range(len(newStatuses)):
        newstatus = newStatuses[i]
        oldstatus = oldStatuses[i]
        if newstatus[0] != oldstatus[0]:  # status has changed
            oldstatus[0] = newstatus[0]
            msg += newstatus[2] + ' er nå ' + newstatus[0] + '  '
        if len(msg) > 0:
            for name in newstatus[4]:
                send('PRIVMSG ' + name + ' face:' + msg)


def midnightreminder():
    msg = ''
    for key in oldStatuses:
        if oldStatuses[key].find(downStatus) != -1:
            if key.find('.') == -1:
                servername = key
            else:
                servername = key[:key.find('.')]
            msg += servername + ' ' + downStatus + '  '
    if len(msg) > 0:
        sendtext('Påminnelse ved midnatt: ' + msg)


def saveconfig():
    configfile = open("config", "w")
    for _status in newStatuses:
        newline = _status[1] + ',' + _status[2] + ',' + _status[3] + ',['
        for name in _status[4]:
            newline += name + ','
        newline = newline[:-1] + ']'
        configfile.write(newline + '\n')


def findname(text):
    return text[1:text.find('!')]


def ismod(name):
    return ('@' + name) in mods


def requestnames():
    send('NAMES #tihlde-drift')


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
send('USER ' + botnick + ' ' + botnick + ' ' + server + ' : pybot')
send('NICK ' + botnick)

send('JOIN ' + channel + ' ' + password)  # join channel

while 1:
    ircmsg = ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip('\n')  # removing linebreaks.

    sender = findname(ircmsg)

    if ircmsg.find('.freenode.net') != -1:
        msgServer = ircmsg[1:ircmsg.find('.freenode.net')]

    if len(ircmsg) > 0:
        print('RECEIVED')
        print(ircmsg)  # print received message

    statusIndex = ircmsg.find('.status(')
    if statusIndex != -1:  # Respond to .serverstatus
        sendserverstatus(ircmsg[ircmsg.find('(') + 1: ircmsg.find(')')], sender)

    # Make sure the message is in specified channel and not a private msg
    if ircmsg.find('PRIVMSG ' + channel) != -1:

        if ircmsg.find('.updatemods') != -1:  # respond to .updatemods
            requestnames()

        if ismod(sender):  # if sender is a mod
            if ircmsg.find('.discodeactivate') != -1:
                discoActive = False
                sendtext('Discotime deactivated', channel)
            elif ircmsg.find('.discoreactivate') != -1:
                discoActive = True
                sendtext('Discotime reactivated', channel)
            try:
                if discoActive and ircmsg.find('.discotime') != -1:
                    try:
                        discoTime = int(
                            ircmsg[ircmsg.find('(') + 1: ircmsg.find(')')])
                    except ValueError:
                        discoTime = standardDiscoTime
                    if discoTime > maxDiscoTime:
                        discoTime = maxDiscoTime
                    print('Discotime for ' + str(discoTime) + '!')
                    ser.write(str.encode(str(discoTime)))
                    print(ser.read())
                else:
                    ser.write(b'0')
            except serial.serialutil.SerialException:
                print('Device unplugged or wrong device used')

    filterString = ':' + msgServer \
                   + '.freenode.net 353 hal-9001 @ #tihlde-drift :'
    # if this message is a name-list. .updatemods has just been called
    isNameMsg = ircmsg.find(filterString) != -1
    isNotJoinMsg = ircmsg.find(
        ':' + msgServer + '.freenode.net 333 hal-9001 #tihlde-drift') == -1
    if isNameMsg and isNotJoinMsg:
        nsStart = len(filterString)
        nsEnd = ircmsg.find(
            ':' + msgServer
            + '.freenode.net 366 hal-9001 #tihlde-drift :End of /NAMES list.')
        nameString = ircmsg[nsStart:nsEnd]

        nameString = nameString.replace('\r\n:' + msgServer + '.freenode.net',
                                        '')
        print('NAMESTRING')
        print(nameString)
        updatemods(nameString)

    if ircmsg.find('PING :') != -1:  # respond to pings
        send('PONG ' + ircmsg[ircmsg.find(':') + 1])

    minute = time.strftime('%M')
    if minute != updateMinute:
        updatestatuses()
        minutewarning()
        updateMinute = minute

    day = time.strftime('%d')
    if day != updateDay:
        midnightreminder()
        updateDay = day


@atexit.register
def exitbot():
    print('Shutting down bot...')
    saveconfig()
    print('Config saved')
    send('PART ' + channel)
    print('Channel left')
    send('QUIT')
    print('Quit server')
    ircsock.close()
    print('Socket closed')
    print('*** Shutdown complete ***')
