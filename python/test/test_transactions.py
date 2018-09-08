#!/usr/bin/env python
'''
Tests for :mod:`transactions`
'''

# Standard imports:
import datetime
import json
import unittest

# Project imports:
import transactions

class TransactionTestCase(unittest.TestCase):

    def test_jsonEncodable(self):
        souvenir = transactions.Transaction()
        souvenir.type = 'debit'
        souvenir.postDate = datetime.date(2018, 9, 7)
        souvenir.description = 'Fairyland Souvenir Shop'
        souvenir.amount = 12.34

        self.assertEqual({
                'type': 'debit',
                'transDate': None,
                'postDate': '2018-09-07',
                'description': 'Fairyland Souvenir Shop',
                'amount': 12.34
                },
            souvenir.jsonEncodable)

if __name__ == '__main__':
    unittest.main()
