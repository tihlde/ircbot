__author__ = 'Harald'


class Group(object):
    name = ""
    owner = ""
    members = {}
    def __init__(self, name, owner, members):
        self.name = name
        self.owner = owner
        self.members = members

    def __str__(self):
        string = self.name + " " + self.owner + ": "
        for member in self.members:
            string += " " + member
        return string

    def __repr__(self):
        return self.__str__()