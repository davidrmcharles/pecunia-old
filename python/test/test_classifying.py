#!/usr/bin/env python
'''
Tests for :mod:`classifying`
'''

# Standard imports:
import unittest

# Project imports:
import classifying

class classifyInteractivelyTestCase(unittest.TestCase):
    pass

class handleUserInputTestCase(unittest.TestCase):
    pass

class parseTagTestCase(unittest.TestCase):

    def test_plainTag(self):
        self.assertEqual(
            {'food': None}, classifying._parseTag('food'))

    def test_tagWithSplit(self):
        self.assertEqual(
            {'cash': 20.00}, classifying._parseTag('cash:20.00'))

    @unittest.skip('TODO')
    def test_tagWithSplitThatIsNotANumber(self):
        self.assertEqual(
            {}, classifying._parseTag('cash:money'))

if __name__ == '__main__':
    unittest.main()
