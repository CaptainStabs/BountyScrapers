import csv


with open("t", "r") as input_csv:
    reader = csv.DictReader(input_csv)

    for row in reader:
        print(" ".join(row["Situs_Address"].split()))
