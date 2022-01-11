import datetime

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2021, 12, 31)
delta = datetime.timedelta(days=5)

while start_date <= end_date:
    print(start_date)
    start_date += delta
