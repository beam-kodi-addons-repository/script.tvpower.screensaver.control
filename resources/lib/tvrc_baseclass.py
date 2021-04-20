from utilities import log
class BaseTVRemoteControl(object):

    @classmethod
    def ident(cls):
        return cls.__name__ + ": " + cls.ident_desc()

    @classmethod
    def ident_desc(cls):
        return "No description"

    def __init__(self):
        log(["Not implemented", "Init", self.__class__.__name__], "warn")

    def turn_off(self):
        log(["Not implemented", "Turn OFF", self.__class__.__name__], "warn")

    def turn_on(self):
        log(["Not implemented", "Turn ON", self.__class__.__name__], "warn")
