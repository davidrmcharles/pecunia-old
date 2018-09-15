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
            datetools.DateSequence([datetime.date(2018, 9, 14)]),
            datetools.parseDateSequence('2018-09-14'))

    def test_twoDates(self):
        self.assertEqual(
            datetools.DateSequence(
                [datetime.date(2018, 9, 13), datetime.date(2018, 9, 14)]),
            datetools.parseDateSequence('2018-09-13,2018-09-14'))

    def test_oneDateRange(self):
        self.assertEqual(
            datetools.DateSequence([
                    datetools.DateRange(
                        datetime.date(2018, 9, 13),
                        datetime.date(2018, 9, 14))]),
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
            datetools.DateRange(None, datetime.date(2018, 9, 14)),
            datetools.parseDateRange('..2018-09-14'))

    def test_trailingDotdots(self):
        self.assertEqual(
            datetools.DateRange(datetime.date(2018, 9, 14), None),
            datetools.parseDateRange('2018-09-14..'))

    def test_adjacentDates(self):
        self.assertEqual(
            datetools.DateRange(
                datetime.date(2018, 9, 14),
                datetime.date(2018, 9, 15)),
            datetools.parseDateRange('2018-09-14..2018-09-15'))

    def test_reversedAdjacentdates(self):
        with self.assertRaises(datetools.InvalidDateRange):
            datetools.parseDateRange('2018-09-15..2018-09-14')

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

class dateAsStringTestCase(unittest.TestCase):
    pass

class DateSequenceTestCase_contains(unittest.TestCase):

    def test_None(self):
        with self.assertRaises(TypeError):
            None in datetools.DateSequence([])

class DateRangeTestCase_contains(unittest.TestCase):

    def test_None(self):
        with self.assertRaises(TypeError):
            None in datetools.DateRange(
                datetime.date(2018, 9, 12),
                datetime.date(2018, 9, 14))

    def test_middleOfBoundedRange(self):
        self.assertTrue(
            datetime.date(2018, 9, 13) in datetools.DateRange(
                datetime.date(2018, 9, 12),
                datetime.date(2018, 9, 14)))

    def test_firstOfBoundedRange(self):
        self.assertTrue(
            datetime.date(2018, 9, 12) in datetools.DateRange(
                datetime.date(2018, 9, 12),
                datetime.date(2018, 9, 14)))

    def test_lastOfBoundedRange(self):
        self.assertTrue(
            datetime.date(2018, 9, 14) in datetools.DateRange(
                datetime.date(2018, 9, 12),
                datetime.date(2018, 9, 14)))

    def test_beforeFirstOfBoundedRange(self):
        self.assertFalse(
            datetime.date(2018, 9, 11) in datetools.DateRange(
                datetime.date(2018, 9, 12),
                datetime.date(2018, 9, 14)))

    def test_afterLstOfBoundedRange(self):
        self.assertFalse(
            datetime.date(2018, 9, 15) in datetools.DateRange(
                datetime.date(2018, 9, 12),
                datetime.date(2018, 9, 14)))

    def test_beforeLastOfOpenFirstRange(self):
        self.assertTrue(
            datetime.date(2018, 9, 13) in datetools.DateRange(
                None,
                datetime.date(2018, 9, 14)))

    def test_onLastOfOpenFirstRange(self):
        self.assertTrue(
            datetime.date(2018, 9, 14) in datetools.DateRange(
                None,
                datetime.date(2018, 9, 14)))

    def test_afterLastOfOpenFirstRange(self):
        self.assertFalse(
            datetime.date(2018, 9, 15) in datetools.DateRange(
                None,
                datetime.date(2018, 9, 14)))

    def test_afterFirstOfOpenLastRange(self):
        self.assertTrue(
            datetime.date(2018, 9, 13) in datetools.DateRange(
                datetime.date(2018, 9, 12),
                None))

    def test_onFirstOfOpenLastRange(self):
        self.assertTrue(
            datetime.date(2018, 9, 12) in datetools.DateRange(
                datetime.date(2018, 9, 12),
                None))

    def test_beforeFirstOfOpenLastRange(self):
        self.assertFalse(
            datetime.date(2018, 9, 11) in datetools.DateRange(
                datetime.date(2018, 9, 12),
                None))

if __name__ == '__main__':
    unittest.main()
