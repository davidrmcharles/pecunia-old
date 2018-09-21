#!/usr/bin/env python
'''
A command-line interface to ``pecunia``

* :func:`main`
'''

# Standard imports:
import argparse
import collections
import re
import sys

# Project imports:
import datetools
import classifying
import importing
import filtering
import formatting
import transactions

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
    return _OptionParser().parse_args(args)

class _OptionParser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Import and analyze bank-account activity')
        self.subparsers = self.parser.add_subparsers(
            title='Command',
            dest='command',
            help='command to perform')
        self._createOptionSubparser_import()
        self._createOptionSubparser_list()
        self._createOptionSubparser_tags()
        self._createOptionSubparser_classify()

    def parse_args(self, args=None):
        return self.parser.parse_args(args)

    def _createOptionSubparser_import(self):
        parser = self.subparsers.add_parser(
            'import',
            description='Import transactions from .csv files',
            help='import transactions')
        parser.add_argument(
            'inputFilePaths',
            nargs='+',
            help='input file path',
            metavar='FILE')

    def _createOptionSubparser_list(self):
        parser = self.subparsers.add_parser(
            'list',
            description='List transactions',
            help='list transactions')
        self._createOption_dates(parser)
        self._createOption_descRegex(parser)
        self._createOption_noTags(parser)

    def _createOptionSubparser_tags(self):
        parser = self.subparsers.add_parser(
            'tags',
            description='List interesting facts about tags',
            help='list tags')
        self._createOption_dates(parser)

    def _createOptionSubparser_classify(self):
        parser = self.subparsers.add_parser(
            'classify',
            description='Interactively classify transactions',
            help='classify transactions')
        self._createOption_dates(parser)
        self._createOption_descRegex(parser)
        self._createOption_noTags(parser)

    def _createOption_dates(self, parser):
        parser.add_argument(
            '--dates',
            type=datetools.parseDateSequence,
            help='consider only transactions in a date range',
            dest='dates')

    def _createOption_descRegex(self, parser):
        parser.add_argument(
            '--desc-regex',
            help='consider only transactions with matching description',
            metavar='REGEX',
            dest='descriptionRegex')

    def _createOption_noTags(self, parser):
        parser.add_argument(
            '--no-tags',
            action='store_true',
            help='consider only transactions without tags',
            dest='noTags')

def _importTransactions(options):
    sys.stdout.write('Importing transactions.\n')

    transactions_ = []
    for path in options.inputFilePaths:
        transactions_.extend(importing.parseFile(path))

    sys.stdout.write('Imported %d transactions.\n' % len(transactions_))

    _storeTransactions(transactions_)

    sys.stdout.write(
        'Stored %d transcations to file "%s".\n' % (
            len(transactions_), transactions.cacheFilePath()))

def _listTransactions(options):
    allTransactions = transactions.load()
    filteredTransactions = _filterTransactions(allTransactions, options)
    for transaction in filteredTransactions:
        sys.stdout.write(formatting.formatTransactionForOneLine(transaction))
        sys.stdout.write('\n')

def _listTags(options):
    allTransactions = transactions.load()
    filteredTransactions = _filterTransactions(allTransactions, options)
    if len(filteredTransactions) == 0:
        return

    transactionsByTag = _sortTransactionsByTag(filteredTransactions)

    def mapTags(tokenFunc):
        return [tokenFunc(tag) for tag in transactionsByTag.iterkeys()]

    def mapTransactionLists(tokenFunc):
        return [
            tokenFunc(transactionList)
            for transactionList in transactionsByTag.itervalues()
            ]

    def tagToken(s):
        return str(s)

    def countToken(transactions_):
        return str(len(transactions_))

    def expenseToken(transactions_):
        return '{0:,.2f}'.format(
            sum([t.amount for t in transactions_ if t.amount < 0]))

    def incomeToken(transactions_):
        return '{0:,.2f}'.format(
            sum([t.amount for t in transactions_ if t.amount > 0]))

    def volumeToken(transactions_):
        return '{0:,.2f}'.format(
            sum([abs(t.amount) for t in transactions_]))

    def netToken(transactions_):
        return '{0:,.2f}'.format(
            sum([t.amount for t in transactions_]))

    table = formatting.ConsoleTable()
    table.createColumn('TAG', mapTags(tagToken), alignment='left')
    table.createColumn('COUNT', mapTransactionLists(countToken))
    table.createColumn('EXPENSE', mapTransactionLists(expenseToken))
    table.createColumn('INCOME', mapTransactionLists(incomeToken))
    table.createColumn('VOLUME', mapTransactionLists(volumeToken))
    table.createColumn('NET', mapTransactionLists(netToken))
    table.write(sys.stdout)

def _sortTransactionsByTag(transactions_):
    # Discover the full set of tags.
    tags = set()
    for transaction in transactions_:
        if len(transaction.tags) == 0:
            tags.add(None)
        for tag in transaction.tags.keys():
            tags.add(tag)

    # Create an alphabetically sorted mapping of tag onto empty lists.
    transactionsByTag = collections.OrderedDict()
    for tag in sorted(tags):
        transactionsByTag[tag] = []

    # Populate the lists with transactions.
    for transaction in transactions_:
        if len(transaction.tags) == 0:
            transactionsByTag[None].append(transaction)
        for tag in transaction.tags.keys():
            transactionsByTag[tag].append(transaction)

    return transactionsByTag

def _classifyTransactions(options):
    sys.stdout.write('Classifying transactions.\n')

    allTransactions = transactions.load()

    sys.stdout.write('Loaded %d transactions.\n' % len(allTransactions))

    filteredTransactions = _filterTransactions(allTransactions, options)

    classifying.classifyInteractively(allTransactions, filteredTransactions)

    transactions.store(allTransactions)
    sys.stdout.write(
        'Stored %d transcations to file "%s".\n' % (
            len(allTransactions), transactions.cacheFilePath()))

def _filterTransactions(allTransactions, options):
    filteredTransactions = filtering.filterTransactions(
        allTransactions, options)

    sys.stdout.write(
        'After filtering, %d transactions remain.\n' % (
            len(filteredTransactions)))

    return filteredTransactions

if __name__ == '__main__':
    main()
