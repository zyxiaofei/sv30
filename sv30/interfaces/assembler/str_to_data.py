import datetime


def string_to_date(date_string: str):
    date_format = "%Y-%m-%d"
    date = datetime.datetime.date(datetime.datetime.strptime(date_string, date_format))
    return date
