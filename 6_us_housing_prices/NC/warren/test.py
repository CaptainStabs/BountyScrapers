import datetime
# timestamp = 632102400000
# time_stamp = datetime.datetime.fromtimestamp(timestamp/1000)

temp_timestamp = -6847804800000

time_stamp = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=temp_timestamp/1000)

print(time_stamp)
