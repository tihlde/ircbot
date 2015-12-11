# coding: utf-8
__author__ = 'Harald Floor Wilhelmsen'


class Helpparser(object):

    def __init__(self, filestring):
        with open(filestring, 'r') as file:
            for line in file:
                splitindex = line.find(':')
                strings = [line[:splitindex], line[splitindex + 1:].rstrip('\n')]
                self.helps[strings[0]] = strings[1]

    def gethelp(self, command):
        if command not in self.helps:
            return 'I cannot help you with that, sorry.'
        return self.helps[command]