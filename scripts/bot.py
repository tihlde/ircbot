# coding: utf-8
__author__ = 'Harald'

import socket
import atexit

import statushandler as sh
import discohandler as dh


ircserver = 'irc.freenode.net'
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


def send(msg):
    msg += '\r\n'
    print('SENDING')
    print(msg)
    ircsock.send(msg)


def sendtext(msg, rec):
    send('PRIVMSG ' + rec + ' :' + msg)


def findname(text):
    return text[1:text.find('!')]


def ismod(name):
    return ('@' + name) in mods


def requestnames():
    send('NAMES #tihlde-drift')


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((ircserver, 6667))
send('USER ' + botnick + ' ' + botnick + ' ' + ircserver + ' : pybot')
send('NICK ' + botnick)

send('JOIN ' + channel + ' ' + password)  # join channel


@atexit.register
def exitbot():
    print('Shutting down bot...')
    sh.savechanges()
    print('Config saved')
    send('PART ' + channel)
    print('Channel left')
    send('QUIT')
    print('Server quit')
    ircsock.close()
    print('Socket closed')
    print('*** Shutdown complete ***')


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
        sh.sendserverstatus(ircmsg[ircmsg.find('(') + 1: ircmsg.find(')')], sender)

    # Make sure the message is in specified channel and not a private msg
    if ircmsg.find('PRIVMSG ' + channel) != -1:
        if ircmsg.find('.updatemods') != -1:  # respond to .updatemods
            requestnames()
        if ismod(sender):  # if sender is a mod
            dh.parsediscowish(ircmsg)

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

    sh.update()
