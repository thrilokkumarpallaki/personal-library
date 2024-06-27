import logging
from datetime import date, timedelta
from threading import Lock
from typing import Any

from personal_library.constants import Constants
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
        search_term = ','.join([member.username, book.bookname])
        if records := self.search_borrowed_record(search_term):
            br_bookname = records[0].book.bookname
            br_iss_dt = records[0].due_date
            raise BookBorrowedAlready(f"Error: Duplicate borrow record. You have borrowed this book, {br_bookname} on {br_iss_dt}.")
        
        today, due_date = self.get_borrowing_periods()
        # If not add the book to the borrowed books system.
        br = BorrowedRecord(book, member, issued_on=today, due_date=due_date)
        self.__borrowed_books.add_record(br)
        
        logger.info(f"User {member.username} has borrowed book {book.bookname}.")
        
        return book
    
    def return_book(self, member: Member, book: Book) -> bool:
        search_term = ','.join([member.username, book.bookname])
        if records := self.search_borrowed_record(search_term):
            if len(records) > 1:
                raise ValueError(f"Multiple borrowed records exists in the system for the same book {book.bookname} by the same member {member.username}")

            # Delete the record from the borrowed Books System.
            if self.__borrowed_books.delete_record(records[0]):
                return True
        return False

    def search_borrowed_record(self, search_term: str, search_type: str="userbook") -> list[BorrowedRecord]:
        if records := self.__borrowed_books.search_record(search_term=search_term, search_type=search_type):
            return records
        return []
    
    def renew_book(self, member: Member, book_name: str) -> bool:
        # Check for borrowed record in the borrow record system
        search_term = ','.join([member.username, book_name])
        records = self.search_borrowed_record(search_term=search_term)
        
        if len(records) > 0 and len(records) == 1:
            borrowed_record = records[0]
        elif len(records) == 0:
            logger.error(f"No record found with the search criteria: {search_term}")
        else:
            raise ValueError(f"Multiple borrowed records exists in the system for search criteria: {search_term}")
        
        if isinstance(borrowed_record, BorrowedRecord):
            today, new_due_date = self.get_borrowing_periods()
            self.__borrowed_books.renew_book(borrowed_record, today, new_due_date)
            logger.info(f"Book, {borrowed_record.book.bookname} renewed successfully!")
            return True
        else:
            raise TypeError(f"Expected an instance of {BorrowedRecord.__name__} type, instead got {type(borrowed_record)}.")

    @staticmethod
    def get_borrowing_periods() -> tuple[date]:
        today: date = date.today()
        due_date = today + timedelta(days=Constants.BORROW_PERIOD_IN_DAYS)
        return today, due_date
