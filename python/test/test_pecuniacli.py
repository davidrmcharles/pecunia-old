#!/usr/bin/env python
'''
Tests for :mod:`pecuniacli`
'''

# Standard imports
import contextlib
import datetime
import StringIO
import sys
import unittest

# Project imports:
import datetools
import pecuniacli


@contextlib.contextmanager
def _captured_stderr():
    errors = StringIO.StringIO()
    sys.stderr = errors
    try:
        yield errors
    finally:
        sys.stderr = sys.__stderr__


class mainTestCase(unittest.TestCase):
    pass


class parse_options_TestCase(unittest.TestCase):

    def test_no_args_raises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parse_options([])

    def test_invalid_command_raises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parse_options(['not-a-command'])


class parse_options_TestCase_import(unittest.TestCase):

    def test_no_args_raises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parse_options(['import'])

    def test_with_file(self):
        with _captured_stderr():
            options = pecuniacli._parse_options(['import', 'foo.csv'])
            self.assertEqual('import', options.command)
            self.assertEqual(['foo.csv'], options.inputFilePaths)


class parse_options_TestCase_list(unittest.TestCase):

    def test_no_args(self):
        options = pecuniacli._parse_options(['list'])
        self.assertEqual('list', options.command)
        self.assertIsNone(options.dates)
        self.assertEquals([], options.include_regexs)
        self.assertEquals([], options.exclude_regexs)
        self.assertFalse(options.no_tags)
        self.assertFalse(options.print_total)

    def test_dates(self):
        options = pecuniacli._parse_options(['list', '--dates=2019-05-03'])
        self.assertEqual('list', options.command)
        self.assertEqual(
            datetools.DateSequence([datetools.parse_date('2019-05-03')]),
            options.dates
        )

    def test_include(self):
        options = pecuniacli._parse_options(['list', '--include=foo'])
        self.assertEqual('list', options.command)
        self.assertEqual(['foo'], options.include_regexs)

    def test_exclude(self):
        options = pecuniacli._parse_options(['list', '--exclude=foo'])
        self.assertEqual('list', options.command)
        self.assertEqual(['foo'], options.exclude_regexs)

    def test_exclude_twice(self):
        options = pecuniacli._parse_options([
            'list', '--exclude=foo', '--exclude=bar'])
        self.assertEqual('list', options.command)
        self.assertEqual(['foo', 'bar'], options.exclude_regexs)

    @unittest.skip('TODO')
    def test_include_and_exclude_raises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parse_options([
                    'list', '--include=foo', '--exclude=foo'])

    def test_no_tags(self):
        options = pecuniacli._parse_options(['list', '--no-tags'])
        self.assertEqual('list', options.command)
        self.assertTrue(options.no_tags)

    def test_print(self):
        options = pecuniacli._parse_options(['list', '--total'])
        self.assertEqual('list', options.command)
        self.assertTrue(options.print_total)


class parse_options_TestCase_tags(unittest.TestCase):

    def test_no_args(self):
        options = pecuniacli._parse_options(['tags'])
        self.assertEqual('tags', options.command)
        self.assertIsNone(options.dates)

    def test_dates_no_arg(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parse_options(['tags', '--dates'])

    def test_dates_one_date(self):
        options = pecuniacli._parse_options(['tags', '--date=2018-09-14'])
        self.assertEqual(
            datetools.DateSequence([datetime.date(2018, 9, 14)]),
            options.dates)

    def test_dates_after_date(self):
        options = pecuniacli._parse_options(['tags', '--date=2018-09-14..'])
        self.assertEqual(
            datetools.DateSequence([
                    datetools.DateRange(datetime.date(2018, 9, 14), None),
            ]),
            options.dates)


class parse_options_TestCase_classify(unittest.TestCase):

    def test_no_args(self):
        options = pecuniacli._parse_options(['classify'])
        self.assertEqual('classify', options.command)
        self.assertFalse(options.no_tags)
        self.assertEquals([], options.include_regexs)

    def test_no_tags(self):
        options = pecuniacli._parse_options(['classify', '--no-tags'])
        self.assertEqual('classify', options.command)
        self.assertTrue(options.no_tags)
        self.assertEquals([], options.include_regexs)

    def test_include_regexs(self):
        options = pecuniacli._parse_options(['classify', '--include=foo'])
        self.assertEqual('classify', options.command)
        self.assertEqual(['foo'], options.include_regexs)

    def test_with_file_raises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parse_options(['classify', 'foo.csv'])


class createOptionParserTestCase(unittest.TestCase):
    pass


class importTransactionsTestCase(unittest.TestCase):
    pass


class listTransactionsTestCase(unittest.TestCase):
    pass


class TransactionOneLineFormatterTestCase(unittest.TestCase):
    pass


class classifyTransactionsTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
