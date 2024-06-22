import unittest


from personal_library.tests.test_book import BookTest


suite = unittest.TestSuite()

suite.addTest(BookTest)

suite.run()


