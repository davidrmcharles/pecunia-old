#!/usr/bin/env python
'''
For importing account activity
'''

# Standard imports:
import datetime
import sys
import traceback

# Project imports:
import transactions


def parse_file(path):
    '''
    Parse the account-activity file at `path`.
    '''

    transactions = []

    with open(path, 'r') as activity_file:
        line = activity_file.readline()
        transaction_key = _parse_key_line(line)
        for line in activity_file.readlines():
            try:
                transaction = _parse_line(transaction_key, line)
            except Exception:
                traceback.print_exc()
                continue

            if transaction.type not in ('payment', 'acct_xfer'):
                transactions.append(transaction)

    return transactions


def _parse_key_line(line):
    '''
    Parse the `line` that explains the content of the various columns.
    '''

    transaction_key = _TransactionKey()
    tokens = line.strip().split(',')
    for index, token in enumerate(tokens):
        if token.lower() in ('posting date', 'post date'):
            transaction_key.post_date = index
        elif token.lower() == 'description':
            transaction_key.description = index
        elif token.lower() == 'amount':
            transaction_key.amount = index
        elif token.lower() == 'type':
            transaction_key.type = index
        elif token.lower() == 'trans date':
            transaction_key.trans_date = index
    return transaction_key


class _TransactionKey(object):

    def __init__(self):
        self.type = None
        self.trans_date = None
        self.post_date = None
        self.description = None
        self.amount = None


def _parse_line(key, line):
    '''
    Parse a single `line` of account activity.
    '''

    transaction = transactions.Transaction()

    tokens = _split_transaction_line(line)
    if key.type is not None:
        transaction.type = _parse_transaction_type(tokens[key.type])
    if key.trans_date is not None:
        transaction.trans_date = _parse_transaction_date(tokens[key.trans_date])
    if key.post_date is not None:
        transaction.post_date = _parse_transaction_date(tokens[key.post_date])
    if key.description is not None:
        transaction.description = tokens[key.description]
    if key.amount is not None:
        transaction.amount = float(tokens[key.amount])

    return transaction


def _split_transaction_line(line):
    maybe_tokens = line.strip().split(',')

    tokens = []
    for maybeToken in maybe_tokens:
        if maybeToken.startswith(' ') and (len(maybeToken) > 1):
            tokens[-1] = tokens[-1] + ',' + maybeToken
        else:
            tokens.append(maybeToken)
    return tokens


def _parse_transaction_type(s):
    return s.lower()


def _parse_transaction_date(s):
    try:
        month, day, year = s.split('/')
    except ValueError:
        year, month, day = s.split('-')
    return datetime.date(int(year), int(month), int(day))


def main():
    transactions = []
    for arg in sys.argv[1:]:
        transactions.extend(parse_file(arg))
    sys.stdout.write('Parsed %d transactions.\n' % len(transactions))


if __name__ == '__main__':
    main()
