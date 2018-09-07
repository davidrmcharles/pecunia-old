#!/usr/bin/env python
'''
For parsing account activity
'''

# Standard imports:
import datetime

def parseFile(path):
    '''
    Parse the account-activity file at `path`.
    '''

    pass  # TODO

def parseString(text):
    '''
    Parse the `text` of an account-activity file.
    '''

    pass  # TODO

def parseKeyLine(line):
    '''
    Parse the `line` that explains the content of the various columns.
    '''

    transactionKey = _TransactionKey()
    tokens = line.split(',')
    for index, token in enumerate(tokens):
        if token.lower() in ('posting date', 'post date'):
            transactionKey.postDate = index
        elif token.lower() == 'description':
            transactionKey.description = index
        elif token.lower() == 'amount':
            transactionKey.amount = index
        elif token.lower() == 'type':
            transactionKey.type = index
        elif token.lower() == 'trans date':
            transactionKey.transDate = index
    return transactionKey

class _TransactionKey(object):

    def __init__(self):
        self.type = None
        self.transDate = None
        self.postDate = None
        self.description = None
        self.amount = None

def parseLine(key, line):
    '''
    Parse a single `line` of account activity.
    '''

    transaction = Transaction()

    tokens = line.split(',')
    transaction.type = _parseTransactionType(tokens[key.type])
    if key.transDate is not None:
        transaction.transDate = _parseTransactionDate(tokens[key.transDate])
    transaction.postDate = _parseTransactionDate(tokens[key.postDate])
    transaction.description = tokens[key.description]
    transaction.amount = float(tokens[key.amount])

    return transaction

def _parseTransactionType(s):
    if s.lower() in ('misc_debit', 'sale'):
        return 'debit'

def _parseTransactionDate(s):
    month, day, year = s.split('/')
    return datetime.date(int(year), int(month), int(day))

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

