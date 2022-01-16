import os
import csv
from tqdm import tqdm
from dateutil import parser

directory = ".\\files\\0\\"

# PROPID,SALEPRICE,SALEDATE,SITUSNUMBER,SITUSSTREET,SITUSCITYSTATEZIP,SELLERNAME,BUYERNAME,YEARBUILT,
columns = ["property_id", "sale_price", "sale_date", "physical_address", "city", "state", "zip5", "seller_name", "buyer_name", "year_built"]

with open("0_extracted_data.csv", "a", encoding="utf-8", newline="") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    writer.writeheader()

    for file in tqdm(os.listdir(directory)):
        with open(os.path.join(directory,file), "r", encoding="utf-8") as input_csv:
            reader = csv.DictReader(input_csv)

            for row in reader:
                land_info = {
                    "property_id": row["PROPID"],
                    "seller_name": " ".join(str(row["SELLERNAME"]).upper().strip().split()),
                    "buyer_name": " ".join(str(row["BUYERNAME"]).upper().strip().split()),
                }

                street_list = [str(row["SITUSNUMBER"]).strip(), str(row["SITUSSTREET"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(str(' '.join(filter(None, street_list)).upper()).split())

                city_state_zip = str(row["SITUSCITYSTATEZIP"]).split(" ")
                if len(city_state_zip) > 1:
                    print(city_state_zip, len(city_state_zip))
                    land_info["city"] = city_state_zip[0].strip().rstrip(",")
                    land_info["state"] = city_state_zip[1].strip()

                    if "-" in city_state_zip[2]:
                        land_info["zip5"] = str(city_state_zip[2]).split("-")[0]
                    else:
                        land_info["zip5"] = city_state_zip[2].strip()

                sale_date = row["SALEDATE"]

                if sale_date != "":
                    land_info["sale_date"] = parser.parse(sale_date)

                land_info["sale_price"] = row["SALEPRICE"].split(".")[0]

                if land_info["buyer_name"] == "MISSING BUYER RECORD":
                    land_info["buyer_name"] = ""

                if land_info["seller_name"] == "MISSING SELLER RECORD":
                    land_info["seller_name"] = ""

                if land_info["sale_price"] and land_info["sale_date"] and land_info["physical_address"]:
                    writer.writerow(land_info)
