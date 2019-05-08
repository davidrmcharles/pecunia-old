def _cumulative_credits(xactions):
    credits_ = 0.0
    for x in xactions:
        if x.amount > 0.0:
            credits_ += x.amount
    return credits_


def _cumulative_debits(xactions):
    debits = 0.0
    for x in xactions:
        if x.amount < 0.0:
            debits += x.amount
    return debits


def _credit_velocity(xactions):
    minPostDate = min(xactions, key=lambda x: x.post_date).post_date
    maxPostDate = max(xactions, key=lambda x: x.post_date).post_date
    numberOfDays = (maxPostDate - minPostDate).days
    return _cumulative_credits(xactions) / float(numberOfDays)


def _debit_velocity(xactions):
    minPostDate = min(xactions, key=lambda x: x.post_date).post_date
    maxPostDate = max(xactions, key=lambda x: x.post_date).post_date
    numberOfDays = (maxPostDate - minPostDate).days
    return _cumulative_debits(xactions) / float(numberOfDays)
