import re


a = "American, 1883-5124"

date_pat = re.compile(r"\d{4}-\d{4}|\d{4}-")
dates = re.findall(date_pat, a)
dates = dates[0] if dates else None

if dates:
    death = dates.split("-")[-1] if len(dates.split("-")) > 1 else None
else:
    death = None
print(dates, death)
# print(re.findall(date_pat, a))
