import logging
from typing import Any
from datetime import date, timedelta

from personal_library.constants import Constants
from personal_library.exceptions import DuplicateBorrowRecord
from .borrowed_record import BorrowedRecord
from .search_borrow_book import BorrowedBookSearchContext

logger = logging.getLogger("PersonalLibrary")


class BorrowedBooksMeta(type):
    """
    BorrowedBooks Meta class helps to create a singleton instance for the BorrowedBooks Class.
    This is done by checking the instance_ class variable is contains the instance. If yes, returns the object.
    Otherwise create a new one. 
    """
    instance_: dict = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls.instance_:
            instance = super().__call__(*args, **kwds)
            cls.instance_[cls] = instance
        return cls.instance_[cls]
    

class BorrowedBooks(metaclass=BorrowedBooksMeta):
    """
    A class to maintain BorrowedRecords in the library system. It has following functionalities:
     1. Add Record
     2. Delete Record
     3. Search Record with following search types: bookname, username, due_date
     4. update_due_date
     5. fine_calculation
     6. report_overdues.
    """
    def __init__(self) -> None:
        self.__borrowed_books: list[BorrowedRecord] = []
        self.__search_context = BorrowedBookSearchContext()

    def add_record(self, borrowed_record: BorrowedRecord):
        """
        This method adds a new borrowed record to the borrowed books store. If the record is already present in the 
        system it raises an error.
        :param borrowed_record: borrowed record instance to store a particular transaction.
        :return: None
        """
        if not self.search_record(borrowed_record.book.bookname):
            self.__borrowed_books.append(borrowed_record)
            logger.info("Record added to the Borrowed Books system")
            return 
        raise DuplicateBorrowRecord(f"Record already exists with the book name: {borrowed_record.book.bookname} on member {borrowed_record.member.username}")
    
    def delete_record(self, borrowed_record: BorrowedRecord):
        """
        This method deletes the borrowed record from the system, when a user returns the book. It checks if the records
        exists in the system and then it removes the records.
        :param borrowed_record: A Record entry for the the transaction when a book borrowed by an user.
        :return: None
        """
        if borrowed_record in self.__borrowed_books:
            self.__borrowed_books.remove(borrowed_record)
            logger.info(f"Record removed from the borrowed books system: {borrowed_record}")
        else:
            logger.error(f"Record not found in the borrowed book system: {borrowed_record}")
    
    def update_due_date(self, borrowed_record: BorrowedRecord, new_due_date: date):
        """
        This method updates the due date for the books that are already borrowed by the user. It checks for the record
        existance and then performs the intended action.
        :param borrowed_record: A Record entry for the transaction when a book borrowed by an user.
        :param new_due_date: Date object to extend the time period for the borrowed book.
        :return: None
        """
        if borrowed_record in self.__borrowed_books:
            borrowed_record.due_date = new_due_date
            logger.info(f"Due date udpated for the record: {borrowed_record}")
        else:
            logger.error(f"Record not found in the borrowed book system: {borrowed_record}")

    def search_record(self, search_term: str, search_type: str="bookname") -> list[BorrowedRecord]:
        """
        This method search for the books records in borrowed books system. It allows multiple search types for search
        criteria.
        search_type: bookname search_term: <Name of the book>
        search_type: username search_term: <Name of the member>
        search_type: due_date search_term: <Date in string format "%Y/%m/%d"> - It only accepts the mentioned string format.
                                            If any other string format is specified it throws a ValueError.
        search_type: userbook search_term: <username,bookname> - This search term follows a convetion that username &
                                            bookname should be seperated by a comma.
        
        :param search_term: A search string to search.
        :param search_type: As mentioned above. It has default search type ie., bookname
        :return: A list of borrowed records.
        """

        self.__search_context.set_search_strategy(search_type=search_type)
        return self.__search_context.search_record(self.__borrowed_books, search_term=search_term)
    
    def fine_calculation(self, borrowed_records: list[BorrowedRecord]) -> float:
        f"""
        This method calculates the fine for the list of borrowed books. The borrowing period for any book is
        one day. For every book that crosses the due date, the fine will be calculated as
            total_days_after_due_date * {Constants.FINE_AMOUNT_PER_DAY}.
        :param borrowed_records: A list of borrowed records to calculate the fine amount.
        :return: It returns total fine amount for the list of borrowed books.
        """
        total_fine = 0

        for record in borrowed_records:
            # Borrowing period for a book.
            td = timedelta(days=Constants.BORROW_PERIOD_IN_DAYS)

            if date.today() > record.due_date:
                overdue_days = (date.today() - record.due_date).days
                total_fine += (overdue_days * Constants.FINE_AMOUNT_PER_DAY)
        return total_fine

    def report_overdues(self) -> list[BorrowedRecord]:
        """
        This method checks for list of overdue records by that day.
        :return: A list of overdue records.
        """
        over_due_records = [record for record in self.__borrowed_books if record.due_date < date.today()]
        return over_due_records
