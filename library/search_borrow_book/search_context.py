from . import SearchStrategy
from ..borrowed_record import BorrowedRecord
from .search_by_bookname import BookNameSearchStrategy
from .search_by_due_date import DueDateSearchStrategy
from .search_by_username import UserNameSearchStrategy
from .search_by_userbook import UserBookSearchStrategy
from personal_library.exceptions import InvalidSearchType


class BorrowedBookSearchContext:
    def __init__(self, search_strategy: SearchStrategy = None) -> None:
        self._search_strategy = search_strategy
        self._valid_search_strategies = {'bookname': BookNameSearchStrategy(), 'username': UserNameSearchStrategy(), 
                                        'due_date': DueDateSearchStrategy(), 'userbook': UserBookSearchStrategy()}
        
    def set_search_strategy(self, search_type: str) -> None:
        if search_type.lower() in self._valid_search_strategies:
            self._search_strategy = self._valid_search_strategies.get(search_type)
            return 
        raise InvalidSearchType(f"{search_type} is not a valid search type.")
        

    def search_record(self, borrowed_records: list[BorrowedRecord], search_term: str) -> list[BorrowedRecord]:
        return self._search_strategy.search(borrowed_records, search_term=search_term)