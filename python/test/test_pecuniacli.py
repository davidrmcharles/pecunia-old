#!/usr/bin/env python
'''
Tests for :mod:`pecunia`
'''

# Standard imports
import unittest

# Project imports:
import pecuniacli

class mainTestCase(unittest.TestCase):
    pass

class parseOptionsTestCase(unittest.TestCase):

    def test_noArgsRaises(self):
        with self.assertRaises(SystemExit):
            pecuniacli._parseOptions([])

    def test_importCommand(self):
        with self.assertRaises(SystemExit):
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
            pecuniacli._parseOptions(['not-a-command'])

    def test_importCommandWithFile(self):
        options = pecuniacli._parseOptions(['import', 'foo.csv'])
        self.assertEqual('import', options.command)
        self.assertEqual(['foo.csv'], options.inputFilePaths)

    def test_classifyCommandWithFile(self):
        with self.assertRaises(SystemExit):
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

if __name__ == '__main__':
    unittest.main()
