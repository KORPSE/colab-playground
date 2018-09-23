from itertools import islice

from datetime import date, datetime

from datesseries import dates, dates_between
from rotation import get_rotation
from timeoff import get_hibob_time_off, merge_time_off

fmt = "%Y-%m-%d"


def generate_schedule(hb_access_token, start_date_str: str, count: int, workers: list, offs: dict, overrides=None):
    if overrides is None:
        overrides = {}
    start_date = __parse_date(start_date_str)
    schedule_dates = list(islice(dates(start_date), count))
    time_off_converted = __convert_time_off(workers, schedule_dates, offs)
    hibob_raw = get_hibob_time_off(hb_access_token, start_date, schedule_dates[-1], workers)
    hibob_time_off = __convert_time_off(workers, schedule_dates, hibob_raw)
    offs = merge_time_off(time_off_converted, hibob_time_off)
    rotation = get_rotation(len(workers), offs, overrides, count)
    return list(__apply_schedule(rotation, start_date, workers))


def __parse_date(dt: str):
    return datetime.strptime(dt, fmt).date()


def __apply_schedule(schedule: iter, start: date, names: list):
    for (n, dt) in zip(schedule, dates(start)):
        yield (str(dt), names[n])


def __convert_time_off(workers: list, schedule_dates: list, offs_raw: dict) -> dict:
    return {workers.index(w): [schedule_dates.index(dt)
                               for dt in __parse_dates(dts) if dt in schedule_dates]
            for (w, dts) in offs_raw.items()}


def __parse_dates(date_range):
    if ':' in date_range:
        parts = date_range.split(':')
        date_from = datetime.strptime(parts[0], fmt).date()
        date_to = datetime.strptime(parts[1], fmt).date()
        return dates_between(date_from, date_to)
    else:
        return [__parse_date(date_range)]
