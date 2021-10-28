import csv
import os

fieldnames_input = ["name", "business_type", "state_registered","street_registered","city_registered","zip5_registered", "corp_id"]
fieldnames_output = ["name", "business_type", "state_registered","street_registered","city_registered","zip5_registered", "filing_id"]

with open("alabama_merged_data.csv", "r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file, fieldnames=fieldnames_input)

    with open("alabama_cleaned_merged_data.csv", "a", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames_output)

        if os.stat("alabama_cleaned_merged_data.csv").st_size == 0:
            writer.writeheader()

        for index, row in enumerate(reader):
            if index == 0:
                continue

            if "-" in row["zip5_registered"]:
                zip5_registered = row["zip5_registered"].split("-")[0]

            else:
                zip5_registered = row["zip5_registered"]

            filing_id = str(row["corp_id"])
            string_center = len(filing_id)//2
            filing_id = filing_id[:string_center] + "-" + filing_id[string_center:]

            output_dict = {
                "name": " ".join(str(row["name"]).split()).strip(),
                "business_type": row["business_type"],
                "state_registered": row["state_registered"],
                "street_registered": " ".join(str(row["street_registered"]).split()).strip().strip(",").strip("-"),
                "city_registered": " ".join(str(row["city_registered"]).split()).strip().strip(",").strip("-"),
                "zip5_registered": zip5_registered,
                "filing_id": filing_id
            }

            writer.writerow(output_dict)
