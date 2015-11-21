__author__ = 'Harald'


class Group(object):
    owner = ""
    members = {}
    def __init__(self, owner, members):
        self.owner = owner
        self.members = members

    def __str__(self):
        string = "owner=" + self.owner
        for member in self.members:
            string += " " + member
        return string

    def __repr__(self):
        return self.__str__()