#!/usr/bin/env python
'''
Test for :mod:`datetools`
'''

# Standard imports:
import datetime
import inspect
import os
import shutil
import sys
import traceback
import unittest

# Project imports:
import datetools


_this_file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
_this_folder_path = os.path.dirname(_this_file_path)
_python_folder_path = os.path.dirname(_this_folder_path)
_root_folder_path = os.path.dirname(_python_folder_path)
_build_folder_path = os.path.join(_root_folder_path, 'build')


class parse_date_file_TestCase(unittest.TestCase):

    def test_empty(self):
        test_file_path = self._create_test_file('')
        self.assertEqual(
            datetools.DateSequence([]),
            datetools.parse_date_sequence_file(test_file_path)
        )

    def test_single_date_without_trailing_newline(self):
        test_file_path = self._create_test_file('2019-05-21')
        self.assertEqual(
            datetools.parse_date_sequence('2019-05-21'),
            datetools.parse_date_sequence_file(test_file_path)
        )

    def test_single_date_with_trailing_newline(self):
        test_file_path = self._create_test_file('2019-05-21\n')
        self.assertEqual(
            datetools.parse_date_sequence('2019-05-21'),
            datetools.parse_date_sequence_file(test_file_path)
        )

    def test_two_dates_on_same_line(self):
        test_file_path = self._create_test_file('2019-05-21,2019-05-22')
        self.assertEqual(
            datetools.parse_date_sequence('2019-05-21,2019-05-22'),
            datetools.parse_date_sequence_file(test_file_path)
        )

    def test_two_dates_on_separate_lines(self):
        test_file_path = self._create_test_file('2019-05-21\n2019-05-22')
        self.assertEqual(
            datetools.parse_date_sequence('2019-05-21,2019-05-22'),
            datetools.parse_date_sequence_file(test_file_path)
        )

    def _create_test_file(self, content):
        test_folder_path = self._create_test_folder()
        test_file_path = os.path.join(test_folder_path, 'date.txt')
        with open(test_file_path, 'w') as test_file:
            test_file.write(content)
        return test_file_path

    def _create_test_folder(self):
        class_name = self.__class__.__name__
        method_name = traceback.extract_stack(None, 2)[0][2]
        path = os.path.join(_build_folder_path, class_name, method_name)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        return path


class parse_date_sequence_TestCase(unittest.TestCase):

    def test_none(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parse_date_sequence(None)

    def test_empty_string(self):
        self.assertEqual(
            datetools.DateSequence([]),
            datetools.parse_date_sequence('')
        )

    def test_comma_only(self):
        self.assertEqual(
            datetools.DateSequence([]),
            datetools.parse_date_sequence(',')
        )

    def test_one_date(self):
        self.assertEqual(
            datetools.DateSequence([datetime.date(2018, 9, 14)]),
            datetools.parse_date_sequence('2018-09-14'))

    def test_two_dates(self):
        self.assertEqual(
            datetools.DateSequence(
                [datetime.date(2018, 9, 13), datetime.date(2018, 9, 14)]),
            datetools.parse_date_sequence('2018-09-13,2018-09-14'))

    def test_one_date_range(self):
        self.assertEqual(
            datetools.DateSequence([
                    datetools.DateRange(
                        datetime.date(2018, 9, 13),
                        datetime.date(2018, 9, 14))]),
            datetools.parse_date_sequence('2018-09-13..2018-09-14'))


class parse_date_range_TestCase(unittest.TestCase):

    def test_None(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parse_date_range(None)

    def test_emptyString(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parse_date_range('')

    def test_dotdotOnly(self):
        with self.assertRaises(datetools.DateParsingError) as context:
            datetools.parse_date_range('..')

    def test_noDotdots(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parse_date_range('2018-09-14')

    def test_tooManyDotdots(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parse_date_range('..2018-09-14..')

    def test_leadingDotdots(self):
        self.assertEqual(
            datetools.DateRange(None, datetime.date(2018, 9, 14)),
            datetools.parse_date_range('..2018-09-14'))

    def test_trailingDotdots(self):
        self.assertEqual(
            datetools.DateRange(datetime.date(2018, 9, 14), None),
            datetools.parse_date_range('2018-09-14..'))

    def test_adjacentDates(self):
        self.assertEqual(
            datetools.DateRange(
                datetime.date(2018, 9, 14),
                datetime.date(2018, 9, 15)),
            datetools.parse_date_range('2018-09-14..2018-09-15'))

    def test_reversedAdjacentdates(self):
        with self.assertRaises(datetools.InvalidDateRange):
            datetools.parse_date_range('2018-09-15..2018-09-14')


class parse_date_TestCase(unittest.TestCase):

    def test_None(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parse_date(None)

    def test_donuts(self):
        with self.assertRaises(datetools.DateParsingError):
            datetools.parse_date('donuts')

    def test_2018_09_14(self):
        self.assertEqual(
            datetime.date(2018, 9, 14),
            datetools.parse_date('2018-09-14'))


class date_as_string_TestCase(unittest.TestCase):
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
