import logging
import sys
import os



current_dir_path = os.path.dirname(os.path.abspath(__name__))


if current_dir_path not in sys.path:
    sys.path.insert(0, current_dir_path)

from logger import setup_logging

setup_logging()

from library_system import LibrarySystem
from personal_library.member.user import Member
from personal_library.exceptions import BookBorrowedAlready

logger = logging.getLogger("PersonalLibrary")


if __name__ == '__main__':
    lms: LibrarySystem = LibrarySystem()
    
    lms.add_book(title="Rich Dad Poor Dad", author="Gausling", description="Decribes how to become a rich dad from poor data.", isbn="12345678")

    thrilok = lms.create_member(name="thrilok")
    book_name = "Rich Dad Poor Dad"
    book = lms.search_book(book_name)
    borrowed_book = lms.borrow_book(thrilok, book)
    if borrowed_book:
        print("I borrowed a book")
    else:
        print(f"No book found with the name: {book_name}")


    try:
        lms.return_book(thrilok, borrowed_book)
    except BookBorrowedAlready as e:
        print("Book already borrowed by you.")
    
    


