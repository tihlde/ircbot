# coding: utf-8
__author__ = 'Harald'

import socket
import time
import os
import threading

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


newStatuses = {
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

oldStatuses = {
    'colargol': newStatuses['colargol'],
    'fantorangen': newStatuses['fantorangen'],
    'odin': newStatuses['odin'],
    'coastguard': newStatuses['coastguard'],
    'handymanny': newStatuses['handymanny'],
    'balthazar': newStatuses['balthazar'],
    'thor': newStatuses['thor'],
    'vcenter.nerdvana': newStatuses['vcenter.nerdvana'],
    'bashful.nerdvana': newStatuses['bashful.nerdvana'],
    'dopey.nerdvana': newStatuses['dopey.nerdvana'],
    'grumpy.nerdvana': newStatuses['grumpy.nerdvana'],
    'sneezy.nerdvana': newStatuses['sneezy.nerdvana'],
    'sleepy.nerdvana': newStatuses['sleepy.nerdvana']
}


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
             '  bashful: ' + oldStatuses['bashful.nerdvana'] +
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
    for key in newStatuses:
        newStat = newStatuses[key]
        if newStat != oldStatuses[key]:
            oldStatuses[key] = newStat
            msg += key[:key.find('.')] + ' er nå ' + newStat + '  '
    if len(msg) > 0:
        if msg.find('NEDE') != -1:
            msg += ';'
            for name in mods:
                msg += ' ' + name[1:]
        sendText('Statusendringer: ' + msg)


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

    filterString = ':leguin.freenode.net 353 hal-9001 @ #tihlde-drift :'
    # if this message is a name-list
    isNameMsg = ircmsg.find(filterString) != -1
    isNotJoinMsg = ircmsg.find(':leguin.freenode.net 333 hal-9001 #tihlde-drift') == -1
    if isNameMsg and isNotJoinMsg:
        nsStart = len(filterString)
        nsEnd = ircmsg.find(':leguin.freenode.net 366 hal-9001 #tihlde-drift :End of /NAMES list.')
        nameString = ircmsg[nsStart:nsEnd]

        nameString = nameString.replace('\r\n:leguin.freenode.net', '')
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