'''
Transaction filtering

* :func:`filter_transactions`
'''

# Standard imports:
import re
import sys

# Project imports:
import datetools


def filter_transactions(xactions, options):
    '''
    Filter a list of transactions by certain criteria.
    '''

    filtered_xactions = xactions

    date_sequence = datetools.DateSequence([])
    if hasattr(options, 'dates') and options.dates is not None:
        date_sequence.extend(options.dates)
    if hasattr(options, 'dates_files'):
        for dates_file in options.dates_files:
            date_sequence.extend(
                datetools.parse_date_sequence_file(dates_file))
    if not date_sequence.is_empty:
        filtered_xactions = _filter_transactions_with_non_matching_dates(
            filtered_xactions, date_sequence)

    if hasattr(options, 'include_regexs') and len(options.include_regexs) > 0:
        filtered_xactions = _filter_transactions_with_non_matching_descriptions(
            filtered_xactions, options.include_regexs)

    if hasattr(options, 'exclude_regexs') and len(options.exclude_regexs) > 0:
        filtered_xactions = _filter_transactions_with_matching_descriptions(
            filtered_xactions, options.exclude_regexs)

    if hasattr(options, 'no_tags') and options.no_tags:
        filtered_xactions = _filter_transactions_without_tags(
            filtered_xactions)

    return filtered_xactions


def _filter_transactions_with_non_matching_dates(xactions, date_sequence):
    filtered_xactions = [
        x for x in xactions
        if x.date in date_sequence
    ]
    return filtered_xactions


def _filter_transactions_with_non_matching_descriptions(xactions, regexs):
    filtered_xactions = [
        x for x in xactions
        if _any_regex_matches(regexs, x.description)
    ]
    sys.stdout.write(
        'Filtered %d transaction(s) for not matching include regex.\n' % (
            len(xactions) - len(filtered_xactions)))
    return filtered_xactions


def _filter_transactions_with_matching_descriptions(xactions, regexs):
    filtered_xactions = [
        x for x in xactions
        if not _any_regex_matches(regexs, x.description)
    ]
    sys.stdout.write(
        'Filtered %d transaction(s) for matching exclude regex.\n' % (
            len(xactions) - len(filtered_xactions)))
    return filtered_xactions


def _any_regex_matches(regexs, s):
    for regex in regexs:
        if re.search(regex, s, re.IGNORECASE) is not None:
            return True
    return False


def _filter_transactions_without_tags(xactions):
    filtered_xactions = [
        x for x in xactions
        if len(x.tags) == 0
    ]
    sys.stdout.write(
        'Filtered %d transaction(s) for not having tags.\n' % (
            len(xactions) - len(filtered_xactions)))
    return filtered_xactions
