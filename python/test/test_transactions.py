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

class loadTransactionsTestCase(unittest.TestCase):
    pass

class storeTransactionsTestCase(unittest.TestCase):
    pass

class TransactionTestCase(unittest.TestCase):

    def test_transDateAsString_None(self):
        transaction = transactions.Transaction()
        transaction.transDate = None
        self.assertIsNone(transaction.transDateAsString)

    def test_transDateAsString_realDate(self):
        transaction = transactions.Transaction()
        transaction.transDate = datetime.date(2018, 9, 11)
        self.assertEqual('2018-09-11', transaction.transDateAsString)

    def test_encode(self):
        souvenir = transactions.Transaction()
        souvenir.type = 'debit'
        souvenir.postDate = datetime.date(2018, 9, 7)
        souvenir.description = 'Fairyland Souvenir Shop'
        souvenir.amount = 12.34
        souvenir.tags = {}

        self.assertEqual({
                'type': 'debit',
                'transDate': None,
                'postDate': '2018-09-07',
                'description': 'Fairyland Souvenir Shop',
                'amount': 12.34,
                'tags': {},
                },
            souvenir.encode())

    def test_decode_tagsAsDict(self):
        '''
        Prove we can decode the tags in ``dict`` format, which has
        superseded the ``list`` format.
        '''

        transaction = transactions.Transaction.decode({
                'type': 'debit',
                'transDate': None,
                'postDate': '2018-09-07',
                'description': 'Fairyland Souvenir Shop',
                'amount': 12.34,
                'tags': {},
                })
        self.assertEqual('debit', transaction.type)
        self.assertIsNone(None, transaction.transDate)
        self.assertEqual(datetime.date(2018, 9, 7), transaction.postDate)
        self.assertEqual('Fairyland Souvenir Shop', transaction.description)
        self.assertEqual(12.34, transaction.amount)
        self.assertEqual({}, transaction.tags)

    def test_decode_tagsAsList(self):
        '''
        Prove we can still decode, even when the tags are a ``list``.
        '''

        transaction = transactions.Transaction.decode({
                'type': 'debit',
                'transDate': None,
                'postDate': '2018-09-07',
                'description': 'Fairyland Souvenir Shop',
                'amount': 12.34,
                'tags': [],
                })
        self.assertEqual('debit', transaction.type)
        self.assertIsNone(None, transaction.transDate)
        self.assertEqual(datetime.date(2018, 9, 7), transaction.postDate)
        self.assertEqual('Fairyland Souvenir Shop', transaction.description)
        self.assertEqual(12.34, transaction.amount)
        self.assertEqual({}, transaction.tags)

class dateAsStringTestCase(unittest.TestCase):
    pass

class parseTransactionDateTestCase(unittest.TestCase):

    def test_None(self):
        self.assertIsNone(transactions._parseTransactionDate(None))

    def test_realDate(self):
        self.assertEqual(
            datetime.date(2018, 9, 11),
            transactions._parseTransactionDate('2018-09-11'))

if __name__ == '__main__':
    unittest.main()
