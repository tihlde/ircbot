# coding: utf-8
__author__ = 'Harald Floor Wilhelmsen'

import socket
import atexit
import time

import statushandler as sh
import discohandler as dh

class Bot(object):

    def __init__(self, ircserver, channel, botnick, password):
        self.ircserver = ircserver
        self.channel = channel
        self.botnick = botnick
        self.password = password


    def send(self, msg):
        msg += '\r\n'
        print('SENDING')
        print(msg)
        self.ircsock.send(msg)


    def sendtext(self, msg, rec):
        self.send('NOTICE ' + rec + ' :' + msg)


    def findname(self, text):
        return text[1:text.find('!')]


    def requestnames(self):
        self.send('NAMES #tihlde-drift')

    def connect(self):
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ircsock.connect((self.ircserver, 6667))
        self.send('USER ' + self.botnick + ' ' + self.botnick + ' ' + self.ircserver + ' : Falkner, from Violet City')
        self.send('NICK ' + self.botnick)
        self.send('JOIN ' + self.channel + ' ' + self.password)  # join channel
        self.lastping = time.time()


    @atexit.register
    def exitbot(self):
        print('Shutting down bot...')
        sh.savechanges()
        print('Config saved')
        self.send('PART ' + self.channel)
        print('Channel left')
        self.send('QUIT')
        print('Server quit')
        self.ircsock.close()
        print('Socket closed')
        print('*** Shutdown complete ***')


    def update(self):
        ircmsg = self.ircsock.recv(2048)  # receive data from the server
        ircmsg = ircmsg.strip('\n')  # removing linebreaks.

        if ircmsg.find('NOTICE') != -1:
            return

        if ircmsg:
            print('RECEIVED')
            print(ircmsg)  # print received message

        sender = self.findname(ircmsg)
        recipient = sender

        # If message is to channel
        if ircmsg.find('PRIVMSG ' + self.channel) != -1:
            discoreturn = dh.parsediscowish(ircmsg, sender)
            if discoreturn != '':
                self.sendtext(discoreturn, self.channel)
            recipient = self.channel

        # command-parsing
        angleindex = ircmsg.find('>')
        if angleindex != -1 and ircmsg[angleindex - 1] == ':':
            command = ircmsg[angleindex + 1:]
            argsstart = command.find(' ')
            # Splits args-segment of string into strings and removes empty entries
            args = filter(None, [x.replace(' ', '') for x in command[argsstart:].strip().split(' ')])
            command = command[:argsstart].strip()
            self.sendtext(sh.executecommand(command, args, sender), recipient)

        now = time.time()
        if ircmsg.find('PING :') != -1:  # respond to pings
            self.lastping = now
            self.send('PONG ' + ircmsg[ircmsg.find(':') + 1:])
        elif now > self.lastping + 300: # Reconnect on timeout
            self.connect()

        sh.update()
        if sh.updatechanges:
            for serverdata in sh.updatechanges:
                group = sh.getgroup(serverdata.notifygroup)
                for name in group.members:
                    self.sendtext('Statusendring: ' + serverdata.prettyname
                             + ' er nå ' + serverdata.status, name)
            sh.updatechanges = []
