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
    host = server[0]
    status = getStatus(host)
    newStatuses[host] = status
    oldStatuses[host] = status


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
        if newStatus[0] != oldStatus[0]:  # status has changed
            oldStatus[0] = newStatus[0]
            msg += newStatus[2] + ' er nå ' + newStatus[0] + '  '
        if len(msg) > 0:
            for name in newStatus[4]:
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


def saveConfig():
    file = open("config", "w")
    for status in newStatuses:
        str = status[1] + ',' + status[2] + ',' + status[3] + ',['
        for name in status[4]:
            str += name + ','
        str = str[:-1] + ']'
        file.write(str + '\n')


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


@atexit.register
def exitBot():
    print('Shutting down bot...')
    saveConfig()
    print('Config saved')
    send('PART ' + channel)
    print('Channel left')
    send('QUIT')
    print('Quit server')
    ircsock.close()
    print('Socket closed')
    print('*** Shutdown complete ***')

