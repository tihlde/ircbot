# coding: utf-8
__author__ = 'Harald Floor Wilhelmsen'

import socket
import atexit

import statushandler as sh
import discohandler as dh


ircserver = 'irc.freenode.net'
channel = '#tihlde-drift'
botnick = 'falkner'
password = open('pw').read()


def send(msg):
    msg += '\r\n'
    print('SENDING')
    print(msg)
    ircsock.send(msg)


def sendtext(msg, rec):
    send('NOTICE ' + rec + ' :' + msg)


def findname(text):
    return text[1:text.find('!')]


def requestnames():
    send('NAMES #tihlde-drift')


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((ircserver, 6667))
send('USER ' + botnick + ' ' + botnick + ' ' + ircserver + ' : Falkner, from Violet City')
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

    if ircmsg.find('NOTICE') != -1:
        continue

    if ircmsg:
        print('RECEIVED')
        print(ircmsg)  # print received message

    sender = findname(ircmsg)
    recipient = sender

    # If message is to channel
    if ircmsg.find('PRIVMSG ' + channel) != -1:
        discoreturn = dh.parsediscowish(ircmsg, sender)
        if discoreturn != '':
            sendtext(discoreturn, channel)
        recipient = channel

    # command-parsing
    angleindex = ircmsg.find('>')
    if angleindex != -1 and ircmsg[angleindex - 1] == ':':
        command = ircmsg[angleindex + 1:]
        argsstart = command.find(' ')
        # Splits args-segment of string into strings and removes empty entries
        args = filter(None, [x.replace(' ', '') for x in command[argsstart:].strip().split(' ')])
        command = command[:argsstart].strip()
        sendtext(sh.executecommand(command, args, sender), recipient)

    if ircmsg.find('PING :') != -1:  # respond to pings
        send('PONG ' + ircmsg[ircmsg.find(':') + 1:])

    sh.update()
    if sh.updatechanges:
        for serverdata in sh.updatechanges:
            group = sh.getgroup(serverdata.notifygroup)
            for name in group.members:
                sendtext('Statusendring: ' + serverdata.prettyname
                         + ' er nå ' + serverdata.status, name)
        sh.updatechanges = []
