import unittest
from unittest import TestCase

from personal_library.book import Book

class BookTest(TestCase):
    def setUp(self) -> None:
        self.book = Book(title="my book", author="thrilok pallaki", isbn="123456", description="This is my book.")
    def test_book_creation(self):
        self.assertIsInstance(self.book, Book)

    def test_bookname(self):
        self.assertEqual(self.book.bookname, "my book")

    def test_authorname(self):
        self.assertEqual(self.book.author, "thrilok pallaki")

    def test_book_isbn(self):
        self.assertEqual(self.book.isbn, "123456")

    def test_change_bookname(self):
        self.book.bookname = "My New Book"
        self.assertEqual(self.book.bookname, "My New Book")

    def test_change_authorname(self):
        self.book.author = "Thrilok Kumar Reddy Pallaki"
        self.assertEqual(self.book.author, "Thrilok Kumar Reddy Pallaki")

    def test_change_description(self):
        self.book.description = "This is my book. It has my rules."
        self.assertEqual(self.book.description, "This is my book. It has my rules.")

    def test_change_isbn(self):
        self.book.isbn = "0987654"
        self.assertEqual(self.book.isbn, "0987654")

    def tearDown(self) -> None:
        del self.book
