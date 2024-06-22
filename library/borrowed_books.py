import logging
from typing import Any
from datetime import date, timedelta

from personal_library.exceptions import InvalidSearchType, DuplicateBorrowRecord
from .borrowed_record import BorrowedRecord

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
        self.iter_idx = 0
        self.__borrowed_books: list[BorrowedRecord] = []

    def add_record(self, borrowed_record: BorrowedRecord):
        """
        This method adds a new borrowed record to the borrowed books store. If the record is already present in the 
        system it raises an error.
        :param borrowed_record: borrowed record instance to store a particular transaction.
        :return: None
        """
        if not self.search_record(borrowed_record.book.bookname):
            self.__borrowed_books.append(borrowed_record)
        raise DuplicateBorrowRecord(f"Record already exists with the book name: {borrowed_record.book.bookname} on member {borrowed_record.member.username}")
    
        logger.info("Record added to the Borrowed Books system")

    def delete_record(self, borrowed_record: BorrowedRecord):
        if borrowed_record in self.__borrowed_books:
            self.__borrowed_books.remove(borrowed_record)
            logger.info(f"Record removed from the borrowed books system: {borrowed_record}")
        else:
            logger.error(f"Record not found in the borrowed book system: {borrowed_record}")
    
    def update_due_date(self, borrowed_record: BorrowedRecord, new_due_date: date):
        if borrowed_record in self.__borrowed_books:
            borrowed_record.due_date = new_due_date
            logger.info(f"Due date udpated for the record: {borrowed_record}")
        else:
            logger.error(f"Record not found in the borrowed book system: {borrowed_record}")

    def search_record(self, search_str: str, search_type: str="bookname") -> BorrowedRecord | None:
        valid_search_types = {"bookname": "book", "username": "member", "due_date": "due_date", "userbook": "username,bookname"}
    
        if search_type not in valid_search_types:
            raise InvalidSearchType(f"SearchType {search_type} is not valid.")
        
        attr = valid_search_types[search_type]

        for record in self.__borrowed_books:
            obj = getattr(record, attr, None)
            if obj and getattr(obj, attr, None) == search_str:
                logger.info(f"Record found: {record}")
                return record
        
        logger.info(f"No record found for {search_str} under {search_type}.")
        return None
    
    def fine_calculation(self, borrowed_records: list[BorrowedRecord]) -> float:
        total_fine = 0

        for record in borrowed_records:
            td = timedelta(days=1)
            if record.due_date + td > date.today():
                total_days = (record.due_date + td - date.today()).days
                total_fine += (total_days * 1.5)
        return total_fine

    def report_overdues(self) -> list[BorrowedRecord]:
        over_due_records = [record for record in self.__borrowed_books if record.due_date < date.today()]
        return over_due_records
