#!/usr/bin/env python
'''
Tests for :mod:`filtering`
'''

# Standard imports:
import unittest

# Project imports
import filtering

class filterTransactionsTestCase(unittest.TestCase):

    def test_emptyListAndNoOptions(self):
        filtering.filterTransactions([], None)

class filterTransactionsWithNonMatchingDates(unittest.TestCase):
    pass

class filterTransactionsWithNonMatchingDescriptions(unittest.TestCase):
    pass

class filterTransactionsWithoutTagsTestCase(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
