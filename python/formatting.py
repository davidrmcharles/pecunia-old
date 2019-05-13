'''
Transaction formatting for the console

* :func:`format_transaction_for_one_line`
* :func:`format_transaction_for_detail`
* :class:`ConsoleTable`
'''

# Standard imports:
import re


def format_transaction_for_one_line(transaction):
    return _TransactionOneLineFormatter(80).format(transaction)


class _TransactionOneLineFormatter(object):

    def __init__(self, width):
        self._width = width

    def format(self, transaction):
        column_budget = self._width

        date = self._format_date(transaction)
        column_budget -= (len(date) + 1)

        amount = self._format_amount(transaction)
        column_budget -= (len(amount) + 1)

        tags = self._format_tags(transaction)
        column_budget -= len(tags)

        space_for_description = column_budget - 1
        description = self._format_description(
            transaction, space_for_description)

        return '%s %s %s %s' % (
            date, amount, description, tags)

    def _format_date(self, transaction):
        if transaction.trans_date is not None:
            return transaction.trans_date_as_string
        elif transaction.post_date is not None:
            return transaction.post_date_as_string
        else:
            return '????-??-??'

    def _format_amount(self, transaction):
        return '%8.2f' % transaction.amount

    def _format_tags(self, transaction):
        return '[%s]' % '|'.join(transaction.tags.keys())

    def _format_description(self, transaction, width):
        description = self._collapse_spaces(transaction.description)
        if len(description) > width:
            description = self._truncate_with_ellipses(description, width)
        if len(description) < width:
            description = self._extend_with_spaces(description, width)
        return description

    def _collapse_spaces(self, s):
        return re.sub(r' {2,}', ' ', s)

    def _truncate_with_ellipses(self, s, width):
        return s[:width - 3] + '...'

    def _extend_with_spaces(self, s, width):
        return '%s%s' % (s, (' ' * (width - len(s))))


def format_transaction_for_detail(transaction):
    return '\n'.join([
        '    type:         %s' % transaction.type,
        '    trans_date:   %s' % transaction.trans_date_as_string,
        '    post_date:    %s' % transaction.post_date_as_string,
        '    description:  %s' % transaction.description,
        '    amount:       %.2f' % transaction.amount,
        '    tags:         %s' % ' '.join(transaction.tags),
    ])


class ConsoleTable(object):

    def __init__(self):
        self.columns = []

    def create_column(self, title, tokens, alignment='right'):
        self.columns.append(_ConsoleTableColumn(title, tokens, alignment))

    def write(self, output_file):
        self._write_titles(output_file)
        self._write_rows(output_file)

    def _write_titles(self, output_file):
        output_file.write(
            '%-*s' % (
                self.columns[0].width, self.columns[0].title))
        for column in self.columns[1:]:
            output_file.write('  %*s' % (column.width, column.title))
        output_file.write('\n')

    def _visit_rows(self):
        return zip(*[column.formatted_tokens for column in self.columns])

    def _write_rows(self, output_file):
        for formatted_tokens in self._visit_rows():
            output_file.write('%s' % formatted_tokens[0])
            for formatted_token in formatted_tokens[1:]:
                output_file.write('  %s' % formatted_token)
            output_file.write('\n')


class _ConsoleTableColumn(object):

    def __init__(self, title, tokens, alignment='right'):
        self.title = title
        self.tokens = tokens
        self.alignment = alignment

    @property
    def width(self):
        return max([
            len(token)
            for token in [self.title] + self.tokens
        ])

    @property
    def alignment_pattern(self):
        if self.alignment == 'left':
            return '%-*s'
        elif self.alignment == 'right':
            return '%*s'

    @property
    def formatted_tokens(self):
        return [
            self.alignment_pattern % (self.width, token)
            for token in self.tokens
        ]
