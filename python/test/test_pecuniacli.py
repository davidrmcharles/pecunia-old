#!/usr/bin/env python
'''
Tests for :mod:`pecuniacli`
'''

# Standard imports
import contextlib
import StringIO
import sys
import unittest

# Project imports:
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

    def test_importCommand(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parseOptions(['import'])

    def test_classifyCommand(self):
        options = pecuniacli._parseOptions(['classify'])
        self.assertEqual('classify', options.command)
        self.assertFalse(options.noTags)
        self.assertIsNone(options.descriptionRegex)

    def test_classifyCommandNoTags(self):
        options = pecuniacli._parseOptions(['classify', '--no-tags'])
        self.assertEqual('classify', options.command)
        self.assertTrue(options.noTags)
        self.assertIsNone(options.descriptionRegex)

    def test_classifyCommandDescriptionRegex(self):
        options = pecuniacli._parseOptions(['classify', '--desc-regex=foo'])
        self.assertEqual('classify', options.command)
        self.assertEqual('foo', options.descriptionRegex)

    def test_invalidCommandRaises(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parseOptions(['not-a-command'])

    def test_importCommandWithFile(self):
        with _captured_stderr():
            options = pecuniacli._parseOptions(['import', 'foo.csv'])
            self.assertEqual('import', options.command)
            self.assertEqual(['foo.csv'], options.inputFilePaths)

    def test_classifyCommandWithFile(self):
        with self.assertRaises(SystemExit):
            with _captured_stderr():
                pecuniacli._parseOptions(['classify', 'foo.csv'])

class createOptionParserTestCase(unittest.TestCase):
    pass

class importTransactionsTestCase(unittest.TestCase):
    pass

class storeTransactionsTestCase(unittest.TestCase):
    pass

class classifyTransactionsTestCase(unittest.TestCase):
    pass

class loadTransactionsTestCase(unittest.TestCase):
    pass

class formatTransactionsTestCase(unittest.TestCase):
    pass

class filterTransactionsTestCase(unittest.TestCase):
    pass

class filterTransactionsWithoutTagsTestCase(unittest.TestCase):
    pass

class filterTransactionsWithNonMatchingDescriptions(unittest.TestCase):
    pass

class handleUserInputTestCase(unittest.TestCase):
    pass

class parseTagTestCase(unittest.TestCase):

    def test_plainTag(self):
        self.assertEqual(
            {'food': None}, pecuniacli._parseTag('food'))

    def test_tagWithSplit(self):
        self.assertEqual(
            {'cash': 20.00}, pecuniacli._parseTag('cash:20.00'))

    @unittest.skip('TODO')
    def test_tagWithSplitThatIsNotANumber(self):
        self.assertEqual(
            {}, pecuniacli._parseTag('cash:money'))

if __name__ == '__main__':
    unittest.main()
