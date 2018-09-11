#!/usr/bin/env python
'''
About transactions

:class:`Transaction`
'''

class Transaction(object):
    '''
    A single account-activity event
    '''

    def __init__(self):
        self.type = None
        self.transDate = None
        self.postDate = None
        self.description = None
        self.amount = None
        self.tags = []

    @property
    def transDateAsString(self):
        return '%04d-%02d-%02d' % (
            self.transDate.year,
            self.transDate.month,
            self.transDate.day
            )

    @property
    def postDateAsString(self):
        return '%04d-%02d-%02d' % (
            self.postDate.year,
            self.postDate.month,
            self.postDate.day
            )

    @property
    def jsonEncodable(self):
        transDate = self.transDate
        if transDate is not None:
            transDate = self.transDateAsString

        postDate = self.postDate
        if postDate is not None:
            postDate = self.postDateAsString
        return {
            'type': self.type,
            'transDate': transDate,
            'postDate': postDate,
            'description': self.description,
            'amount': self.amount,
            'tags': self.tags,
            }

    @staticmethod
    def createFromJson(jsonDecodable):
        t = Transaction()
        t.type = jsonDecodable['type']

        if t.transDate is not None:
            t.transDate = _parseTransactionDate(jsonDecodable['transDate'])
        if t.postDate is not None:
            t.postDate = _parseTransaactionDate(jsonDecodable['postDate'])

        t.description = jsonDecodable['description']
        t.amount = jsonDecodable['amount']
        if 'tags' in jsonDecodable:
            t.tags = jsonDecodable['tags']
        return t

def _parseTransactionDate(s):
    month, day, year = s.split('-')
    return datetime.date(int(year), int(month), int(day))

def _cumulativeCredits(transactions):
    credits_ = 0.0
    for transaction in transactions:
        if transaction.amount > 0.0:
            credits_ += transaction.amount
    return credits_

def _cumulativeDebits(transactions):
    debits = 0.0
    for transaction in transactions:
        if transaction.amount < 0.0:
            debits += transaction.amount
    return debits

def _creditVelocity(transactions):
    minPostDate = min(transactions, key=lambda t: t.postDate).postDate
    maxPostDate = max(transactions, key=lambda t: t.postDate).postDate
    numberOfDays = (maxPostDate - minPostDate).days
    return _cumulativeCredits(transactions) / float(numberOfDays)

def _debitVelocity(transactions):
    minPostDate = min(transactions, key=lambda t: t.postDate).postDate
    maxPostDate = max(transactions, key=lambda t: t.postDate).postDate
    numberOfDays = (maxPostDate - minPostDate).days
    return _cumulativeDebits(transactions) / float(numberOfDays)
