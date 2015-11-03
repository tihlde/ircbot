# coding: utf-8
__author__ = 'Harald'

import socket
import time
import os
import threading
import copy

import serial


discoActive = True
maxDiscoTime = 3000
standardDiscoTime = 20

updateMinute = time.strftime('%M')
updateDay = time.strftime('%d')

ser = serial.Serial('/dev/ttyACM0', 9600)

server = 'irc.freenode.net'
channel = '#tihlde-drift'
botnick = 'hal-9001'
password = open('pw').read()
mods = []


def updateMods(names):
    print('MSG BEFORE SPLIT')
    print(names)
    nameList = names.split(' ')
    print('MSG AFTER SPLIT')
    print(nameList)
    mods[:] = []
    for name in nameList:
        if name.find('@') != -1 and name.find('ChanServ') == -1:
            mods.append(name)
    print('MOD-LIST')
    print(mods)


def getStatus(hostname):
    if os.system('ping -c 1 -i 0.2 ' + hostname + '.tihlde.org') == 0:
        return '\x033,1oppe\x03'
    else:
        return '\x030,4NEDE\x03'


newStatuses = [[]]


def readServers():
    with open('servers') as file:
        for line in file:
            if line.find('#') != -1:
                continue
            data = line[:line.find('[')].split(',')
            print("Data")
            print(data)
            data.append(line[line.find('[') + 1:len(line) - 1].split(','))
            print("Data with users")
            print(data)
            newStatuses.append(data)


readServers()
oldStatuses = copy.deepcopy(newStatuses)


def send(msg):
    msg += '\r\n'
    print('SENDING')
    print(msg)
    ircsock.send(msg)


def sendText(msg):
    send('PRIVMSG ' + channel + ' :' + msg)


def sendServerStatuses():
    sendText('colargol: ' + oldStatuses['colargol'] +
             '  fantorangen: ' + oldStatuses['fantorangen'] +
             '  odin: ' + oldStatuses['odin'] +
             '  coastguard: ' + oldStatuses['coastguard'] +
             '  handymanny: ' + oldStatuses['handymanny'] +
             '  balthazar: ' + oldStatuses['balthazar'] +
             '  thor: ' + oldStatuses['thor'])


def sendNerdvanaStatuses():
    sendText('vcenter: ' + oldStatuses['vcenter.nerdvana'] +
             '  grumpy: ' + oldStatuses['grumpy.nerdvana'] +
             '  dopey: ' + oldStatuses['dopey.nerdvana'] +
             '  sleepy: ' + oldStatuses['sleepy.nerdvana'] +
             '  sneezy: ' + oldStatuses['sneezy.nerdvana'])


def updateStatuses():
    t = threading.Thread(target=threadPings, args=())
    t.daemon = True
    t.start()


def threadPings():
    for key in newStatuses:
        newStatuses[key] = getStatus(key)


def minuteWarning():
    msg = ''
    for i in range(len(newStatuses)):
        newStatus = newStatuses[i]
        oldStatus = oldStatuses[i]
        if newStatus[0] != oldStatus[0]: # status has changed
            oldStatus[0] = newStatus[0]
            msg += newStatus[2] + ' er nå ' + newStatus[0] + '  '
        if len(msg) > 0:
            for name in newStatus[3]:
                send('PRIVMSG ' + name + ' :' + msg)


def midnightReminder():
    msg = ''
    for key in oldStatuses:
        if oldStatuses[key].find('NEDE') != -1:
            if key.find('.') == -1:
                serverName = key
            else:
                serverName = key[:key.find('.')]
            msg += serverName + ' \x030,4ER NEDE\x03  '
    if len(msg) > 0:
        sendText('Påminnelse ved midnatt: ' + msg)


def findName(ircmsg):
    return ircmsg[1:ircmsg.find('!')]


def isMod(name):
    return ('@' + name) in mods


def requestNames():
    send('NAMES #tihlde-drift')


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
send('USER ' + botnick + ' ' + botnick + ' ' + server + ' : pybot')
send('NICK ' + botnick)

send('JOIN ' + channel + ' ' + password)  # join channel

while 1:
    ircmsg = ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip('\n')  # removing linebreaks.

    if ircmsg.find('.freenode.net') != -1:
        msgServer = ircmsg[1:ircmsg.find('.freenode.net')]

    if len(ircmsg) > 0:
        print('RECEIVED')
        print(ircmsg)  # print received message

    # Make sure the message is in specified channel and not a private msg
    if ircmsg.find('PRIVMSG #tihlde-drift') != -1:

        if ircmsg.find('.serverstatus') != -1:  # Respond to .serverstatus
            sendServerStatuses()

        if ircmsg.find('.nerdvanastatus') != -1:  # Respond to .nerdvanastatus
            sendNerdvanaStatuses()

        if ircmsg.find('.updatemods') != -1:  # respond to .updatemods
            requestNames()

        if isMod(findName(ircmsg)):  # if sender is a mod
            if ircmsg.find('.discodeactivate') != -1:
                discoActive = False
                sendText('Discotime deactivated')
            elif ircmsg.find('.discoreactivate') != -1:
                discoActive = True
                sendText('Discotime reactivated')
            try:
                if discoActive and ircmsg.find('.discotime') != -1:
                    try:
                        discoTime = int(ircmsg[ircmsg.find('(') + 1: ircmsg.find(')')])
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

    filterString = ':' + msgServer + '.freenode.net 353 hal-9001 @ #tihlde-drift :'
    # if this message is a name-list. .updatemods has just been called
    isNameMsg = ircmsg.find(filterString) != -1
    isNotJoinMsg = ircmsg.find(':' + msgServer + '.freenode.net 333 hal-9001 #tihlde-drift') == -1
    if isNameMsg and isNotJoinMsg:
        nsStart = len(filterString)
        nsEnd = ircmsg.find(
            ':' + msgServer + '.freenode.net 366 hal-9001 #tihlde-drift :End of /NAMES list.')
        nameString = ircmsg[nsStart:nsEnd]

        nameString = nameString.replace('\r\n:' + msgServer + '.freenode.net', '')
        print('NAMESTRING')
        print(nameString)
        updateMods(nameString)

    if ircmsg.find('PING :') != -1:  # respond to pings
        send('PONG ' + ircmsg[ircmsg.find(':') + 1])

    minute = time.strftime('%M')
    if minute != updateMinute:
        updateStatuses()
        minuteWarning()
        updateMinute = minute

    day = time.strftime('%d')
    if day != updateDay:
        midnightReminder()
        updateDay = day
