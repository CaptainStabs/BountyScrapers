import csv
import os
from tqdm import tqdm

columns = ["name", "business_type", "state_registered","street_physical"]
filename = "mississippi.csv"

with open(filename, "r") as input_csv:
    line_count = 0

    for line in input_csv.readlines():
        line_count += 1

    input_csv.seek(0)

    csv_reader = csv.DictReader(input_csv, fieldnames=columns)

    with open("mississippi_cleaned.csv", "a", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=columns)

        if os.stat("mississippi_cleaned.csv").st_size == 0:
            writer.writeheader()

        for index, row in tqdm(enumerate(csv_reader)):
            if index == 0:
                continue

            street_physical = str(row["street_physical"])
            if street_physical.count(",") == 1:
                street_list = street_physical.split(",")
                if str(street_list[0]).strip() == str(street_list[1]).strip().lstrip("Â "):
                    street_physical_output = street_list[0]
                    print("\n" + street_physical.replace("Â ", ""))

                    business_info = {
                        "name":row["name"],
                        "business_type":row["business_type"],
                        "state_registered":row["state_registered"],
                        "street_physical": street_physical_output
                    }

                    writer.writerow(business_info)
