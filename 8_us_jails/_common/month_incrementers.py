from datetime import datetime as dt
from dateutil.relativedelta import *

def file_month_incrementer(date, str_format='%B %d %Y'):
    # date = " 01 ".join(file.split("-")[1][:-4].split())
    date = dt.strptime(date, str_format)
    date = date + relativedelta(months=+1)
    date = date.strftime("%Y-%m-%d")
    return date
