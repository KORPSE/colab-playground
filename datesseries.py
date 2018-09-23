from datetime import date, timedelta


def dates(start: date):
    dt = start
    while True:
        if dt.weekday() < 5:
            yield dt
        dt = dt + timedelta(days=1)


def dates_between(start: date, end: date):
    dt = start
    while dt <= end:
        if dt.weekday() < 5:
            yield dt
        dt = dt + timedelta(days=1)
