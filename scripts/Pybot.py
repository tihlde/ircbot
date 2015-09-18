# coding: utf-8
__author__ = 'Harald'

import socket
import time
from random import randint
from subprocess import call

updateTime = 5  # time between updates in seconds
lastUpdate = time.time()  # time since last update

server = "irc.freenode.net"
channel = '#tihlde-drift'
botnick = "hal-9001"
password = open("pw").read()
greetings = ["We meet again",
             "Hello",
             "Sup",
             "What's up?",
             "It's been a long time... not long enough",
             "Hi!",
             "My old nemesis",
             "Did you hear something?",
             "I think some sub-intelligent species is trying to establish contact..."]


def sendmsg(chan, msg):
    send("PRIVMSG " + chan + " :" + msg)


def joinchan(chan):
    send("JOIN " + chan + " " + password)


def send(msg):
    print(msg)
    ircsock.send(msg + "\r\n")

def compileAndUpload(beers):
    codeDeclerations = ""
    codeSetupStart = "void setup() {"
    codeSetup = ""
    codeSetupEnd = "}"
    codeLoopStart = "void loop() {"
    codeLoop = ""
    codeLoopEnd = ""
    code = codeDeclerations + codeSetupStart + codeSetup + codeSetupEnd + codeLoopStart + codeLoop + codeLoopEnd;
    call("")


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
send("USER " + botnick + " " + botnick + " " + server + " : pybot")
send("NICK " + botnick)

joinchan("#tihlde")
send("PRIVMSG hilde: .øl")

joinchan(channel)

while 1:
    ircmsg = ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip('\n')  # removing any unnecessary linebreaks.

    print(ircmsg)

    if ircmsg.lower().find(":hello " + botnick) != -1:
        send("PRIVMSG " + channel + " :" + greetings[randint(0, len(greetings) - 1)])
    elif ircmsg.find(botnick) > ircmsg.find("!") and ircmsg.find("PRIVMSG #tihlde-drift") != -1:
        send("PRIVMSG " + channel + " :I cannot do that " + ircmsg[1:(ircmsg.find("!"))])

    if ircmsg.find("PING :") != -1:  # respond to pings
        send("PONG " + ircmsg[ircmsg.find(":") + 1])

    now = time.time()
    if now > lastUpdate + updateTime:
        # more than the updateTime has gone by
        lastUpdate = now
        send("PRIVMSG hilde: .øl")
