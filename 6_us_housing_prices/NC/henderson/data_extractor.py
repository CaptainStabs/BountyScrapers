import csv

columns = ["state", "county", "property_id", "physical_address", "property_type", "year_built", "sale_price", "sale_date", "source_url"]
with open("sale_denali.csv", "r") as input_csv:
    reader = csv.DictReader(input_csv)
    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in reader:
            land_info = {
                "state": "NC",
                "county": "HENDERSON",
                "property_id": row["PAR_PARCEL_PK"].strip("'"),
                "physical_address": " ".join(row["LOCATION_ADDR"].split()).strip("'").strip(),
                "property_type": row["SALE_TYPE"].strip("'"),
                "sale_price": int(row["PRICE"].strip("'")),
                "sale_date": row["SALE_DATE"].strip("'"),
                "source_url": "https://hendersoncountync.sharefile.com/share/view/s8ceee93ece54dbb9/fod01be9-6fee-41e3-9de5-c8ce062aa493"
            }

            try:
                land_info["year_built"] = int(row["YEAR_BUILT"].strip("'"))
            except:
                continue
            writer.writerow(land_info)
