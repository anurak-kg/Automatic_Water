import datetime

__author__ = 'Anurak'


def build_dict(seq, key):
    return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))


def time_in_range(start, end):
    current_time = datetime.datetime.today().time()
    if start <= end:
        return start <= current_time <= end
    else:
        return start <= current_time or current_time <= end
