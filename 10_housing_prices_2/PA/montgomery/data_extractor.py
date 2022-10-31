import csv
from tqdm import tqdm
import datetime
import json
import os

with open("property_types.csv", "r") as f:
    reader = csv.reader(f)
    prop_types = {rows[0]:rows[2] for rows in reader}

prop_letter_types = {
    "R": "Residential",
    "C": "Commercial",
    "E": "Exempt",
    "U": "Utility",
    "I": "Industry",
    "A": "Apartment/Townhouse/Low-Rise"
}

# Parcel,,Class,,Site_Full_,Site_Zip_C,Last_Sale_,Last_Sal_1,Year_Built
columns = ["property_id", "property_type", "property_street_address", "property_zip5", "sale_datetime", "sale_price", "building_year_built", "property_county", "state", "source_url", "appraisal_total", "assessed_total", "land_area_acres", "building_area_sqft", "building_num_stories", "building_num_beds", 'building_num_baths', 'land_area_sqft']
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            timestamp = int(str(row["Last_Sale_"]).strip())
            if os.name == "nt" and timestamp < 0:
                sec = 0
                microsec = 0
                if isinstance(timestamp, int):
                    sec = timestamp
                else:
                    whole, frac = str(timestamp).split(".")
                    sec = int(whole)
                    microsec = int(frac) * -1
                dt = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=sec/1000, microseconds=microsec)
            else:
                dt = datetime.datetime.fromtimestamp(timestamp/1000)
            try:
                land_info = {
                    "property_id": row["Parcel"],
                    "property_street_address": " ".join(str(row["Site_Full_"]).upper().split()),
                    "property_zip5": row["Site_Zip_C"],
                    "sale_price": row["Last_Sal_1"],
                    "sale_datetime": dt,
                    "property_county": "MONTGOMERY",
                    "state": "PA",
                    "source_url": "https://mapservices.pasda.psu.edu/server/rest/services/pasda/MontgomeryCounty/MapServer/14",
                    "appraisal_total": row["Appraisal"],
                    "assessed_total": row["Assessment"],
                    "land_area_acres": row["Land_Acres"],
                    "land_area_sqft": row["Land_Squar"],
                    "building_area_sqft": row["Livable_Sq"],
                    "building_num_stories": row["Stories"],
                    "building_num_beds": row["Bedrooms"],
                    "building_num_baths": sum([float(row["Baths"]), float(row["Half_Baths"]) * 0.5])
                }


                try:
                    l_code = row["Land_Use_C"]
                    if l_code:
                        land_info["property_type"] = ": ".join([l_code, prop_types[l_code]])
                except KeyError:
                    if row["Class"].strip():
                        land_info["property_type"] = prop_letter_types[row["Class"]]


                # Delete if no year_built
                try:
                    if int(row["Year_Built"]) != 0 and int(row["Year_Built"]) <= 2022:
                        land_info["building_year_built"] = row["Year_Built"]

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["property_zip5"] == "00000" or land_info["property_zip5"] == "0" or len(land_info["property_zip5"]) != 5:
                    land_info["property_zip5"] = ""


                year = land_info["sale_datetime"].year

                if land_info["property_street_address"] and land_info["sale_datetime"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except Exception as e:
                raise e
                pass
