import logging


logger = logging.getLogger("PersonalLibrary")


class Book:
    def __init__(self, **kwargs) -> None:
        self.__title = kwargs.get('title')
        self.__author = kwargs.get('author')
        self.__isbn = kwargs.get('isbn')
        self.__description = kwargs.get('description')

        if self.__title is None:
            raise ValueError("Book name cannot be empty")

    @property
    def bookname(self):
        return self.__title

    @bookname.setter
    def bookname(self, name):
        self.__title = name

    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self, desc):
        self.__description = desc

    @property
    def isbn(self):
        return self.__isbn
    
    @isbn.setter
    def isbn(self, isbn):
        self.__isbn = isbn

    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, author_name):
        self.__author = author_name

