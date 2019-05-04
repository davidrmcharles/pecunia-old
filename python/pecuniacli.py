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

    options = _parse_options()
    if options.command == 'import':
        _ImportTransactionsCommand(options).do()
    elif options.command == 'list':
        _ListTransactionsCommand(options).do()
    elif options.command == 'tags':
        _ListTagsCommand(options).do()
    elif options.command == 'classify':
        _ClassifyTransactionsCommand(options).do()


def _parse_options(args=None):
    return _OptionParser().parse_args(args)


class _OptionParser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Import and analyze bank-account activity')
        self.subparsers = self.parser.add_subparsers(
            title='Command',
            dest='command',
            help='command to perform')
        self._create_options_subparser_import()
        self._create_options_subparser_list()
        self._create_options_subparser_tags()
        self._create_options_subparser_classify()

    def parse_args(self, args=None):
        return self.parser.parse_args(args)

    def _create_options_subparser_import(self):
        parser = self.subparsers.add_parser(
            'import',
            description='Import transactions from .csv files',
            help='import transactions')
        parser.add_argument(
            'inputFilePaths',
            nargs='+',
            help='input file path',
            metavar='FILE')

    def _create_options_subparser_list(self):
        parser = self.subparsers.add_parser(
            'list',
            description='List transactions',
            help='list transactions')
        self._create_option_dates(parser)
        self._create_option_descRegex(parser)
        self._create_option_noTags(parser)
        self._create_option_printTotal(parser)

    def _create_options_subparser_tags(self):
        parser = self.subparsers.add_parser(
            'tags',
            description='List interesting facts about tags',
            help='list tags')
        self._create_option_dates(parser)

    def _create_options_subparser_classify(self):
        parser = self.subparsers.add_parser(
            'classify',
            description='Interactively classify transactions',
            help='classify transactions')
        self._create_option_dates(parser)
        self._create_option_descRegex(parser)
        self._create_option_noTags(parser)

    def _create_option_dates(self, parser):
        parser.add_argument(
            '--dates',
            type=datetools.parseDateSequence,
            help='consider only transactions in a date range',
            dest='dates')

    def _create_option_descRegex(self, parser):
        parser.add_argument(
            '--desc-regex',
            help='consider only transactions with matching description',
            metavar='REGEX',
            dest='descriptionRegex')

    def _create_option_noTags(self, parser):
        parser.add_argument(
            '--no-tags',
            action='store_true',
            help='consider only transactions without tags',
            dest='noTags')

    def _create_option_printTotal(self, parser):
        parser.add_argument(
            '--total',
            action='store_true',
            help='print total amount of listed transactions',
            dest='printTotal')


class _ImportTransactionsCommand(object):
    '''
    The ``import`` command
    '''

    def __init__(self, options):
        self.options = options

    def do(self):
        sys.stdout.write('Importing transactions.\n')

        transactions_ = []
        for path in self.options.inputFilePaths:
            transactions_.extend(importing.parseFile(path))

        sys.stdout.write('Imported %d transactions.\n' % len(transactions_))

        transactions.store(transactions_)

        sys.stdout.write(
            'Stored %d transcations to file "%s".\n' % (
                len(transactions_), transactions.cacheFilePath()))


class _ListTransactionsCommand(object):
    '''
    The ``list`` command
    '''

    def __init__(self, options):
        self.options = options

    def do(self):
        allTransactions = transactions.load()
        filteredTransactions = _filter_transactions(
            allTransactions, self.options)
        for transaction in filteredTransactions:
            sys.stdout.write(formatting.formatTransactionForOneLine(transaction))
            sys.stdout.write('\n')

        if self.options.printTotal:
            sys.stdout.write('%s\n' % ('-' * 80))
            sys.stdout.write(
                '           %8.2f\n' % sum([
                    t.amount for t in filteredTransactions
                ])
            )


class _ListTagsCommand(object):
    '''
    The ``tags`` command
    '''

    def __init__(self, options):
        self.options = options

    def do(self):
        allTransactions = transactions.load()
        filteredTransactions = _filter_transactions(
            allTransactions, self.options)
        if len(filteredTransactions) == 0:
            return

        transactionsByTag = _sort_transactions_by_tag(filteredTransactions)

        def map_tags(tokenFunc):
            return [tokenFunc(tag) for tag in transactionsByTag.iterkeys()]

        def map_transaction_lists(tokenFunc):
            return [
                tokenFunc(transactionList)
                for transactionList in transactionsByTag.itervalues()
                ]

        def tag_token(s):
            return str(s)

        def countToken(transactions_):
            return str(len(transactions_))

        def expense_token(transactions_):
            return '{0:,.2f}'.format(
                sum([t.amount for t in transactions_ if t.amount < 0]))

        def income_token(transactions_):
            return '{0:,.2f}'.format(
                sum([t.amount for t in transactions_ if t.amount > 0]))

        def volume_token(transactions_):
            return '{0:,.2f}'.format(
                sum([abs(t.amount) for t in transactions_]))

        def net_token(transactions_):
            return '{0:,.2f}'.format(
                sum([t.amount for t in transactions_]))

        table = formatting.ConsoleTable()
        table.createColumn('TAG', map_tags(tag_token), alignment='left')
        table.createColumn('COUNT', map_transaction_lists(countToken))
        table.createColumn('EXPENSE', map_transaction_lists(expense_token))
        table.createColumn('INCOME', map_transaction_lists(income_token))
        table.createColumn('VOLUME', map_transaction_lists(volume_token))
        table.createColumn('NET', map_transaction_lists(net_token))
        table.write(sys.stdout)


def _sort_transactions_by_tag(transactions_):
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


class _ClassifyTransactionsCommand(object):
    '''
    The ``classify`` command
    '''

    def __init__(self, options):
        self.options = options

    def do(self):
        sys.stdout.write('Classifying transactions.\n')

        allTransactions = transactions.load()

        sys.stdout.write('Loaded %d transactions.\n' % len(allTransactions))

        filteredTransactions = _filter_transactions(allTransactions, self.options)

        classifying.classifyInteractively(allTransactions, filteredTransactions)

        transactions.store(allTransactions)
        sys.stdout.write(
            'Stored %d transcations to file "%s".\n' % (
                len(allTransactions), transactions.cacheFilePath()))


def _filter_transactions(allTransactions, options):
    filteredTransactions = filtering.filterTransactions(
        allTransactions, options)

    sys.stdout.write(
        'After filtering, %d transactions remain.\n' % (
            len(filteredTransactions)))

    return filteredTransactions


if __name__ == '__main__':
    main()
