#!/usr/bin/env python
'''
Tests for :mod:`activity`
'''

# Standard imports:
import datetime
import unittest

# Project imports:
import importing


class parse_file_TestCase(unittest.TestCase):
    pass  # TODO


class parse_key_line_TestCase(unittest.TestCase):

    def test_debit_card(self):
        line = '''Details,Posting Date,Description,Amount,Type,Balance,Check or Slip #'''
        transaction_key = importing._parse_key_line(line)
        self.assertIsNotNone(transaction_key)
        self.assertEqual(4, transaction_key.type)
        self.assertEqual(None, transaction_key.trans_date)
        self.assertEqual(1, transaction_key.post_date)
        self.assertEqual(2, transaction_key.description)
        self.assertEqual(3, transaction_key.amount)

    def test_credit_card(self):
        line = '''Type,Trans Date,Post Date,Description,Amount'''
        transaction_key = importing._parse_key_line(line)
        self.assertIsNotNone(transaction_key)
        self.assertEqual(0, transaction_key.type)
        self.assertEqual(1, transaction_key.trans_date)
        self.assertEqual(2, transaction_key.post_date)
        self.assertEqual(3, transaction_key.description)
        self.assertEqual(4, transaction_key.amount)


class TransactionKeyTestCase(unittest.TestCase):
    pass  # TODO


class parse_line_TestCase(unittest.TestCase):

    debit_key = importing._parse_key_line(
        '''Details,Posting Date,Description,Amount,Type,Balance,Check or Slip #''')
    credit_key = importing._parse_key_line(
        '''Type,Trans Date,Post Date,Description,Amount''')

    def test_debit_card_at_trader_joes(self):
        line = '''DEBIT,09/07/2018,"POS DEBIT TRADER JOE'S # 123 HAPPY AZ",-10.80,MISC_DEBIT, ,,'''
        transaction = importing._parse_line(self.debit_key, line)
        self.assertIsNotNone(transaction)
        self.assertEqual('misc_debit', transaction.type)
        self.assertEqual(datetime.date(2018, 9, 7), transaction.post_date)
        self.assertEqual('''"POS DEBIT TRADER JOE'S # 123 HAPPY AZ"''', transaction.description)
        self.assertEqual(-10.80, transaction.amount)

    def test_credit_card_at_walgreens(self):
        line = '''Sale,09/05/2018,09/06/2018,WALGREENS #1234,-2.85'''
        transaction = importing._parse_line(self.credit_key, line)
        self.assertIsNotNone(transaction)
        self.assertEqual('sale', transaction.type)
        self.assertEqual(datetime.date(2018, 9, 5), transaction.trans_date)
        self.assertEqual(datetime.date(2018, 9, 6), transaction.post_date)
        self.assertEqual('''WALGREENS #1234''', transaction.description)
        self.assertEqual(-2.85, transaction.amount)

    def test_credit_card_with_comma_in_description(self):
        transaction = importing._parse_line(
            self.credit_key,
            '''Sale,08/18/2018,08/19/2018,THRIFT BOOKS GLOBAL, LLC,-43.87''')
        self.assertIsNotNone(transaction)
        self.assertEqual('sale', transaction.type)
        self.assertEqual(datetime.date(2018, 8, 18), transaction.trans_date)
        self.assertEqual(datetime.date(2018, 8, 19), transaction.post_date)
        self.assertEqual('THRIFT BOOKS GLOBAL, LLC', transaction.description)
        self.assertEqual(-43.87, transaction.amount)


class split_transaction_line_TestCase(unittest.TestCase):
    pass  # TODO


class parse_transaction_type_TestCase(unittest.TestCase):
    pass  # TODO


class parse_transaction_date_TestCase(unittest.TestCase):
    pass  # TODO


if __name__ == '__main__':
    unittest.main()
