# coding: utf-8
__author__ = 'Harald'

import serial
import socket
import time
import os
from random import randint

updateDay = time.strftime("%d")

ser = serial.Serial('/dev/ttyACM0', 9600)

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

status = {
    'colargol': 'notYetAvailable',
    'fantorangen': 'notYetAvailable',
    'odin': 'notYetAvailable',
    'coastguard': 'notYetAvailable',
    'handymanny': 'notYetAvailable',
    'balthazar': 'notYetAvailable',
    'thor': 'notYetAvailable',
    'vcenter.nerdvana': 'notYetAvailable',
    'bashful.nerdvana': 'notYetAvailable',
    'dopey.nerdvana': 'notYetAvailable',
    'grumpy.nerdvana': 'notYetAvailable',
    'sneezy.nerdvana': 'notYetAvailable',
    'sleepy.nerdvana': 'notYetAvailable'
}


def joinchan(chan):
    send("JOIN " + chan + " " + password)


def send(msg):
    print(msg)
    ircsock.send(msg + "\r\n")


def sendmsg(chan, msg):
    send("PRIVMSG " + chan + " :" + msg)


def pingServers():
    sendmsg(channel, "colargol: " + status["colargol"] +
            "  fantorangen: " + status["fantorangen"] +
            "  odin: " + status["odin"] +
            "  coastguard: " + status["coastguard"] +
            "  handymanny: " + status["handymanny"] +
            "  balthazar: " + status["balthazar"] +
            "  thor: " + status["thor"]
            )


def pingNerdvana():
    sendmsg(channel, "vcenter: " + status["vcenter.nerdvana"] +
            "  bashful: " + status["bashful.nerdvana"] +
            "  grumpy: " + status["grumpy.nerdvana"] +
            "  dopey: " + status["dopey.nerdvana"] +
            "  sleepy: " + status["sleepy.nerdvana"] +
            "  sneezy: " + status["sneezy.nerdvana"]
            )


def getPing(hostname):
    if os.system("ping -c 1 " + hostname + ".tihlde.org") == 0:
        return "\x033,1oppe\x03"
    else:
        return "\x030,4NEDE\x03"


def updateStatuses():
    for key in status:
        status[key] = getPing(key)


def warnIfDown():
    msg = ""
    for key in status:
        if status[key].find("NEDE") != -1:
            msg += key[:key.find(".")] + ": " + status[key] + " \x030,4ER NEDE\x03\n"
    if len(msg) > 0:
        sendmsg(channel, msg)


ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
send("USER " + botnick + " " + botnick + " " + server + " : pybot")
send("NICK " + botnick)

joinchan(channel)

while 1:
    ircmsg = ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip('\n')  # removing linebreaks.

    print(ircmsg)
    
    if ircmsg.find("PRIVMSG #tihlde-drift") != -1:  # Responds to 'Hello botnick'
        if ircmsg.lower().find(":hello " + botnick) != -1:
            send("PRIVMSG " + channel + " :" + greetings[randint(0, len(greetings) - 1)])
        elif ircmsg.find(".serverstatus") != -1:  # Responds to -serverstatus
            updateStatuses()
            pingServers()
        elif ircmsg.find(".nerdvanastatus") != -1:  # Respons to .nerdvanastatus
            updateStatuses()
            pingNerdvana()
    if ircmsg.find(".discotime!") != -1:
        print("Discotime!")
        ser.write(b'1')
    else:
        ser.write(b'0')

    if ircmsg.find("PING :") != -1:  # respond to pings
        send("PONG " + ircmsg[ircmsg.find(":") + 1])

    if time.strftime("%d") != updateDay:
        updateStatuses()
        warnIfDown()
        updateDay = time.strftime("%d")

