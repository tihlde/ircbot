__author__ = 'Harald'

import socket

server = "irc.freenode.net"
channel = '#tihlde-drift'
botnick = "hal-9001"
password = open("pw").read()


def sendmsg(chan, msg):
    send("PRIVMSG " + chan + " :" + msg)


def joinchan(chan):
    send("JOIN " + chan + " " + password)


def hello():
    send("PRIVMSG " + channel + " :sup")


def send(msg):
    ircsock.send(msg + "\r\n")


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
send("USER " + botnick + " " + botnick + " " + server + " : pybot")
send("NICK " + botnick)

joinchan(channel)

while 1:
    ircmsg = ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip('\n')  # removing any unnecessary linebreaks.
    print(ircmsg)

    if ircmsg.find(":Hello " + botnick) != -1:
        hello()

    if ircmsg.find("PING :") != -1:  # respond to pings
        send("PONG " + ircmsg[ircmsg.find(":") + 1])
