# coding: utf-8
__author__ = 'Harald'

import socket
import time
import os

import serial


discoActive = True
updateDay = time.strftime("%d")

ser = serial.Serial('/dev/ttyACM0', 9600)

server = "irc.freenode.net"
channel = '#tihlde-drift'
botnick = "hal-9001"
password = open("pw").read()


def pingStatus(hostname):
    if os.system("ping -c 1 " + hostname + ".tihlde.org") == 0:
        return "\x033,1oppe\x03"
    else:
        return "\x030,4NEDE\x03"


statuses = {
    'colargol': pingStatus('colargol'),
    'fantorangen': pingStatus('fantorangen'),
    'odin': pingStatus('odin'),
    'coastguard': pingStatus('coastguard'),
    'handymanny': pingStatus('handymanny'),
    'balthazar': pingStatus('balthazar'),
    'thor': pingStatus('thor'),
    'vcenter.nerdvana': pingStatus('vcenter.nerdvana'),
    'bashful.nerdvana': pingStatus('bashful.nerdvana'),
    'dopey.nerdvana': pingStatus('dopey.nerdvana'),
    'grumpy.nerdvana': pingStatus('grumpy.nerdvana'),
    'sneezy.nerdvana': pingStatus('sneezy.nerdvana'),
    'sleepy.nerdvana': pingStatus('sleepy.nerdvana')
}


def joinchan(chan):
    send("JOIN " + chan + " " + password)


def send(msg):
    print(msg)
    ircsock.send(msg + "\r\n")


def sendmsg(chan, msg):
    send("PRIVMSG " + chan + " :" + msg)


def pingServers():
    sendmsg(channel, "colargol: " + statuses["colargol"] +
            "  fantorangen: " + statuses["fantorangen"] +
            "  odin: " + statuses["odin"] +
            "  coastguard: " + statuses["coastguard"] +
            "  handymanny: " + statuses["handymanny"] +
            "  balthazar: " + statuses["balthazar"] +
            "  thor: " + statuses["thor"]
            )


def pingNerdvana():
    sendmsg(channel, "vcenter: " + statuses["vcenter.nerdvana"] +
            "  bashful: " + statuses["bashful.nerdvana"] +
            "  grumpy: " + statuses["grumpy.nerdvana"] +
            "  dopey: " + statuses["dopey.nerdvana"] +
            "  sleepy: " + statuses["sleepy.nerdvana"] +
            "  sneezy: " + statuses["sneezy.nerdvana"]
            )


def updateStatuses():
    for key in statuses:
        statuses[key] = pingStatus(key)


def warnIfDown():
    msg = ""
    for key in statuses:
        if statuses[key].find("NEDE") != -1:
            if key.find(".") != -1:
                serverName = key
            else:
                serverName = key[:key.find(".")]
            msg += serverName + ": " + statuses[key] + " \x030,4ER NEDE\x03\n"
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

    # Make sure the message is in specified channel and not a private msg
    if ircmsg.find("PRIVMSG #tihlde-drift") != -1:
        if ircmsg.find(".serverstatus") != -1:  # Respond to .serverstatus
            updateStatuses()
            pingServers()

        if ircmsg.find(".nerdvanastatus") != -1:  # Respond to .nerdvanastatus
            updateStatuses()
            pingNerdvana()

        if ircmsg.find(".discoDeactivate") != -1:
            discoActive = False
        elif ircmsg.find(".discoActivate") != -1:
            discoActive = True

        if ircmsg.find(".discotime!") != -1 and discoActive:
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

