import csv
from tqdm import tqdm
import datetime

prop_types = {
    "R": "RESIDENTIAL",
    "C": "COMMERCIAL"
}
# Parcel,,Class,,Site_Full_,Site_Zip_C,Last_Sale_,Last_Sal_1,Year_Built
columns = ["property_id", "property_type", "physical_address", "zip5", "sale_date", "sale_price", "year_built", "county", "state", "source_url"]
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            timestamp = int(str(row["Last_Sale_"]).strip())
            try:
                land_info = {
                    "property_id": row["Parcel"],
                    "physical_address": " ".join(str(row["Site_Full_"]).upper().split()),
                    "zip5": row["Site_Zip_C"],
                    "sale_price": row["Last_Sal_1"],
                    "sale_date": datetime.datetime.fromtimestamp((timestamp/1000)),
                    "county": "MONTGOMERY",
                    "state": "PA",
                    "source_url": "https://mapservices.pasda.psu.edu/server/rest/services/pasda/MontgomeryCounty/MapServer/14",
                }

                try:
                    land_info["property_type"] = prop_types[row["Class"]]
                except KeyError:
                    land_info["property_type"] = row["Class"].upper().strip()


                # Delete if no year_built
                try:
                    if int(row["Year_Built"]) != 0 and int(row["Year_Built"]) <= 2022:
                        land_info["year_built"] = row["Year_Built"]

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""


                year = land_info["sale_date"].year

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except Exception as e:
                pass
