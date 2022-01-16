import os
import csv
from tqdm import tqdm
from dateutil import parser
import usaddress


directory = ".\\files\\2\\"

# PROPID,SALEPRICE,SALEDATE,SITUSNUMBER,SITUSSTREET,SITUSCITYSTATEZIP,SELLERNAME,BUYERNAME,YEARBUILT,
columns = ["property_id", "sale_price", "sale_date", "physical_address", "city", "state", "zip5", "seller_name", "buyer_name", "year_built", "source_url"]

with open(".\\extracted_data\\2_extracted_data.csv", "a", encoding="utf-8", newline="") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    writer.writeheader()

    for file in tqdm(os.listdir(directory)):
        with open(os.path.join(directory,file), "r", encoding="utf-8") as input_csv:
            reader = csv.DictReader(input_csv)

            for row in reader:
                land_info = {
                    "property_id": row["ROPID"],
                    "seller_name": " ".join(str(row["SELLERNAME"]).upper().strip().split()),
                    "buyer_name": " ".join(str(row["BUYERNAME"]).upper().strip().split()),
                    "source_url": "https://www.co.marion.or.us/AO/Pages/datacenter.aspx"
                }

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

                    land_info["year_built"] = row["YEARBUILT"].split(".")[0]

                    if land_info["sale_price"] and land_info["sale_date"] and land_info["physical_address"]:
                        writer.writerow(land_info)
