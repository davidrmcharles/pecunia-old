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
    # subparsers.add_parser('classify', help='classify transactions')
    return parser

def _importTransactions(options):
    sys.stdout.write('Importing transactions.\n')

    transactions = []
    for path in options.inputFilePaths:
        transactions.extend(importing.parseFile(path))

    sys.stdout.write('Imported %d transactions.\n' % len(transactions))

    outputFilePath = os.path.join(
        _rootFolderPath, 'private', 'transactions.json')
    with open(outputFilePath, 'w') as outputFile:
        json.dump(
            [t.jsonEncodable for t in transactions],
            outputFile,
            indent=4)

    sys.stdout.write(
        'Recorded transcations to file "%s".\n' % outputFilePath)

def _classifyTransactions():
    print 'classifying...'  # TODO

if __name__ == '__main__':
    main()
