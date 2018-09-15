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

class parseOptionsTestCase(unittest.TestCase):

    def test_noArgsRaises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parseOptions([])

    def test_invalidCommandRaises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parseOptions(['not-a-command'])

class parseOptionsTestCase_import(unittest.TestCase):

    def test_noArgsRaises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parseOptions(['import'])

    def test_withFile(self):
        with _captured_stderr():
            options = pecuniacli._parseOptions(['import', 'foo.csv'])
            self.assertEqual('import', options.command)
            self.assertEqual(['foo.csv'], options.inputFilePaths)

class parseOptionsTestCase_list(unittest.TestCase):

    def test_noArgs(self):
        options = pecuniacli._parseOptions(['list'])
        self.assertEqual('list', options.command)
        self.assertFalse(options.noTags)

    def test_noTags(self):
        options = pecuniacli._parseOptions(['list', '--no-tags'])
        self.assertEqual('list', options.command)
        self.assertTrue(options.noTags)

class parseOptionsTestCase_tags(unittest.TestCase):

    def test_noArgs(self):
        options = pecuniacli._parseOptions(['tags'])
        self.assertEqual('tags', options.command)
        self.assertIsNone(options.dates)

    def test_dates_noArg(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parseOptions(['tags', '--dates'])

    def test_dates_oneDate(self):
        options = pecuniacli._parseOptions(['tags', '--date=2018-09-14'])
        self.assertEqual(
            datetools.DateSequence([datetime.date(2018, 9, 14)]),
            options.dates)

    def test_dates_afterDate(self):
        options = pecuniacli._parseOptions(['tags', '--date=2018-09-14..'])
        self.assertEqual(
            datetools.DateSequence([
                    datetools.DateRange(datetime.date(2018, 9, 14), None),
                    ]),
            options.dates)

class parseOptionsTestCase_classify(unittest.TestCase):

    def test_noArgs(self):
        options = pecuniacli._parseOptions(['classify'])
        self.assertEqual('classify', options.command)
        self.assertFalse(options.noTags)
        self.assertIsNone(options.descriptionRegex)

    def test_noTags(self):
        options = pecuniacli._parseOptions(['classify', '--no-tags'])
        self.assertEqual('classify', options.command)
        self.assertTrue(options.noTags)
        self.assertIsNone(options.descriptionRegex)

    def test_descRegex(self):
        options = pecuniacli._parseOptions(['classify', '--desc-regex=foo'])
        self.assertEqual('classify', options.command)
        self.assertEqual('foo', options.descriptionRegex)

    def test_withFileRaises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parseOptions(['classify', 'foo.csv'])

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
