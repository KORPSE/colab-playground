import requests
from datetime import date, datetime
from typing import Dict, Set


url = "https://api.hibob.com/v1/timeoff/whosout"
fmt = "%Y-%m-%d"


def get_hibob_time_off(access_token: str, date_from: date, date_to: date, workers) -> dict:
    result = {}
    for (name, start, end) in __hibob_time_off_list(access_token, date_from, date_to):
        if name in workers:
            dates = str(max(start, date_from)) + ':' + str(min(date_to, end))
            if name in result:
                result[name] = result.get(name) + dates
            else:
                result[name] = dates
    return result


def merge_time_off(off_a: Dict[str, Set[date]], off_b: Dict[str, Set[date]]) -> Dict[str, Set[date]]:
    result = {}
    all_items = list(off_a.items()) + list(off_b.items())
    for (w, dates) in all_items:
        if w in result:
            result[w] += dates
        else:
            result[w] = dates
    return result


def __hibob_time_off_list(access_token: str, date_from: date, date_to: date) -> iter:
    querystring = {"from": str(date_from), "to": str(date_to)}

    response = requests.request("GET",
                                url,
                                params=querystring,
                                headers={"Authorization": access_token})

    for employee in response.json()['outs']:
        yield employee['employeeDisplayName'], \
              datetime.strptime(employee['startDate'], fmt).date(),\
              datetime.strptime(employee['endDate'], fmt).date()


