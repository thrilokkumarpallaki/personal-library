import unittest

from personal_library.library_system import LibrarySystem
from personal_library.book import Book
from personal_library.member import Member


class LibrarySystemTest(unittest.TestCase):
    def setUp(self) -> None:
        self.book = Book(title="My Book", author="Thrilok Pallaki", description="This is my new book", isbn="12345678")
        self.lms: LibrarySystem = LibrarySystem()

    def test_add_book(self):
        self.assertIsInstance(self.lms.add_book(title="My Book", author="Thrilok Pallaki", description="This is my new book", isbn="12345678"), Book)
    
    def test_add_member(self):
        member = self.lms.create_member(name="Thrilok")
        self.assertIsInstance(member, Member)
    
    @unittest.skip("Not implemented")
    def test_remove_member(self):
        pass

    def test_remove_book(self):
        removed_book = self.lms.remove_book(self.book)
        self.assertIsInstance(removed_book, Book)

    def test_remove_invalid_book(self):
        book = Book(title="My New Book", author="Thrilok Pallaki", description="This is my new book", isbn="123456789")
        self.assertIsNone(self.lms.remove_book(book))

    def test_search_book(self):
        book = self.lms.add_book(title="My Third Book", author="Thrilok Pallaki", description="This is my Third book", isbn="1234589")
        self.assertEqual(self.lms.search_book(book.bookname), book)

    def test_search_invalid_book(self):
        self.assertIsNone(self.lms.search_book("Hello World!"))


    def test_borrow_book(self):
        member = Member(name="Thrilok Pallaki")
        book = self.lms.borrow_book(member, self.book)
        self.assertIsInstance(book, Book)