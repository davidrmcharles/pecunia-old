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
        self._create_option_include_regexs(parser)
        self._create_option_exclude_regexs(parser)
        self._create_option_no_tags(parser)
        self._create_option_print_total(parser)

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
        self._create_option_include_regexs(parser)
        self._create_option_exclude_regexs(parser)
        self._create_option_no_tags(parser)

    def _create_option_dates(self, parser):
        parser.add_argument(
            '--dates',
            type=datetools.parse_date_sequence,
            help='consider only transactions in a date range',
            dest='dates')

    def _create_option_include_regexs(self, parser):
        parser.add_argument(
            '--include',
            action='append',
            default=[],
            help='consider only transactions with matching description',
            metavar='REGEX',
            dest='include_regexs')

    def _create_option_exclude_regexs(self, parser):
        parser.add_argument(
            '--exclude',
            action='append',
            default=[],
            help='consider only transactions with a non-matching description',
            metavar='REGEX',
            dest='exclude_regexs')

    def _create_option_no_tags(self, parser):
        parser.add_argument(
            '--no-tags',
            action='store_true',
            help='consider only transactions without tags',
            dest='no_tags')

    def _create_option_print_total(self, parser):
        parser.add_argument(
            '--total',
            action='store_true',
            help='print total amount of listed transactions',
            dest='print_total')


class _ImportTransactionsCommand(object):
    '''
    The ``import`` command
    '''

    def __init__(self, options):
        self.options = options

    def do(self):
        sys.stdout.write('Importing transactions.\n')

        xactions = []
        for path in self.options.inputFilePaths:
            xactions.extend(importing.parse_file(path))

        sys.stdout.write('Imported %d transactions.\n' % len(xactions))

        transactions.store(xactions)

        sys.stdout.write(
            'Stored %d transcations to file "%s".\n' % (
                len(xactions), transactions.cacheFilePath()))


class _ListTransactionsCommand(object):
    '''
    The ``list`` command
    '''

    def __init__(self, options):
        self.options = options

    def do(self):
        all_xactions = transactions.load()
        filtered_xactions = _filter_transactions(
            all_xactions, self.options)
        for xaction in filtered_xactions:
            sys.stdout.write(formatting.formatTransactionForOneLine(xaction))
            sys.stdout.write('\n')

        if self.options.print_total:
            sys.stdout.write('%s\n' % ('-' * 80))
            sys.stdout.write(
                '           %8.2f\n' % sum([
                    x.amount for x in filtered_xactions
                ])
            )


class _ListTagsCommand(object):
    '''
    The ``tags`` command
    '''

    def __init__(self, options):
        self.options = options

    def do(self):
        all_xactions = transactions.load()
        filtered_xactions = _filter_transactions(
            all_xactions, self.options)
        if len(filtered_xactions) == 0:
            return

        xactions_by_tag = _sort_transactions_by_tag(filtered_xactions)

        def map_tags(token_func):
            return [token_func(tag) for tag in xactions_by_tag.iterkeys()]

        def map_transaction_lists(token_func):
            return [
                token_func(xaction_list)
                for xaction_list in xactions_by_tag.itervalues()
                ]

        def tag_token(s):
            return str(s)

        def countToken(xactions):
            return str(len(xactions))

        def expense_token(xactions):
            return '{0:,.2f}'.format(
                sum([x.amount for x in xactions if x.amount < 0]))

        def income_token(xactions):
            return '{0:,.2f}'.format(
                sum([x.amount for x in xactions if x.amount > 0]))

        def volume_token(xactions):
            return '{0:,.2f}'.format(
                sum([abs(x.amount) for x in xactions]))

        def net_token(xactions):
            return '{0:,.2f}'.format(
                sum([x.amount for x in xactions]))

        table = formatting.ConsoleTable()
        table.createColumn('TAG', map_tags(tag_token), alignment='left')
        table.createColumn('COUNT', map_transaction_lists(countToken))
        table.createColumn('EXPENSE', map_transaction_lists(expense_token))
        table.createColumn('INCOME', map_transaction_lists(income_token))
        table.createColumn('VOLUME', map_transaction_lists(volume_token))
        table.createColumn('NET', map_transaction_lists(net_token))
        table.write(sys.stdout)


def _sort_transactions_by_tag(xactions):
    # Discover the full set of tags.
    tags = set()
    for xaction in xactions:
        if len(xaction.tags) == 0:
            tags.add(None)
        for tag in xaction.tags.keys():
            tags.add(tag)

    # Create an alphabetically sorted mapping of tag onto empty lists.
    xactions_by_tag = collections.OrderedDict()
    for tag in sorted(tags):
        xactions_by_tag[tag] = []

    # Populate the lists with transactions.
    for xaction in xactions:
        if len(xaction.tags) == 0:
            xactions_by_tag[None].append(xaction)
        for tag in xaction.tags.keys():
            xactions_by_tag[tag].append(xaction)

    return xactions_by_tag


class _ClassifyTransactionsCommand(object):
    '''
    The ``classify`` command
    '''

    def __init__(self, options):
        self.options = options

    def do(self):
        sys.stdout.write('Classifying transactions.\n')

        all_xactions = transactions.load()

        sys.stdout.write('Loaded %d transactions.\n' % len(all_xactions))

        filtered_xactions = _filter_transactions(all_xactions, self.options)

        classifying.classifyInteractively(all_xactions, filtered_xactions)

        transactions.store(all_xactions)
        sys.stdout.write(
            'Stored %d transcations to file "%s".\n' % (
                len(all_xactions), transactions.cacheFilePath()))


def _filter_transactions(all_xactions, options):
    filtered_xactions = filtering.filter_transactions(
        all_xactions, options)

    sys.stdout.write(
        'After filtering, %d transactions remain.\n' % (
            len(filtered_xactions)))

    return filtered_xactions


if __name__ == '__main__':
    main()
