#!/usr/bin/env python
'''
A command-line interface to ``pecunia``
'''

# Standard imports:
import argparse
import json
import sys

# Project imports:
import importing

def main():
    '''
    The command-line interface
    '''

    options = _parseOptions()
    if options.command == 'import':
        sys.stdout.write('Importing transactions.\n')
        _importTransactions()
    elif options.command == 'classify':
        sys.stdout.write('Classifying transactions.\n')
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

def _importTransactions():
    print 'importing...'  # TODO

def _classifyTransactions():
    print 'classifying...'  # TODO

if __name__ == '__main__':
    main()
