from datetime import date, datetime

from personal_library.library.borrowed_record import BorrowedRecord
from . import SearchStrategy


class DueDateSearchStrategy(SearchStrategy):
    def search(self, records: list[BorrowedRecord], search_term: str):
        dt: date = self.parse_date(search_term)
        return [record for record in records if record.due_date < dt]

    def parse_date(self, date_str: str):
        try:
            return datetime.strptime(date_str, "%Y/%m/%d").date()
        except ValueError as e:
            raise ValueError(f"Error: {e}")