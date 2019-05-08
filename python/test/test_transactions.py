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


class load_TestCase(unittest.TestCase):
    pass


class store_TestCase(unittest.TestCase):
    pass


class TransactionTestCase(unittest.TestCase):

    def test_trans_date_as_string_None(self):
        x = transactions.Transaction()
        x.trans_date = None
        self.assertIsNone(x.trans_date_as_string)

    def test_trans_date_as_string_realDate(self):
        x = transactions.Transaction()
        x.trans_date = datetime.date(2018, 9, 11)
        self.assertEqual('2018-09-11', x.trans_date_as_string)

    def test_encode(self):
        souvenir = transactions.Transaction()
        souvenir.type = 'debit'
        souvenir.post_date = datetime.date(2018, 9, 7)
        souvenir.description = 'Fairyland Souvenir Shop'
        souvenir.amount = 12.34
        souvenir.tags = {}

        self.assertEqual(
            {
                'type': 'debit',
                'trans_date': None,
                'post_date': '2018-09-07',
                'description': 'Fairyland Souvenir Shop',
                'amount': 12.34,
                'tags': {},
            },
            souvenir.encode())

    def test_decode_tags_as_dict(self):
        '''
        Prove we can decode the tags in ``dict`` format, which has
        superseded the ``list`` format.
        '''

        x = transactions.Transaction.decode(
            {
                'type': 'debit',
                'trans_date': None,
                'post_date': '2018-09-07',
                'description': 'Fairyland Souvenir Shop',
                'amount': 12.34,
                'tags': {},
            })
        self.assertEqual('debit', x.type)
        self.assertIsNone(None, x.trans_date)
        self.assertEqual(datetime.date(2018, 9, 7), x.post_date)
        self.assertEqual('Fairyland Souvenir Shop', x.description)
        self.assertEqual(12.34, x.amount)
        self.assertEqual({}, x.tags)

    def test_decode_tags_as_list(self):
        '''
        Prove we can still decode, even when the tags are a ``list``.
        '''

        x = transactions.Transaction.decode(
            {
                'type': 'debit',
                'trans_date': None,
                'post_date': '2018-09-07',
                'description': 'Fairyland Souvenir Shop',
                'amount': 12.34,
                'tags': [],
            })
        self.assertEqual('debit', x.type)
        self.assertIsNone(None, x.trans_date)
        self.assertEqual(datetime.date(2018, 9, 7), x.post_date)
        self.assertEqual('Fairyland Souvenir Shop', x.description)
        self.assertEqual(12.34, x.amount)
        self.assertEqual({}, x.tags)


class parse_transaction_date_TestCase(unittest.TestCase):

    def test_None(self):
        self.assertIsNone(transactions._parse_transaction_date(None))

    def test_realDate(self):
        self.assertEqual(
            datetime.date(2018, 9, 11),
            transactions._parse_transaction_date('2018-09-11'))


if __name__ == '__main__':
    unittest.main()
