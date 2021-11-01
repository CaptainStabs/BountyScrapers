import csv
from tqdm import tqdm
from utils import us_state_abbrev
import os

input_columns = ["name", "business_type", "state_registered", "street_registered", "city_registered", "zip5_registered", "state_physical", "street_physical", "city_physical", "zip5_physical", "filing_number", "agent_name", "agent_title", "raw_physical_address", "raw_registered_address"]
output_columns = ["name", "business_type", "state_registered", "street_registered", "city_registered", "zip5_registered", "state_physical", "street_physical", "city_physical", "zip5_physical", "filing_number"]
filename = "pa_cleaned_merged_data.csv"

with open("pa_merged_data.csv", "r", encoding="utf-8") as input_csv:
    lines = input_csv.readlines()
    total = 0
    for line in tqdm(lines):
        total += 1

    del lines

    input_csv.seek(0)

    reader = csv.DictReader(input_csv, fieldnames=input_columns)

    with open(filename, "a", newline="", encoding="utf-8") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=output_columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        for i, row in tqdm(enumerate(reader), total=total):
            business_info = {}
            if i == 0:
                continue

            save_row = True
            business_info = {
                "name": row["name"],
                "business_type": row["business_type"],
                "street_registered": row["street_registered"],
                "city_registered": row["city_registered"],
                "street_physical": row["street_physical"],
                "city_physical": row["city_physical"],
                "filing_number": row["filing_number"]
            }

            if row["state_registered"] == "NULL":
                save_row = False

            else:
                if len(row["state_registered"]) != 2:
                    save_row = False
                else:
                    save_row = True
                    business_info["state_registered"] = row["state_registered"]
                    # print(row["state_registered"])

            if "-" in row["zip5_registered"]:
                zip5_list = row["zip5_registered"].split("-")
                if len(zip5_list[0]) != 5:
                    if len(zip5_list[1]) == 5:
                        business_info["zip5_registered"] = zip5_list[1]
                        print("   [*] Second part of zip5_list is equal to 5")
                elif len(zip5_list[0]) == 5:
                    business_info["zip5_registered"] = zip5_list[0]

            if "-" in row["zip5_physical"]:
                zip5_list = row["zip5_physical"].split("-")
                if len(zip5_list[0]) != 5:
                    if len(zip5_list[1]) == 5:
                        business_info["zip5_ physical"] = zip5_list[1]
                        print("   [*] Second part of zip5_list is equal to 5")
                elif len(zip5_list[0]) == 5:
                    business_info["zip5_physical"] = zip5_list[0]

            if row["state_physical"] != "NULL":
                if len(row["state_physical"]) != 2:
                    business_info["state_physical"] = row["state_physical"][:2]

            if save_row:
                writer.writerow(business_info)
