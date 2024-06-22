import unittest

from personal_library.book import Book
from personal_library.library import Library


class LibraryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.library: Library = Library()
        self.book = Book(title="my book", author="thrilok pallaki", isbn="123456", description="This is my book.")

    def test_add_book(self):
        self.library.add_book(self.book)
        self.assertIs(self.library.search_book(self.book.bookname), self.book)
    
    def test_remove_book(self):
        self.library.remove_book(self.book)
        self.assertIsNone(self.library.search_book(self.book.bookname))

    def test_search_book(self):
        self.library.add_book(self.book)
        self.assertIs(self.library.search_book(self.book.bookname), self.book)
