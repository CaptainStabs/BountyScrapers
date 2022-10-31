from sale_type import sale_type
import csv
import json

with open("emap.csv", "r") as f:
    reader = csv.reader(f)
    mydict = {rows[0]:rows[1] for rows in reader if rows[0] not in sale_type.keys()}
    print(json.dumps(mydict, indent=2))
