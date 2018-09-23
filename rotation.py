def get_rotation(positions, off, override, max_m):
    series = __rotation(positions, off, max_m)
    schedule = __assign_workers(series, positions)
    return __apply_overrides(schedule, override)


def __rotation(positions, off, max_m):
    m = 0
    n = 0
    while m <= max_m:
        n = __offset(m, n, positions, off)
        yield n
        m += 1
        n += 1


def __offset(m, n, positions, off):
    r = n
    while m in off and (r % positions in off[m]):
        r += 1
    return r


def __apply_overrides(schedule: iter, overrides: dict):
    return [overrides[(m, n)] if (m, n) in overrides else n for (m, n) in enumerate(schedule)]


def __assign_workers(series: iter, count: int):
    return map(lambda n: n % count, series)
