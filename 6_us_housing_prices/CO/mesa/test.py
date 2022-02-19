import datetime
import os
timestamp = int(-49507200000/1000)

if os.name == "nt" and timestamp < 0:
    sec = 0
    microsec = 0
    if isinstance(timestamp, int):
        sec = timestamp
    else:
        whole, frac = str(timestamp).split(".")
        sec = int(whole)
        microsec = int(frac) * -1
    dt = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=sec, microseconds=microsec)
else:
    dt = datetime.datetime.fromtimestamp(timestamp, tzinfo)

print(dt)
# print(datetime.datetime.fromtimestamp(timestamp))
# print(int(int(-16502400000)/1000))
