'''
Transaction filtering
'''

def filterTransactions(allTransactions, options):
    filteredTransactions = allTransactions

    if hasattr(options, 'noTags') and options.noTags:
        filteredTransactions = _filterTransactionsWithoutTags(
            filteredTransactions)

    if hasattr(options, 'descriptionRegex') and options.descriptionRegex is not None:
        filteredTransactions = _filterTransactionsWithNonMatchingDescriptions(
            filteredTransactions, options.descriptionRegex)

    if hasattr(options, 'dates') and options.dates is not None:
        filteredTransactions = _filterTransactionsWithNonMatchingDates(
            filteredTransactions, options.dates)

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

def _filterTransactionsWithNonMatchingDescriptions(filteredTransactions,
                                                   descriptionRegex):
    beforeSize = len(filteredTransactions)
    filteredTransactions = [
        t for t in filteredTransactions
        if re.search(descriptionRegex, t.description) is not None
        ]
    afterSize = len(filteredTransactions)
    sys.stdout.write(
        'Filtered %d transactions with non-matching description.\n' % (
            beforeSize - afterSize))
    return filteredTransactions

def _filterTransactionsWithNonMatchingDates(filteredTransactions,
                                            dateSequence):
    filteredTransactions = [
        t for t in filteredTransactions
        if t.date in dateSequence
        ]
    return filteredTransactions
