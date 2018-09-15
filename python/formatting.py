'''
Transaction formatting for the console

* :func:`formatTransactionForOneLine`
* :func:`formatTransactionForDetail`
'''

# Standard imports:
import re

def formatTransactionForOneLine(transaction):
    return _TransactionOneLineFormatter(80).format(transaction)

class _TransactionOneLineFormatter(object):

    def __init__(self, width):
        self._width = width

    def format(self, transaction):
        columnBudget = self._width

        date = self._formatDate(transaction)
        columnBudget -= (len(date) + 1)

        amount = self._formatAmount(transaction)
        columnBudget -= (len(amount) + 1)

        tags = self._formatTags(transaction)
        columnBudget -= len(tags)

        spaceForDescription = columnBudget - 1
        description = self._formatDescription(
            transaction, spaceForDescription)

        return '%s %s %s %s' % (
            date, amount, description, tags)

    def _formatDate(self, transaction):
        if transaction.transDate is not None:
            return transaction.transDateAsString
        elif transaction.postDate is not None:
            return transaction.postDateAsString
        else:
            return '????-??-??'

    def _formatAmount(self, transaction):
        return '%7.2f' % transaction.amount

    def _formatTags(self, transaction):
        return '[%s]' % '|'.join(transaction.tags.keys())

    def _formatDescription(self, transaction, width):
        description = self._collapseSpaces(transaction.description)
        if len(description) > width:
            description = self._truncateWithEllipses(description, width)
        if len(description) < width:
            description = self._extendWithSpaces(description, width)
        return description

    def _collapseSpaces(self, s):
        return re.sub(r' {2,}', ' ', s)

    def _truncateWithEllipses(self, s, width):
        return s[:width - 3] + '...'

    def _extendWithSpaces(self, s, width):
        return '%s%s' % (s, (' ' * (width - len(s))))

def formatTransactionForDetail(transaction):
    return '\n'.join([
            '    type:         %s' % transaction.type,
            '    transDate:    %s' % transaction.transDateAsString,
            '    postDate:     %s' % transaction.postDateAsString,
            '    description:  %s' % transaction.description,
            '    amount:       %.2f' % transaction.amount,
            '    tags:         %s' % ' '.join(transaction.tags),
            ])