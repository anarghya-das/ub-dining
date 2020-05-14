import calendar
import time

# date format: YYYY-MM-DD


def get_unix_time(date):
    date = date.strip()
    # Adding 5 hours for EST conversion from UTC
    return calendar.timegm(time.strptime(f'{date} 05', '%Y-%m-%d %H'))
