import unittest

from personal_library.member import Member
from personal_library.book import Book
from personal_library.library_system import LibrarySystem
from personal_library.exceptions import BookNotFound, InvalidBook


class MemberTest(unittest.TestCase):
    def setUp(self) -> None:
        self.lms: LibrarySystem = LibrarySystem()
        self.book = self.lms.add_book(title="My Book", author="Thrilok Pallaki", description="This is my new book", isbn="12345678")
        self.user = Member(name="Thrilok")

    def test_user_creation(self):
        self.assertIsInstance(self.user, Member)

    def test_username(self):
        self.assertEqual(self.user.username, "Thrilok")

    def test_borrow_book(self):
        book = self.user.borrow_book(self.book)
        self.assertIsInstance(book, Book)

    def test_list_borrowed_books(self):
        borrowed_books = self.user.borrowed_books
        self.assertEqual(len(borrowed_books), 0)

    def test_return_book(self):
        book = self.user.borrow_book(self.book)
        book_returned = self.user.return_book(book)
        self.assertTrue(book_returned, "Book Returned successfully.")

    def test_return_invalid_book(self):
        unknow_book = Book(title="Unknown Book", author="Unknow Author", description="Unknown Desc", isbn="Unknown Isbn")
        self.assertRaises(InvalidBook, self.user.return_book, book=unknow_book)
    
    def tearDown(self) -> None:
        self.lms.remove_book(self.book)
    