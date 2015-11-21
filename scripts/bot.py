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


def send(msg):
    msg += '\r\n'
    print('SENDING')
    print(msg)
    ircsock.send(msg)


def sendtext(msg, rec):
    send('PRIVMSG ' + rec + ' :' + msg)


def findname(text):
    return text[1:text.find('!')]


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

    if ircmsg.find('.status(') != -1:  # Respond to .serverstatus
        sh.sendserverstatus(ircmsg[ircmsg.find('(') + 1: ircmsg.find(')')], sender)

    # Make sure the message is in specified channel and not a private msg
    if ircmsg.find('PRIVMSG ' + channel) != -1:
        dh.parsediscowish(ircmsg, sender)

    if ircmsg.find('PING :') != -1:  # respond to pings
        send('PONG ' + ircmsg[ircmsg.find(':') + 1])

    sh.update()
