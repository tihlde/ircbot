# coding: utf-8
__author__ = 'Harald Floor Wilhelmsen'

from helpparser import Helpparser

class Command(object):

    def __init__(self, execute, helpmsg):
        self.execute = execute
        self.helpmsg = helpmsg