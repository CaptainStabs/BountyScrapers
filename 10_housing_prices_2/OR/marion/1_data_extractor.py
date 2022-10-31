import os
import csv
from tqdm import tqdm
from dateutil import parser
import usaddress
import re

from pathlib import Path
import sys

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))

from _sale_type.sale_type import sale_type


directory = ".\\files\\1\\"
pat = re.compile("(?<=\w, )[A-Z][A-Z](?:(?= \d)|(?=  \d))")

# PROPID,SALEPRICE,SALEDATE,SITUSNUMBER,SITUSSTREET,SITUSCITYSTATEZIP,SELLERNAME,BUYERNAME,YEARBUILT,
columns = ["property_id", "sale_price", "sale_date", "physical_address", "city", "state", "zip5", "seller_name", "buyer_name", "building_year_built", "sale_type", "source_url", "land_area_acres", "land_area_sqft", "buyer_1_state", "seller_1_state"]

with open("1_extracted_data.csv", "a", encoding="utf-8", newline="") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    writer.writeheader()

    for file in tqdm(os.listdir(directory)):
        with open(os.path.join(directory,file), "r", encoding="utf-8") as input_csv:
            reader = csv.DictReader(input_csv)

            for row in reader:
                land_info = {
                    "property_id": row["\ufeffPROPID"],
                    "seller_name": " ".join(str(row["SELLERNAME"]).upper().strip().split()),
                    "buyer_name": " ".join(str(row["BUYERNAME"]).upper().strip().split()),
                    "source_url": "https://www.co.marion.or.us/AO/Pages/datacenter.aspx"
                }
                try:
                    land_info["sale_type"] = sale_type[row["DEEDTYPE"].upper().replace("_", "").strip()]

                except KeyError:
                    land_info["sale_type"] = str(row["DEEDTYPE"].upper().replace("_", "").strip())

                if "Missing Situs Address Record" not in row["SITUSSTREET"]:
                    situs_number = row["SITUSNUMBER"]
                    if ".0" in situs_number:
                        situs_number = situs_number.replace(".0", "")

                    street_list = [situs_number, str(row["SITUSSTREET"]).strip()]

                    # concat the street parts filtering out blank parts
                    land_info["physical_address"] = ' '.join(str(' '.join(filter(None, street_list)).upper()).split())

                    city_state_zip = row["SITUSCITYSTATEZIP"]

                    try:
                        parsed_address = usaddress.tag(city_state_zip)

                    except usaddress.RepeatedLabelError as e:
                        print(e)

                    try:
                        land_info["city"] = " ".join(str(parsed_address[0]["PlaceName"]).strip().rstrip(",").upper().split())
                    except KeyError:
                        # print("Error on city:", city_state_zip)
                        pass

                    try:
                        land_info["state"] = str(parsed_address[0]["StateName"]).upper().strip()

                    except KeyError:
                        land_info["state"] = "OR"
                        # print("Error on state:", city_state_zip)
                        pass

                    try:
                        zip5 = str(parsed_address[0]["ZipCode"]).strip()

                        if "-" in zip5:
                            zip5 = zip5.split("-")[0]

                        land_info["zip5"] = zip5
                    except KeyError:
                        # print("Error on zip:", city_state_zip)
                        pass

                    sale_date = row["SALEDATE"]

                    if sale_date != "":
                        land_info["sale_date"] = parser.parse(sale_date)

                    land_info["sale_price"] = row["SALEPRICE"].split(".")[0]

                    if land_info["buyer_name"] == "MISSING BUYER RECORD" or "UNKNOWN" in land_info["buyer_name"]:
                        land_info["buyer_name"] = ""

                    if land_info["seller_name"] == "MISSING SELLER RECORD" or "UNKNOWN" in land_info["seller_name"]:
                        land_info["seller_name"] = ""

                    land_info["land_area_acres"] = row["ACRES"]
                    land_info["land_area_sqft"] = row["LANDSQFT"]

                    buyer = row["BUYERCSZ"]
                    buyer = re.findall(pat, buyer)
                    if buyer:
                        land_info["buyer_1_state"] = buyer[0]

                    seller = row["SELLERCSZ"]
                    seller = re.findall(pat, seller)
                    if seller:
                        land_info["seller_1_state"] = seller[0]

                    land_info["building_year_built"] = row["YEARBUILT"].split(".")[0]

                    if land_info["sale_price"] and land_info["sale_date"] and land_info["physical_address"]:
                        writer.writerow(land_info)
