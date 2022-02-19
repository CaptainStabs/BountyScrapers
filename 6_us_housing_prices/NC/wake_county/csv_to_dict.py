import csv
import json

with open("tabula-CodeDescriptions.csv", "r") as f:
    reader = csv.reader(f)

    dict_from_csv = {rows[0]:rows[1] for rows in reader}
    print(json.dumps(dict_from_csv, indent=2))
