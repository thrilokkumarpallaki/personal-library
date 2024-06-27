import logging

from datetime import date

from personal_library.book import Book
from personal_library.member import Member


logger = logging.getLogger("personalLibrary")


class BorrowedRecord:
    def __init__(self, book: Book, member: Member, issued_on: date, due_date: date, **kwargs) -> None:
        self.book = book
        self.member = member
        self.issued_on = issued_on
        self.due_date = due_date
        self.last_renewal_date = None
        self.extas = kwargs

    def __str__(self) -> str:
        return f"{self.book.bookname} borrowed by {self.member.username} on {self.issued_on.strftime('%d/%m/%Y')}."