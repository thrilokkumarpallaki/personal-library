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

logger = logging.getLogger("PersonalLibrary")


if __name__ == '__main__':
    lms: LibrarySystem = LibrarySystem()
    
    lms.add_book(title="Rich Dad Poor Dad", author="Gausling", description="Decribes how to become a rich dad from poor data.", isbn="12345678")

    thrilok = lms.create_member(name="thrilok")
    book_name = "Rich Dad Poor Dad"

    book = thrilok.borrow_book(book_name)
    if book:
        print("I borrowed a book")
    else:
        print(f"No book found with the name: {book_name}")

    print("Iterate all the books in the library")
    


