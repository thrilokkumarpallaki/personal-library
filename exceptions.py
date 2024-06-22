
class BookNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidBook(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BookAlreadyExists(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidSearchType(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DuplicateBorrowRecord(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BookBorrowedAlready(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
