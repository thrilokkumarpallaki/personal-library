from personal_library.library.borrowed_record import BorrowedRecord
from . import SearchStrategy


class BookNameSearchStrategy(SearchStrategy):
    def search(self, records: list[BorrowedRecord], search_term: str):
        return [record for record in records if record.book.bookname == search_term]
