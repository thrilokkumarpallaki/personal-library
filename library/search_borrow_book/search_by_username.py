from personal_library.library.borrowed_record import BorrowedRecord
from . import SearchStrategy


class UserNameSearchStrategy(SearchStrategy):
    def search(self, records: list[BorrowedRecord], search_term: str):
        return [record for record in records if record.member.username == search_term]
