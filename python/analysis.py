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
    min_post_date = min(xactions, key=lambda x: x.post_date).post_date
    max_post_date = max(xactions, key=lambda x: x.post_date).post_date
    day_count = (max_post_date - min_post_date).days
    return _cumulative_credits(xactions) / float(day_count)


def _debit_velocity(xactions):
    min_post_date = min(xactions, key=lambda x: x.post_date).post_date
    max_post_date = max(xactions, key=lambda x: x.post_date).post_date
    day_count = (max_post_date - min_post_date).days
    return _cumulative_debits(xactions) / float(day_count)
