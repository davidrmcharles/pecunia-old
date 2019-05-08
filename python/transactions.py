#!/usr/bin/env python
'''
About transactions

:func:`load`
:func:`store`
:func:`database_path`
:class:`Transaction`
'''

# Standard imports:
import datetime
import inspect
import json
import os

# Project imports:
import datetools

_this_file_path = inspect.getfile(inspect.currentframe())
_this_folder_path = os.path.abspath(os.path.dirname(_this_file_path))
_root_folder_path = os.path.dirname(_this_folder_path)
_database_path = os.path.join(
    _root_folder_path, 'private', 'transactions.json')


def load():
    with open(_database_path, 'r') as database_file:
        json_decodables = json.load(database_file)
        xactions = [
            Transaction.decode(json_decodable)
            for json_decodable in json_decodables
            ]
    xactions.sort(key=lambda x: x.date, reverse=True)
    return xactions


def store(xactions):
    with open(_database_path, 'w') as database_file:
        json.dump(
            [x.encode() for x in xactions],
            database_file,
            indent=4)


def database_path():
    return _database_path


class Transaction(object):
    '''
    A single account-activity event
    '''

    def __init__(self):
        self.type = None
        self.trans_date = None
        self.post_date = None
        self.description = None
        self.amount = None
        self.tags = {}

    @property
    def date(self):
        if self.trans_date is not None:
            return self.trans_date
        elif self.post_date is not None:
            return self.post_date
        return None

    @property
    def date_as_string(self):
        if self.date is None:
            return None
        return datetools.date_as_string(self.date)

    @property
    def trans_date_as_string(self):
        if self.trans_date is None:
            return None
        return datetools.date_as_string(self.trans_date)

    @property
    def post_date_as_string(self):
        if self.post_date is None:
            return None
        return datetools.date_as_string(self.post_date)

    def encode(self):
        return {
            'type': self.type,
            'trans_date': self.trans_date_as_string,
            'post_date': self.post_date_as_string,
            'description': self.description,
            'amount': self.amount,
            'tags': self.tags,
        }

    @staticmethod
    def decode(json_decodable):
        x = Transaction()
        x.type = json_decodable['type']
        x.trans_date = _parse_transaction_date(json_decodable['trans_date'])
        x.post_date = _parse_transaction_date(json_decodable['post_date'])
        x.description = json_decodable['description']
        x.amount = json_decodable['amount']
        if 'tags' in json_decodable:
            x.tags = json_decodable['tags']
            if isinstance(x.tags, list):
                x.tags = {tag: None for tag in x.tags}
        return x


def _parse_transaction_date(s):
    if s is None:
        return None
    return datetools.parse_date(s)
