# coding: utf-8
__author__ = 'Harald'

import socket
import time
import os

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
            if name.find('\r\n:leguin.freenode.net') != -1:
                name = name.strip('\r\n:leguin.freenode.net')
            mods.append(name)
    print('MOD-LIST')
    print(mods)


def getStatus(hostname):
    if os.system('ping -c 1 ' + hostname + '.tihlde.org') == 0:
        return '\x033,1oppe\x03'
    else:
        return '\x030,4NEDE\x03'


statuses = {
    'colargol': getStatus('colargol'),
    'fantorangen': getStatus('fantorangen'),
    'odin': getStatus('odin'),
    'coastguard': getStatus('coastguard'),
    'handymanny': getStatus('handymanny'),
    'balthazar': getStatus('balthazar'),
    'thor': getStatus('thor'),
    'vcenter.nerdvana': getStatus('vcenter.nerdvana'),
    'bashful.nerdvana': getStatus('bashful.nerdvana'),
    'dopey.nerdvana': getStatus('dopey.nerdvana'),
    'grumpy.nerdvana': getStatus('grumpy.nerdvana'),
    'sneezy.nerdvana': getStatus('sneezy.nerdvana'),
    'sleepy.nerdvana': getStatus('sleepy.nerdvana')
}


def send(msg):
    msg += '\r\n'
    print('SENDING')
    print(msg)
    ircsock.send(msg)


def sendText(msg):
    send('PRIVMSG ' + channel + ' :' + msg)


def sendServerStatuses():
    sendText('colargol: ' + statuses['colargol'] +
             '  fantorangen: ' + statuses['fantorangen'] +
             '  odin: ' + statuses['odin'] +
             '  coastguard: ' + statuses['coastguard'] +
             '  handymanny: ' + statuses['handymanny'] +
             '  balthazar: ' + statuses['balthazar'] +
             '  thor: ' + statuses['thor'])


def sendNerdvanaStatuses():
    sendText('vcenter: ' + statuses['vcenter.nerdvana'] +
             '  bashful: ' + statuses['bashful.nerdvana'] +
             '  grumpy: ' + statuses['grumpy.nerdvana'] +
             '  dopey: ' + statuses['dopey.nerdvana'] +
             '  sleepy: ' + statuses['sleepy.nerdvana'] +
             '  sneezy: ' + statuses['sneezy.nerdvana'])


def updateStatuses():
    msg = ''
    for key in statuses:
        oldStatus = statuses[key]
        newStatus = getStatus(key)
        statuses[key] = newStatus
        if oldStatus != newStatus:
            msg += key + ' er nå ' + newStatus + '  '
    if len(msg) > 0:
        sendText('Endringer i status siste minutt: ' + msg)


def warnIfDown():
    msg = ''
    for key in statuses:
        if statuses[key].find('NEDE') != -1:
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
                else:
                    ser.write(b'0')
            except serial.serialutil.SerialException:
                print('Device unplugged or wrong device used')

    # if this message is a name-list
    filterString = ':leguin.freenode.net 353 hal-9001 @ #tihlde-drift :'
    if ircmsg.find(filterString) != -1 and ircmsg.find(
            ':leguin.freenode.net 333 hal-9001 #tihlde-drift') == -1:
        nameString = ircmsg[len(filterString):ircmsg.find(
            ':leguin.freenode.net 366 hal-9001 #tihlde-drift :End of /NAMES list.')]
        nameString = ircmsg.strip(':leguin.freenode.net 353 hal-9001 @ #tihlde-drift :')
        nameString = nameString.strip('\r\n:leguin.freenode.net')
        print('NAMESTRING')
        print(nameString)
        updateMods(nameString)

    if ircmsg.find('PING :') != -1:  # respond to pings
        send('PONG ' + ircmsg[ircmsg.find(':') + 1])

    minute = time.strftime('%M')
    if minute != updateMinute:
        updateStatuses()
        updateMinute = minute

    day = time.strftime('%d')
    if day != updateDay:
        updateStatuses()
        warnIfDown()
        updateDay = day