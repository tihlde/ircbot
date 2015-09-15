__author__ = 'Harald'

# Import some necessary libraries.
import socket
# Set up our commands function
def commands(nick,channel,message):
    if message.find(botnick+': shellium') != -1:
        ircsock.send('PRIVMSG %s :%s: Shellium is awesome!\r\n' % (channel,nick))
    elif message.find(botnick+': help') != -1:
        ircsock.send('PRIVMSG %s :%s: My other command is shellium.\r\n' % (channel,nick))

server = "irc.freenode.net"
channel = "#tihlde-drift"
botnick = "anna"
password = open("pw").read()

def ping():
    ircsock.send("PONG :pingis\n")

def sendmsg(chan , msg):
    ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")

def joinchan(chan):
    ircsock.send("JOIN "+ chan + "[" + password + "]" + "\n")

def hello():
    ircsock.send("PRIVMSG "+ channel +" :Sup fucker!\n")

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick)
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined

while 1: # Be careful with these! it might send you to an infinite loop
    ircmsg = ircsock.recv(2048) # receive data from the server
    ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
    print(ircmsg) # Here we print what's coming from the server
    if ircmsg.find(' PRIVMSG ') != -1:
        nick=ircmsg.split('!')[0][1:]
        thisChan = ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
        commands(nick, thisChan, ircmsg)

    if ircmsg.find(":Hello "+ botnick) != -1: # if someone says "Hello anna"
        hello()

    if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
        ping()