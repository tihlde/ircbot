# coding: utf-8
__author__ = 'Harald'

import socket
import time
import os

import serial


discoActive = True
updateDay = time.strftime('%d')

ser = serial.Serial('/dev/ttyACM0', 9600)

server = 'irc.freenode.net'
channel = '#tihlde-drift'
botnick = 'hal-9001'
password = open('pw').read()
mods = []


def updateMods(names):
    print('MSG BEFORE SPLIT' + names)
    nameList = names.split(' ')
    print('MSG AFTER SPLIT' + nameList)
    mods[:] = []
    for name in names:
        if name.find('@') != -1:
            mods.append(name)
    print('MOD-LIST: ' + mods)


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
    ircsock.send(msg + '\r\n')


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
    for key in statuses:
        statuses[key] = getStatus(key)


def warnIfDown():
    msg = ''
    for key in statuses:
        if statuses[key].find('NEDE') != -1:
            if key.find('.') != -1:
                serverName = key
            else:
                serverName = key[:key.find('.')]
            msg += serverName + ': ' + statuses[key] + ' \x030,4ER NEDE\x03\n'
    if len(msg) > 0:
        sendText(msg)


def findName(ircmsg):
    return ircmsg[1:ircmsg.find('!')]


def isMod(name):
    return ('@' + name) in mods


def requestNames():
    send('NAMES [#tihlde-drift]')


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
send('USER ' + botnick + ' ' + botnick + ' ' + server + ' : pybot')
send('NICK ' + botnick)

send('JOIN ' + channel + ' ' + password)  # join channel

while 1:
    ircmsg = ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip('\n')  # removing linebreaks.

    print(ircmsg)  # print received message

    # Make sure the message is in specified channel and not a private msg
    if ircmsg.find('PRIVMSG #tihlde-drift') != -1:
        serverStatus = (ircmsg.find('.serverstatus') != -1)
        nerdvanaStatus = (ircmsg.find('.nerdvanastatus') != -1)
        if serverStatus or nerdvanaStatus:
            updateStatuses()

        if serverStatus:  # Respond to .serverstatus
            sendServerStatuses()

        if nerdvanaStatus:  # Respond to .nerdvanastatus
            sendNerdvanaStatuses()

        if ircmsg.find('.updatemods') != -1:
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
                    print('Discotime!')
                    ser.write(b'1')
                else:
                    ser.write(b'0')
            except serial.serialutil.SerialException:
                print('Device unplugged or wrong device used')

    # if this message is a name-list
    if ircmsg.find(':leguin.freenode.net 353 hal-9001 @ #tihlde-drift :') != -1:
        updateMods(ircmsg.strip(':leguin.freenode.net 353 hal-9001 @ #tihlde-drift :'))

    if ircmsg.find('PING :') != -1:  # respond to pings
        send('PONG ' + ircmsg[ircmsg.find(':') + 1])

    if time.strftime('%d') != updateDay:
        updateStatuses()
        warnIfDown()
        updateDay = time.strftime('%d')