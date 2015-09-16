__author__ = 'Harald'

# Import some necessary libraries.
import socket
import time

server = "irc.freenode.net"
channel = '#tihlde-drift'
botnick = "hilde-drift"
password = open("pw").read()

def sendmsg(chan , msg):
    ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\r\n")

def joinchan(chan):
    ircsock.send("JOIN "+ chan + " "  + password + "\r\n")

def hello():
    ircsock.send("PRIVMSG "+ channel +" :Sup fucker\r\n")

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send("USER "+ botnick + " " + botnick +" " + server + " : pybot\r\n")
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined

while 1: # Be careful with these! it might send you to an infinite loop
    ircmsg = ircsock.recv(2048) # receive data from the server
    ircmsg = ircmsg.strip('\n') # removing any unnecessary linebreaks.
    print(ircmsg) # Here we print what's coming from the server

    if ircmsg.find(":Hello "+ botnick) != -1: # if someone says "Hello anna"
        hello()

    if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
        ircsock.send("PONG " + ircmsg[ircmsg.find(":") + 1])
