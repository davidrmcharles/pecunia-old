#!/usr/bin/env python
'''
For parsing account activity
'''

# Standard imports:
import datetime
import sys
import traceback

def parseFile(path):
    '''
    Parse the account-activity file at `path`.
    '''

    transactions = []

    with open(path, 'r') as activityFile:
        line = activityFile.readline()
        transactionKey = parseKeyLine(line)
        for line in activityFile.readlines():
            try:
                transactions.append(parseLine(transactionKey, line))
            except Exception:
                traceback.print_exc()

    return transactions

def parseKeyLine(line):
    '''
    Parse the `line` that explains the content of the various columns.
    '''

    transactionKey = _TransactionKey()
    tokens = line.strip().split(',')
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

    tokens = _splitTransactionLine(line)
    transaction.type = _parseTransactionType(tokens[key.type])
    if key.transDate is not None:
        transaction.transDate = _parseTransactionDate(tokens[key.transDate])
    transaction.postDate = _parseTransactionDate(tokens[key.postDate])
    transaction.description = tokens[key.description]
    transaction.amount = float(tokens[key.amount])

    return transaction

def _splitTransactionLine(line):
    maybeTokens = line.strip().split(',')

    tokens = []
    for maybeToken in maybeTokens:
        if maybeToken.startswith(' ') and (len(maybeToken) > 1):
            tokens[-1] = tokens[-1] + ',' + maybeToken
        else:
            tokens.append(maybeToken)
    return tokens

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

if __name__ == '__main__':
    transactions = []
    for arg in sys.argv[1:]:
        transactions.extend(parseFile(arg))

    credits_ = 0.0
    for transaction in transactions:
        if transaction.amount > 0.0:
            credits_ += transaction.amount

    debits = 0.0
    for transaction in transactions:
        if transaction.amount < 0.0:
            debits += transaction.amount

    balance = credits_ + debits

    sys.stdout.write(
        'Parsed %d transactions with profile %.2f/%.2f/%.2f.\n' % (
            len(transactions), credits_, debits, balance))
