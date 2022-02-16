class Attachment:

    def __init__(self, name, path):
        self.__name = name
        self.__path = path

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                    self.name == other.name
                    and self.path == other.path
            )
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__name + str(self.__code))

    def __str__(self):
        return self.__name
