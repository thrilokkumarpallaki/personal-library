import logging

from typing import Any
from personal_library.book import Book
from threading import Lock

logger = logging.getLogger("PersonalLibrary")


class LibraryMeta(type):
    instance_: dict = {}
    lock_: Lock = Lock()

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        with cls.lock_:
            if cls not in cls.instance_:
                instance = super().__call__(*args, **kwds)
                cls.instance_[cls] = instance
            return cls.instance_[cls]



class Library(metaclass=LibraryMeta):
    # Singleton class
    def __init__(self) -> None:
        self.__book_collection: dict[str:Book] = {}

    def add_book(self, book) -> None:
        self.__book_collection[book.bookname] = book
        logger.info(f"New book addded to the collection: {book.bookname}")

    def remove_book(self, book) -> None:
        del self.__book_collection[book.bookname]
        logger.info(f"A book has been removed from the collection: {book.bookname}")

    def search_book(self, book_name) -> Book | None:
        if book_name in self.__book_collection:
            logger.info(f"book, {book_name} found in the library collection!")
            return self.__book_collection[book_name]
        else:
            logger.info(f"Students looking for book name: {book_name} and it is not found!")
            return None
    
    def borrow_book(self, book: Book) -> Book:
        # TODO: Add the entry to BorrowedBooks, when a user borrows a book.
        return book
    
    def return_book(self, book: Book) -> bool:
        # TODO: Make the changes in the systems regarding the book and check the dues.
        return True
