#!/usr/bin/env python
'''
A command-line interface to ``pecunia``
'''

# Standard imports:
import argparse
import inspect
import json
import os
import sys

# Project imports:
import importing
import transactions

_thisFilePath = inspect.getfile(inspect.currentframe())
_thisFolderPath = os.path.abspath(os.path.dirname(_thisFilePath))
_rootFolderPath = os.path.dirname(_thisFolderPath)

def main():
    '''
    The command-line interface
    '''

    options = _parseOptions()
    if options.command == 'import':
        _importTransactions(options)
    elif options.command == 'classify':
        _classifyTransactions()

def _parseOptions(args=None):
    parser = _createOptionParser()
    options = parser.parse_args(args)
    return options

def _createOptionParser():
    parser = argparse.ArgumentParser(
        description='Import and classify transactions')
    subparsers = parser.add_subparsers(
        title='Command',
        dest='command',
        help='command to perform')
    importParser = subparsers.add_parser('import', help='import transactions')
    importParser.add_argument(
        'inputFilePaths',
        nargs='+',
        help='input file path',
        metavar='FILE')
    subparsers.add_parser('classify', help='classify transactions')
    return parser

_cacheFilePath = os.path.join(
    _rootFolderPath, 'private', 'transactions.json')

def _importTransactions(options):
    sys.stdout.write('Importing transactions.\n')

    transactions_ = []
    for path in options.inputFilePaths:
        transactions_.extend(importing.parseFile(path))

    sys.stdout.write('Imported %d transactions.\n' % len(transactions_))

    _storeTransactions(transactions_)

    sys.stdout.write(
        'Stored transcations to file "%s".\n' % _cacheFilePath)

def _storeTransactions(transactions_):
    outputFilePath = os.path.join(
        _rootFolderPath, 'private', 'transactions.json')
    with open(outputFilePath, 'w') as outputFile:
        json.dump(
            [t.jsonEncodable for t in transactions_],
            outputFile,
            indent=4)

def _classifyTransactions():
    sys.stdout.write('Classifying transactions.\n')

    transactions_ = _loadTransactions()

    sys.stdout.write('Loaded %d transactions.\n' % len(transactions_))

    for t in transactions_:
        sys.stdout.write('%s\n' % ('-' * 70))
        sys.stdout.write('%s\n' % _formatTransaction(t))
        sys.stdout.write('%s\n' % ('-' * 70))
        raw_input('Enter tags: ')

def _loadTransactions():
    with open(_cacheFilePath, 'r') as cacheFile:
        jsonDecodables = json.load(cacheFile)
        transactions_ = [
            transactions.Transaction.createFromJson(jsonDecodable)
            for jsonDecodable in jsonDecodables
            ]
    return transactions_

def _formatTransaction(transaction):
    return '\n'.join([
            'type:        %s' % transaction.type,
            'transDate:   %s' % transaction.transDate,
            'postDate:    %s' % transaction.postDate,
            'description: %s' % transaction.description,
            'amount:      %.2f' % transaction.amount
            ])

if __name__ == '__main__':
    main()
