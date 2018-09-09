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
        description='Import and classify transactions',
        usage='''\
pecunia <command>

The commands are:
    import
    classify
''')
    parser.add_argument(
        'command',
        choices=['import', 'classify'],
        help='The command to perform')
    return parser

def _importTransactions():
    print 'importing...'  # TODO

def _classifyTransactions():
    print 'classifying...'  # TODO

if __name__ == '__main__':
    main()
