import logging


logger = logging.getLogger("PersonalLibrary")


class Member:
    def __init__(self, name) -> None:
        self.__name: str = name

    @property
    def username(self):
        return self.__name
    
    @username.setter
    def username(self, new_name):
        self.__name = new_name

