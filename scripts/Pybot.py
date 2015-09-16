__author__ = 'Harald'

import socket
from random import randint

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


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
send("USER " + botnick + " " + botnick + " " + server + " : pybot")
send("NICK " + botnick)

joinchan(channel)

while 1:
    ircmsg = ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip('\n')  # removing any unnecessary linebreaks.
    ircmsg = ircmsg.lower()
    print(ircmsg)

    if ircmsg.find(":hello " + botnick) != -1:
        send("PRIVMSG " + channel + " :" + greetings[randint(0, len(greetings) - 1)])
    elif ircmsg.find(botnick) > ircmsg.find("!") and ircmsg.find("PRIVMSG #tihlde-drift") != -1:
        send("PRIVMSG " + channel + " :I cannot do that " + ircmsg[1:(ircmsg.find("!"))])

    if ircmsg.find("PING :") != -1:  # respond to pings
        send("PONG " + ircmsg[ircmsg.find(":") + 1])
