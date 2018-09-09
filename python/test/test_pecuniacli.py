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
        options = pecuniacli._parseOptions(['import'])
        self.assertEqual('import', options.command)

    def test_classifyCommand(self):
        options = pecuniacli._parseOptions(['classify'])
        self.assertEqual('classify', options.command)

    def test_invalidCommandRaises(self):
        with self.assertRaises(SystemExit):
            pecuniacli._parseOptions(['not-a-command'])

if __name__ == '__main__':
    unittest.main()
