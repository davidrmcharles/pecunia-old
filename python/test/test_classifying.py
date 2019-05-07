#!/usr/bin/env python
'''
Tests for :mod:`classifying`
'''

# Standard imports:
import unittest

# Project imports:
import classifying


class classify_interactively_TestCase(unittest.TestCase):
    pass


class handle_user_input_TestCase(unittest.TestCase):
    pass


class parse_tag_TestCase(unittest.TestCase):

    def test_plain_tag(self):
        self.assertEqual(
            {'food': None}, classifying._parse_tag('food'))

    def test_tag_with_split(self):
        self.assertEqual(
            {'cash': 20.00}, classifying._parse_tag('cash:20.00'))

    @unittest.skip('TODO')
    def test_tag_with_split_that_is_not_a_number(self):
        self.assertEqual(
            {}, classifying._parse_tag('cash:money'))


if __name__ == '__main__':
    unittest.main()
