#!/usr/bin/env python
'''
Test for :mod:`datetools`
'''

# Standard imports:
import datetime
import unittest

# Project imports:
import datetools

class parseDateSequenceTestCase(unittest.TestCase):

    def test_None(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parseDateSequence(None)

    def test_emptyString(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parseDateSequence('')

    def test_commaOnly(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parseDateSequence(',')

    def test_oneDate(self):
        self.assertEqual(
            [datetime.date(2018, 9, 14)],
            datetools.parseDateSequence('2018-09-14'))

    def test_twoDates(self):
        self.assertEqual(
            [datetime.date(2018, 9, 13), datetime.date(2018, 9, 14)],
            datetools.parseDateSequence('2018-09-13,2018-09-14'))

    def test_oneDateRange(self):
        self.assertEqual(
            [(datetime.date(2018, 9, 13), datetime.date(2018, 9, 14))],
            datetools.parseDateSequence('2018-09-13..2018-09-14'))

class parseDateRangeTestCase(unittest.TestCase):

    def test_None(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parseDateRange(None)

    def test_emptyString(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parseDateRange('')

    def test_dotdotOnly(self):
        with self.assertRaises(datetools.DateParsingError) as context:
            datetools.parseDateRange('..')

    def test_noDotdots(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parseDateRange('2018-09-14')

    def test_tooManyDotdots(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parseDateRange('..2018-09-14..')

    def test_leadingDotdots(self):
        self.assertEqual(
            (None, datetime.date(2018, 9, 14)),
            datetools.parseDateRange('..2018-09-14'))

    def test_trailingDotdots(self):
        self.assertEqual(
            (datetime.date(2018, 9, 14), None),
            datetools.parseDateRange('2018-09-14..'))

class parseDateTestCase(unittest.TestCase):

    def test_None(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parseDate(None)

    def test_donuts(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parseDate('donuts')

    def test_2018_09_14(self):
        self.assertEqual(
            datetime.date(2018, 9, 14),
            datetools.parseDate('2018-09-14'))

if __name__ == '__main__':
    unittest.main()
