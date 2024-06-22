from personal_library.library.borrowed_record import BorrowedRecord
from . import SearchStrategy


class UserBookSearchStrategy(SearchStrategy):
    def search(self, records: list[BorrowedRecord], search_term: str):
        username, bookname = search_term.split(',')
        return [record for record in records if record.member.username == username.strip() and record.book.bookname == bookname.strip()]
    