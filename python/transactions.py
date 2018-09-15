#!/usr/bin/env python
'''
About transactions

:func:`load`
:func:`store`
:func:`cacheFilePath`
:class:`Transaction`
'''

# Standard imports:
import datetime
import inspect
import json
import os

_thisFilePath = inspect.getfile(inspect.currentframe())
_thisFolderPath = os.path.abspath(os.path.dirname(_thisFilePath))
_rootFolderPath = os.path.dirname(_thisFolderPath)
_cacheFilePath = os.path.join(
    _rootFolderPath, 'private', 'transactions.json')

def load():
    with open(_cacheFilePath, 'r') as cacheFile:
        jsonDecodables = json.load(cacheFile)
        transactions = [
            Transaction.createFromJson(jsonDecodable)
            for jsonDecodable in jsonDecodables
            ]
    transactions.sort(key=lambda t: t.date, reverse=True)
    return transactions

def store(transactions):
    outputFilePath = os.path.join(
        _rootFolderPath, 'private', 'transactions.json')
    with open(outputFilePath, 'w') as outputFile:
        json.dump(
            [t.jsonEncodable for t in transactions],
            outputFile,
            indent=4)

def cacheFilePath():
    return _cacheFilePath

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
        self.tags = {}

    @property
    def date(self):
        if self.transDate is not None:
            return self.transDate
        elif self.postDate is not None:
            return self.postDate
        return None

    @property
    def dateAsString(self):
        if self.date is None:
            return None
        return _dateAsString(self.date)

    @property
    def transDateAsString(self):
        if self.transDate is None:
            return None
        return _dateAsString(self.transDate)

    @property
    def postDateAsString(self):
        if self.postDate is None:
            return None
        return _dateAsString(self.postDate)

    @property
    def jsonEncodable(self):
        return {
            'type': self.type,
            'transDate': self.transDateAsString,
            'postDate': self.postDateAsString,
            'description': self.description,
            'amount': self.amount,
            'tags': self.tags,
            }

    @staticmethod
    def createFromJson(jsonDecodable):
        t = Transaction()
        t.type = jsonDecodable['type']
        t.transDate = _parseTransactionDate(jsonDecodable['transDate'])
        t.postDate = _parseTransactionDate(jsonDecodable['postDate'])
        t.description = jsonDecodable['description']
        t.amount = jsonDecodable['amount']
        if 'tags' in jsonDecodable:
            t.tags = jsonDecodable['tags']
            if isinstance(t.tags, list):
                t.tags = {tagName: None for tagName in t.tags}
        return t

def _dateAsString(date):
    return '%04d-%02d-%02d' % (date.year, date.month, date.day)

def _parseTransactionDate(s):
    if s is None:
        return None
    year, month, day = s.split('-')
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
