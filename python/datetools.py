'''
For working with dates

* :func:`dateAsString`
* :func:`parseSequenceOfDates`
* :func:`parseDateRange`
* :func:`parseDate`
'''

# Standard imports:
import datetime
import sys

class DateParsingError(ValueError):

    def __init__(self, s):
        ValueError.__init__(self, s)

def dateAsString(date):
    return '%04d-%02d-%02d' % (date.year, date.month, date.day)

def parseDateSequence(s):
    try:
        dates = []
        for subtoken in s.split(','):
            if '..' in subtoken:
                dates.append(parseDateRange(subtoken))
            else:
                dates.append(parseDate(subtoken))
        return dates

    except Exception:
        raise DateParsingError('"%s" is not a date sequence.' % s), None, sys.exc_info()[2]

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

        return dates[0], dates[1]

    except Exception as e:
        raise DateParsingError(
            '"%s" is not a date range.' % s), None, sys.exc_info()[2]

def parseDate(s):
    try:
        year, month, day = s.split('-')
        return datetime.date(int(year), int(month), int(day))
    except Exception:
        raise DateParsingError('"%s" is not a date.' % s), None, sys.exc_info()[2]
