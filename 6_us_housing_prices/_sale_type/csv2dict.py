import csv
import json

with open("C:\\Users\\adria\\github\\BountyScrapers\\6_us_housing_prices\\_sale_type\\sale_types.csv", "r") as f:
    reader = csv.reader(f)
    mydict = {rows[0]:rows[1] for rows in reader}
    print(json.dumps(mydict, indent=2))
