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

    if hasattr(options, 'include_regexs') and len(options.include_regexs) > 0:
        filteredTransactions = _filterTransactionsWithNonMatchingDescriptions(
            filteredTransactions, options.include_regexs)

    if hasattr(options, 'exclude_regexs') and len(options.exclude_regexs) > 0:
        filteredTransactions = _filterTransactionsWithMatchingDescriptions(
            filteredTransactions, options.exclude_regexs)

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
                                                   regexs):
    beforeSize = len(filteredTransactions)
    filteredTransactions = [
        t for t in filteredTransactions
        if _any_regex_matches(regex, t.description)
    ]
    afterSize = len(filteredTransactions)
    sys.stdout.write(
        'Filtered %d transactions with non-matching description.\n' % (
            beforeSize - afterSize))
    return filteredTransactions

def _filterTransactionsWithMatchingDescriptions(filteredTransactions,
                                                regexs):
    beforeSize = len(filteredTransactions)
    filteredTransactions = [
        t for t in filteredTransactions
        if not _any_regex_matches(regexs, t.description)
    ]
    afterSize = len(filteredTransactions)
    sys.stdout.write(
        'Filtered %d transactions with non-matching description.\n' % (
            beforeSize - afterSize))
    return filteredTransactions

def _any_regex_matches(regexs, s):
    for regex in regexs:
        if re.search(regex, s, re.IGNORECASE) is not None:
            return True
    return False

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

