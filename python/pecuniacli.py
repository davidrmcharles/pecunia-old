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
        'Stored %d transcations to file "%s".\n' % (
            len(transactions_), _cacheFilePath))

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

    for transaction in transactions_:
        sys.stdout.write('''\
Classifying this transaction:

    ----------------------------------------------------------------------
''')
        sys.stdout.write('%s\n' % _formatTransaction(transaction))
        sys.stdout.write('''\
    ----------------------------------------------------------------------

Each whitespace-delimited token is either a COMMAND or TAG to add to
this transaction.  Each token is processed in the order it appears.
Here are the commands:

    !quit:  Quit without saving
    !save:  Save classification work to disk

You may also simply press ENTER to skip to the next transaction.

''')

        _handleUserInput(
            raw_input('>>> '),
            transactions_,
            transaction)

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
            '    type:         %s' % transaction.type,
            '    transDate:    %s' % transaction.transDate,
            '    postDate:     %s' % transaction.postDate,
            '    description:  %s' % transaction.description,
            '    amount:       %.2f' % transaction.amount,
            '    tags:         %s' % ' '.join(transaction.tags),
            ])

def _handleUserInput(rawInput, transactions_, transaction):
    tokens = rawInput.strip().split()
    for token in tokens:
        if token.lower() in ('!quit', '!exit'):
            raise SystemExit(0)
        elif token.lower() in ('!store', '!save'):
            _storeTransactions(transactions_)
            sys.stdout.write(
                'Stored %d transcations to file "%s".\n' % (
                    len(transactions_), _cacheFilePath))
        else:
            transaction.tags.append(token)


if __name__ == '__main__':
    main()
