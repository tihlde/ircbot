# coding: utf-8
__author__ = 'Harald Floor Wilhelmsen'


class Group(object):

    def __init__(self, name, owner, members):
        self.name = name
        self.owner = owner
        self.members = members

    def __str__(self):
        string = self.name + ' ' + self.owner + ':'
        for member in self.members:
            string += ' ' + member
        return string

    def __repr__(self):
        return self.__str__()