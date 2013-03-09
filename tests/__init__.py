import unittest

from .jsonutil_test import JSONTestCase
from .firebase_test import FirebaseTestCase


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(JSONTestCase))
    suite.addTest(unittest.makeSuite(FirebaseTestCase))
    return suite
