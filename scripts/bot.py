# coding: utf-8
__author__ = 'Harald'

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

    if len(ircmsg) > 0:
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

    angleindex = ircmsg.find('>')
    if angleindex != -1:
        command = ircmsg[angleindex + 1:]
        argsstart = command.find(" ")
        args = [x.replace(" ", '') for x in command[argsstart:].strip().split(' ')]
        command = command[:argsstart].strip()
        if command not in sh.commands:
            sendtext("Invalid command: " + command, recipient)
        else:
            sendtext(sh.executecommand(command, args, sender), recipient)


    if ircmsg.find('PING :') != -1:  # respond to pings
        send('PONG ' + ircmsg[ircmsg.find(':') + 1])

    sh.update()
    if len(sh.updatechanges) > 0:
        for update in sh.updatechanges:
            serverdata = update[0]
            group = sh.getgroup(serverdata.notifygroup)
            for name in group:
                sendtext(update[1], name)
        sh.updatechanges = []
