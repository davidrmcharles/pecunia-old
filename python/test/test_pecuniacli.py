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

    def test_noArgsRaises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parse_options([])

    def test_invalidCommandRaises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parse_options(['not-a-command'])


class parse_options_TestCase_import(unittest.TestCase):

    def test_noArgsRaises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parse_options(['import'])

    def test_withFile(self):
        with _captured_stderr():
            options = pecuniacli._parse_options(['import', 'foo.csv'])
            self.assertEqual('import', options.command)
            self.assertEqual(['foo.csv'], options.inputFilePaths)


class parse_options_TestCase_list(unittest.TestCase):

    def test_noArgs(self):
        options = pecuniacli._parse_options(['list'])
        self.assertEqual('list', options.command)
        self.assertFalse(options.noTags)

    def test_noTags(self):
        options = pecuniacli._parse_options(['list', '--no-tags'])
        self.assertEqual('list', options.command)
        self.assertTrue(options.noTags)

    def test_total(self):
        options = pecuniacli._parse_options(['list', '--total'])
        self.assertEqual('list', options.command)
        self.assertTrue(options.printTotal)


class parse_options_TestCase_tags(unittest.TestCase):

    def test_noArgs(self):
        options = pecuniacli._parse_options(['tags'])
        self.assertEqual('tags', options.command)
        self.assertIsNone(options.dates)

    def test_dates_noArg(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parse_options(['tags', '--dates'])

    def test_dates_oneDate(self):
        options = pecuniacli._parse_options(['tags', '--date=2018-09-14'])
        self.assertEqual(
            datetools.DateSequence([datetime.date(2018, 9, 14)]),
            options.dates)

    def test_dates_afterDate(self):
        options = pecuniacli._parse_options(['tags', '--date=2018-09-14..'])
        self.assertEqual(
            datetools.DateSequence([
                    datetools.DateRange(datetime.date(2018, 9, 14), None),
                    ]),
            options.dates)


class parse_options_TestCase_classify(unittest.TestCase):

    def test_noArgs(self):
        options = pecuniacli._parse_options(['classify'])
        self.assertEqual('classify', options.command)
        self.assertFalse(options.noTags)
        self.assertIsNone(options.descriptionRegex)

    def test_noTags(self):
        options = pecuniacli._parse_options(['classify', '--no-tags'])
        self.assertEqual('classify', options.command)
        self.assertTrue(options.noTags)
        self.assertIsNone(options.descriptionRegex)

    def test_descRegex(self):
        options = pecuniacli._parse_options(['classify', '--desc-regex=foo'])
        self.assertEqual('classify', options.command)
        self.assertEqual('foo', options.descriptionRegex)

    def test_withFileRaises(self):
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
