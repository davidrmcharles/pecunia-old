#!/usr/bin/env python
'''
Tests for :mod:`activity`
'''

# Standard imports:
import datetime
import unittest

# Project imports:
import activity

class parseFileTestCase(unittest.TestCase):
    pass  # TODO

class parseKeyLineTestCase(unittest.TestCase):

    def test_debitCard(self):
        line = '''Details,Posting Date,Description,Amount,Type,Balance,Check or Slip #'''
        transactionKey = activity.parseKeyLine(line)
        self.assertIsNotNone(transactionKey)
        self.assertEqual(4, transactionKey.type)
        self.assertEqual(None, transactionKey.transDate)
        self.assertEqual(1, transactionKey.postDate)
        self.assertEqual(2, transactionKey.description)
        self.assertEqual(3, transactionKey.amount)

    def test_creditCard(self):
        line = '''Type,Trans Date,Post Date,Description,Amount'''
        transactionKey = activity.parseKeyLine(line)
        self.assertIsNotNone(transactionKey)
        self.assertEqual(0, transactionKey.type)
        self.assertEqual(1, transactionKey.transDate)
        self.assertEqual(2, transactionKey.postDate)
        self.assertEqual(3, transactionKey.description)
        self.assertEqual(4, transactionKey.amount)

class TransactionKeyTestCase(unittest.TestCase):
    pass  # TODO

class parseLineTestCase(unittest.TestCase):

    debitKey = activity.parseKeyLine(
        '''Details,Posting Date,Description,Amount,Type,Balance,Check or Slip #''')
    creditKey = activity.parseKeyLine(
        '''Type,Trans Date,Post Date,Description,Amount''')

    def test_debitCardAtTraderJoes(self):
        line = '''DEBIT,09/07/2018,"POS DEBIT                TRADER JOE'S # 123        HAPPY        AZ",-10.80,MISC_DEBIT, ,,'''
        transaction = activity.parseLine(self.debitKey, line)
        self.assertIsNotNone(transaction)
        self.assertEqual('debit', transaction.type)
        self.assertEqual(datetime.date(2018, 9, 7), transaction.postDate)
        self.assertEqual('''"POS DEBIT                TRADER JOE'S # 123        HAPPY        AZ"''', transaction.description)
        self.assertEqual(-10.80, transaction.amount)

    def test_creditCardAtWalgreens(self):
        line = '''Sale,09/05/2018,09/06/2018,WALGREENS #1234,-2.85'''
        transaction = activity.parseLine(self.creditKey, line)
        self.assertIsNotNone(transaction)
        self.assertEqual('debit', transaction.type)
        self.assertEqual(datetime.date(2018, 9, 5), transaction.transDate)
        self.assertEqual(datetime.date(2018, 9, 6), transaction.postDate)
        self.assertEqual('''WALGREENS #1234''', transaction.description)
        self.assertEqual(-2.85, transaction.amount)

    def test_creditCardWithCommaInDescription(self):
        transaction = activity.parseLine(
            self.creditKey,
            '''Sale,08/18/2018,08/19/2018,THRIFT BOOKS GLOBAL, LLC,-43.87''')
        self.assertIsNotNone(transaction)
        self.assertEqual('debit', transaction.type)
        self.assertEqual(datetime.date(2018, 8, 18), transaction.transDate)
        self.assertEqual(datetime.date(2018, 8, 19), transaction.postDate)
        self.assertEqual('THRIFT BOOKS GLOBAL, LLC', transaction.description)
        self.assertEqual(-43.87, transaction.amount)

class splitTransactionLineTestCase(unittest.TestCase):
    pass  # TODO

class parseTransactionTypeTestCase(unittest.TestCase):
    pass  # TODO

class parseTransactionDateTestCase(unittest.TestCase):
    pass  # TODO

if __name__ == '__main__':
    unittest.main()
