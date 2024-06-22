from abc import ABC, abstractmethod

from ..borrowed_record import BorrowedRecord

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, records: list[BorrowedRecord], search_term: str):
        pass