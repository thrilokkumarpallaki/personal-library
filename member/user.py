import logging

from personal_library.exceptions import BookNotFound, InvalidBook
from personal_library.library import Library
from personal_library.book.book import Book


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

