#!/usr/bin/env python
'''
A command-line interface to ``pecunia``
'''

# Standard imports:
import argparse
import inspect
import json
import os
import re
import sys

# Project imports:
import datetools
import importing
import filtering
import formatting
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
    elif options.command == 'list':
        _listTransactions(options)
    elif options.command == 'tags':
        _listTags(options)
    elif options.command == 'classify':
        _classifyTransactions(options)

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
    _createOptionSubparser_import(subparsers)
    _createOptionSubparser_list(subparsers)
    _createOptionSubparser_tags(subparsers)
    _createOptionSubparser_classify(subparsers)
    return parser

def _createOptionSubparser_import(subparsers):
    parser = subparsers.add_parser(
        'import',
        help='import transactions')
    parser.add_argument(
        'inputFilePaths',
        nargs='+',
        help='input file path',
        metavar='FILE')

def _createOptionSubparser_list(subparsers):
    parser = subparsers.add_parser(
        'list',
        help='list transactions')
    _createOption_dates(parser)
    _createOption_descRegex(parser)
    _createOption_noTags(parser)

def _createOptionSubparser_tags(subparsers):
    parser = subparsers.add_parser(
        'tags',
        help='list tags')
    _createOption_dates(parser)

def _createOptionSubparser_classify(subparsers):
    parser = subparsers.add_parser(
        'classify',
        help='classify transactions')
    _createOption_dates(parser)
    _createOption_descRegex(parser)
    _createOption_noTags(parser)

def _createOption_dates(parser):
    parser.add_argument(
        '--dates',
        type=datetools.parseDateSequence,
        help='consider only transactions in a date range',
        dest='dates')

def _createOption_descRegex(parser):
    parser.add_argument(
        '--desc-regex',
        help='consider only transactions with matching description',
        metavar='REGEX',
        dest='descriptionRegex')

def _createOption_noTags(parser):
    parser.add_argument(
        '--no-tags',
        action='store_true',
        help='consider only transactions without tags',
        dest='noTags')

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

def _listTransactions(options):
    allTransactions = _loadTransactions()
    filteredTransactions = _filterTransactions(allTransactions, options)
    for transaction in filteredTransactions:
        sys.stdout.write(formatting.formatTransactionForOneLine(transaction))
        sys.stdout.write('\n')

def _listTags(options):
    allTransactions = _loadTransactions()
    filteredTransactions = _filterTransactions(allTransactions, options)
    if len(filteredTransactions) == 0:
        return

    transactionsByTag = {}
    for transaction in filteredTransactions:
        if len(transaction.tags) == 0:
            if None not in transactionsByTag:
                transactionsByTag[None] = []
            transactionsByTag[None].append(transaction)

        for tag in transaction.tags.keys():
            if tag not in transactionsByTag:
                transactionsByTag[tag] = []
            transactionsByTag[tag].append(transaction)

    tagColumnWidth = max([
            len(str(tag))
            for tag in transactionsByTag.iterkeys()
            ])

    for tag, transactionsWithTag in sorted(transactionsByTag.iteritems()):
        sys.stdout.write(
            '%-*s  %d\n' % (
                tagColumnWidth, tag, len(transactionsWithTag)))

def _classifyTransactions(options):
    sys.stdout.write('Classifying transactions.\n')

    allTransactions = _loadTransactions()

    sys.stdout.write('Loaded %d transactions.\n' % len(allTransactions))

    filteredTransactions = _filterTransactions(allTransactions, options)

    for index, transaction in enumerate(filteredTransactions):
        sys.stdout.write('''\
Classifying transaction %d of %d:

    ----------------------------------------------------------------------
''' % (index + 1, len(filteredTransactions)))
        sys.stdout.write('%s\n' % formatting.formatTransactionForDetail(transaction))
        sys.stdout.write('''\
    ----------------------------------------------------------------------

Each whitespace-delimited token is either a COMMAND or TAG to add to
this transaction.  Each token is processed in the order it appears.

To 'split' a transaction, append a colon and a dollar amount that
represents the amount associated with the tag.  For example:

    grocery cash:20.00

In the above example, $20.00 of the total amount is tagged as cash,
and the remaining balance of the transaction is tagged as grocery.

Here are the commands:

    !quit:  Quit without saving
    !save:  Save classification work to disk

You may also simply press ENTER to skip to the next transaction.

''')

        _handleUserInput(
            raw_input('>>> '),
            allTransactions,
            transaction)

    _storeTransactions(allTransactions)
    sys.stdout.write(
        'Stored %d transcations to file "%s".\n' % (
            len(allTransactions), _cacheFilePath))

def _loadTransactions():
    with open(_cacheFilePath, 'r') as cacheFile:
        jsonDecodables = json.load(cacheFile)
        transactions_ = [
            transactions.Transaction.createFromJson(jsonDecodable)
            for jsonDecodable in jsonDecodables
            ]
    transactions_.sort(key=lambda t: t.date, reverse=True)
    return transactions_

def _filterTransactions(allTransactions, options):
    filteredTransactions = filtering.filterTransactions(
        allTransactions, options)

    sys.stdout.write(
        'After filtering, %d transactions remain.\n' % (
            len(filteredTransactions)))

    return filteredTransactions

def _handleUserInput(rawInput, allTransactions, transaction):
    tokens = rawInput.strip().split()
    for token in tokens:
        if token.lower() in ('!quit', '!exit'):
            raise SystemExit(0)
        elif token.lower() in ('!store', '!save'):
            _storeTransactions(allTransactions)
            sys.stdout.write(
                'Stored %d transcations to file "%s".\n' % (
                    len(allTransactions), _cacheFilePath))
        else:
            transaction.tags.update(_parseTag(token))

def _parseTag(token):
    if ':' in token:
        tagName, tagAmount = token.split(':')
        return {tagName: float(tagAmount)}
    else:
        return {token: None}

if __name__ == '__main__':
    main()
