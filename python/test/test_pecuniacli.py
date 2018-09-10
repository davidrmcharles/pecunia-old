#!/usr/bin/env python
'''
Tests for :mod:`pecunia`
'''

# Standard imports
import unittest

# Project imports:
import pecuniacli

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

if __name__ == '__main__':
    unittest.main()
