'''
For working with dates

Functions:

* :func:`parse_date_sequence_file`
* :func:`parse_date_sequence`
* :func:`parse_date_range`
* :func:`parse_date`
* :func:`date_as_string`

Objects:

* :class:`DateSequence`
* :class:`DateRange`

Exceptions:

* :class:`DateError`
* :class:`DateParsingError`
* :class:`InvalidDateRange`
'''

# Standard imports:
import datetime
import sys


def parse_date_sequence_file(path):
    '''
    Convert the contents of the file at `path` to a :class:`DateSequence`.
    '''

    result = DateSequence([])
    with open(path, 'r') as date_sequence_file:
        return parse_date_sequence(
            date_sequence_file.read().strip().replace('\n', ','))
    return result


def parse_date_sequence(s):
    '''
    Convert the string representation of a date sequence to its object
    representation.
    '''

    try:
        dates = []
        for subtoken in s.split(','):
            if subtoken == '':
                continue
            elif '..' in subtoken:
                dates.append(parse_date_range(subtoken))
            else:
                dates.append(parse_date(subtoken))
        return DateSequence(dates)

    except Exception as e:
        if not isinstance(e, DateError):
            raise DateParsingError(
                '"%s" is not a date sequence.' % s), None, sys.exc_info()[2]
        raise


def parse_date_range(s):
    '''
    Convert the string representation of a single date ranage to its
    object representation.
    '''

    try:
        subtokens = s.split('..')

        if len(subtokens) == 1:
            raise DateParsingError('No dotdots!!')
        if len(subtokens) > 2:
            raise DateParsingError('More than one dotdot!')

        dates = []
        for subtoken in subtokens:
            if len(subtoken) == 0:
                dates.append(None)
            else:
                dates.append(parse_date(subtoken))

        if dates == [None, None]:
            raise DateParsingError('Dotdot only, no dates!')

        return DateRange(dates[0], dates[1])

    except Exception as e:
        if not isinstance(e, DateError):
            raise DateParsingError(
                '"%s" is not a date range.' % s), None, sys.exc_info()[2]
        raise


def parse_date(s):
    '''
    Convert the string representation of a single date to its
    object representation.
    '''

    try:
        year, month, day = s.split('-')
        return datetime.date(int(year), int(month), int(day))
    except Exception as e:
        if not isinstance(e, DateError):
            raise DateParsingError(
                '"%s" is not a date.' % s), None, sys.exc_info()[2]
        raise


def date_as_string(date):
    '''
    Convert a `date` object to its string representation.
    '''

    return '%04d-%02d-%02d' % (date.year, date.month, date.day)


class DateSequence(object):
    '''
    A sequence of dates and date ranges
    '''

    def __init__(self, dates):
        self.dates = dates

    def __repr__(self):
        return '[%s]' % (
            ', '.join([
                date.__repr__()
                for date in self.dates])
        )

    def __contains__(self, date):
        if not isinstance(date, datetime.date):
            raise TypeError(
                'Non-date "%s" was passed to DateSequence.__contains__().' % (
                    date))
        for date_ in self.dates:
            if isinstance(date_, DateRange):
                if date in date_:
                    return True
            else:
                if date == date_:
                    return True
        return False

    def __eq__(self, other):
        if not isinstance(other, DateSequence):
            return False
        if len(self.dates) != len(other.dates):
            return False
        for self_date, other_date in zip(self.dates, other.dates):
            if self_date != other_date:
                return False
        return True

    def __ne__(self, other):
        if not isinstance(other, DateSequence):
            return True
        if len(self.dates) != len(other.dates):
            return True
        for self_date, other_date in zip(self.dates, other.dates):
            if self_date != other_date:
                return True
        return False

    def __hash__(self):
        return hash(tuple(self.dates))

    def extend(self, other):
        self.dates.extend(other.dates)


class DateRange(object):
    '''
    A single date range
    '''

    def __init__(self, first, last):
        if (first, last) == (None, None):
            raise InvalidDateRange(
                '"(%s, %s)" is an invalid DateRange.' % (
                    first, last))
        if (first is not None) and (last is not None) and (first > last):
            raise InvalidDateRange(
                '"(%s, %s)" is an invalid DateRange.' % (
                    first, last))
        self.first = first
        self.last = last

    def __contains__(self, date):
        if not isinstance(date, datetime.date):
            raise TypeError(
                'Non-date "%s" was passed to DateRange.__contains__().' % (
                    date))
        if self.first is None:
            return date <= self.last
        elif self.last is None:
            return date >= self.first
        else:
            return (date >= self.first) and (date <= self.last)

    def __eq__(self, other):
        if not isinstance(other, DateRange):
            return False
        return (self.first == other.first) and (self.last == other.last)

    def __ne__(self, other):
        if not isinstance(other, DateRange):
            return True
        return (self.first != other.first) or (self.last != other.last)

    def __hash__(self):
        return hash((self.first, self.last))


class DateError(ValueError):
    '''
    Base of all date-related exceptions
    '''

    def __init__(self, s):
        ValueError.__init__(self, s)


class DateParsingError(DateError):
    '''
    A failure to parse a single date
    '''

    def __init__(self, s):
        DateError.__init__(self, s)


class InvalidDateRange(DateError):
    '''
    A failure to valiate a range of two successfully parsed dates
    '''

    def __init__(self, s):
        DateError.__init__(self, s)
