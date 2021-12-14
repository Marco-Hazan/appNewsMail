
class Channel:

    def __init__(self,name,is_active,owner,isnew):
        self.__name = name
        self.__is_active = is_active
        self.__owner = owner
        self.__isnew = isnew

    @property
    def name(self):
        return self.__name

    @property
    def is_active(self):
        return self.__is_active

    @property
    def owner(self):
        return owner

    @property
    def isnew(self):
        return isnew

    def __eq__(self,other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(name + str(code))
