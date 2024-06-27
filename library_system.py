from typing import Any


from threading import Lock
import logging

from personal_library.book import Book
from personal_library.library import Library
from personal_library.member import Member

from personal_library.exceptions import BookAlreadyExists


logger = logging.getLogger("PersonalLibrary")


class LibrarySystemMeta(type):
    instance_: dict = {}
    lock_: Lock = Lock()

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        with cls.lock_:
            if cls not in cls.instance_:
                instance = super().__call__(*args, **kwds)
                cls.instance_[cls] = instance

            return cls.instance_[cls]

class LibrarySystem(metaclass=LibrarySystemMeta):
    def __init__(self) -> None:
        self.__library: Library = Library()
        
    def create_member(self, name) -> Member:
        """
        This methods creates user with a given name.
        :param name: name of the user.
        :return: It returns a member instance.
        """
        logger.info(f"Creating user with username: {name}")
        new_member = Member(name=name)
        return  new_member
    
    def search_book(self, book_name: str) -> Book | None:
        """
        This method searches the given book name in the library. If a book with the name is present
        it returns as a return value.
        :param book_name: name of the book.
        :return: It returns a book instance if the book is present. Otherwise None.
        """
        if book := self.__library.search_book(book_name):
            return book
        else:
            return None
        
    def add_book(self, **kwargs) -> Book:
        """
        This method adds a new book with given informations. If the books is already present in the library
        it throws an error 
        """
        book_name = kwargs.get('title')
        
        if self.__library.search_book(book_name=book_name):
            raise BookAlreadyExists("Book already exists in the library.")
        
        # Create book instance
        new_book = Book(**kwargs)
        self.__library.add_book(new_book)
        return new_book

    def remove_book(self, book: Book) -> Book | None:
        if book := self.__library.search_book(book.bookname):
            self.__library.remove_book(book)
            return book
        else:
            return None

    def borrow_book(self, member: Member, book: Book) -> Book | None:
        if member is None or book is None:
            raise ValueError("Member/Book cannot be empty")
        
        if book := self.__library.borrow_book(member, book):
            return book
        else:
            return None
        
    def return_book(self, member: Member, book: Book):
        if member is None or book is None:
            raise ValueError("Member/Book cannot be empty")
        
        if status := self.__library.return_book(member, book):
            return status
        
    def renew_book(self, member: Member, book_name: str):
        return self.__library.renew_book(member, book_name)
        