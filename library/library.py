import logging
from datetime import date, timedelta
from threading import Lock
from typing import Any

from personal_library.book import Book
from personal_library.member import Member
from personal_library.exceptions import BookBorrowedAlready
from .borrowed_books import BorrowedBooks
from .borrowed_record import BorrowedRecord



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
        self.__borrowed_books: BorrowedBooks = BorrowedBooks()

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
    
    def borrow_book(self, member: Member, book: Book) -> Book:
        if not member or not book:
            raise ValueError("Member/book cannot be empty")
        
        # Check if for the record of borrowing the book exists already.
        if records := self.search_borrowed_record(member, book):
            br_bookname = records[0].book.bookname
            br_iss_dt = records[0].due_date
            raise BookBorrowedAlready(f"Error: Duplicate borrow record. You have borrowed this book, {br_bookname} on {br_iss_dt}.")
        
        # If not add the book to the borrowed books system.
        today: date = date.today()
        due_date = today + timedelta(days=1)
        
        br = BorrowedRecord(book, member, issued_on=today, due_date=due_date)
        self.__borrowed_books.add_record(br)
        
        logger.info(f"User {member.username} has borrowed book {book.bookname}.")
        
        return book
    
    def return_book(self, member: Member, book: Book) -> bool:
        if records := self.search_borrowed_record(member, book):
            if len(records) > 1:
                raise ValueError(f"Multiple borrowed records exists in the system for the same book {book.bookname} by the same member {member.username}")

            # Delete the record from the borrowed Books System.
            self.__borrowed_books.delete_record(records[0])
        return True
    

    def search_borrowed_record(self, member: Member, book: Book) -> list[BorrowedRecord]:
        search_term = ','.join([member.username, book.bookname])
        if records := self.__borrowed_books.search_record(search_term=search_term, search_type="userbook"):
            return records
        return []
