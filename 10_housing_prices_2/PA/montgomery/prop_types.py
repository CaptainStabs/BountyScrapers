import csv

with open("property_types.csv", "r") as f:
    reader = csv.reader(f)
    dict_from_csv = {rows[0]:rows[2] for rows in reader}
    print(dict_from_csv)
