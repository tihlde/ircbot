# coding: utf-8
__author__ = 'Harald Floor Wilhelmsen'

from bot import Bot

ircserver = 'irc.freenode.net'
channel = '#tihlde-drift'
botnick = 'falkner'
password = open('pw').read()

bot = Bot(ircserver, channel, botnick, password)

bot.connect()

while True:
    bot.update()