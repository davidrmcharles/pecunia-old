'''
Transaction filtering
'''

# Standard imports:
import re
import sys

def filterTransactions(allTransactions, options):
    filteredTransactions = allTransactions

    if hasattr(options, 'dates') and options.dates is not None:
        filteredTransactions = _filterTransactionsWithNonMatchingDates(
            filteredTransactions, options.dates)

    if hasattr(options, 'include_regex') and options.include_regex is not None:
        filteredTransactions = _filterTransactionsWithNonMatchingDescriptions(
            filteredTransactions, options.include_regex)

    if hasattr(options, 'exclude_regex') and options.exclude_regex is not None:
        filteredTransactions = _filterTransactionsWithMatchingDescriptions(
            filteredTransactions, options.exclude_regex)

    if hasattr(options, 'no_tags') and options.no_tags:
        filteredTransactions = _filterTransactionsWithoutTags(
            filteredTransactions)

    return filteredTransactions

def _filterTransactionsWithNonMatchingDates(filteredTransactions,
                                            dateSequence):
    filteredTransactions = [
        t for t in filteredTransactions
        if t.date in dateSequence
        ]
    return filteredTransactions

def _filterTransactionsWithNonMatchingDescriptions(filteredTransactions,
                                                   regex):
    beforeSize = len(filteredTransactions)
    filteredTransactions = [
        t for t in filteredTransactions
        if re.search(regex, t.description, re.IGNORECASE) is not None
        ]
    afterSize = len(filteredTransactions)
    sys.stdout.write(
        'Filtered %d transactions with non-matching description.\n' % (
            beforeSize - afterSize))
    return filteredTransactions

def _filterTransactionsWithMatchingDescriptions(filteredTransactions,
                                                regex):
    beforeSize = len(filteredTransactions)
    filteredTransactions = [
        t for t in filteredTransactions
        if re.search(regex, t.description, re.IGNORECASE) is None
        ]
    afterSize = len(filteredTransactions)
    sys.stdout.write(
        'Filtered %d transactions with non-matching description.\n' % (
            beforeSize - afterSize))
    return filteredTransactions

def _filterTransactionsWithoutTags(filteredTransactions):
    beforeSize = len(filteredTransactions)
    filteredTransactions = [
        t for t in filteredTransactions
        if len(t.tags) == 0
        ]
    afterSize = len(filteredTransactions)
    sys.stdout.write(
        'Filtered %d transactions without tags.\n' % (
            beforeSize - afterSize))
    return filteredTransactions

