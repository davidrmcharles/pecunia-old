'''
For working with dates

Functions:
* :func:`parseSequenceOfDates`
* :func:`parseDateRange`
* :func:`parseDate`
* :func:`dateAsString`

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

def parseDateSequence(s):
    try:
        dates = []
        for subtoken in s.split(','):
            if '..' in subtoken:
                dates.append(parseDateRange(subtoken))
            else:
                dates.append(parseDate(subtoken))
        return DateSequence(dates)

    except Exception as e:
        if not isinstance(e, DateError):
            raise DateParsingError(
                '"%s" is not a date sequence.' % s), None, sys.exc_info()[2]
        raise

def parseDateRange(s):
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
                dates.append(parseDate(subtoken))

        if dates == [None, None]:
            raise DateParsingError('Dotdot only, no dates!')

        return DateRange(dates[0], dates[1])

    except Exception as e:
        if not isinstance(e, DateError):
            raise DateParsingError(
                '"%s" is not a date range.' % s), None, sys.exc_info()[2]
        raise

def parseDate(s):
    try:
        year, month, day = s.split('-')
        return datetime.date(int(year), int(month), int(day))
    except Exception as e:
        if not isinstance(e, DateError):
            raise DateParsingError(
                '"%s" is not a date.' % s), None, sys.exc_info()[2]
        raise

def dateAsString(date):
    return '%04d-%02d-%02d' % (date.year, date.month, date.day)

class DateSequence(object):

    def __init__(self, dates):
        self.dates = dates

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
        for selfDate, otherDate in zip(self.dates, other.dates):
            if selfDate != otherDate:
                return False
        return True

    def __ne__(self, other):
        if not isinstance(other, DateSequence):
            return True
        if len(self.dates) != len(other.dates):
            return True
        for selfDate, otherDate in zip(self.dates, other.dates):
            if selfDate != otherDate:
                return True
        return False

    def __hash__(self):
        return hash(tuple(self.dates))

class DateRange(object):

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

    def __init__(self, s):
        ValueError.__init__(self, s)

class DateParsingError(DateError):

    def __init__(self, s):
        DateError.__init__(self, s)

class InvalidDateRange(DateError):

    def __init__(self, s):
        DateError.__init__(self, s)
