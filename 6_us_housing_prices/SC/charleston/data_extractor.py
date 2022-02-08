import csv
from tqdm import tqdm
from dateutil import parser
import traceback as tb
import datetime

# "PROP_ST_NO","PROP_ST_NAME","PROP_TYPE"
# "PARCELPID", "CLASS_CODE",,"PROP_CITY","PROP_ZIP",,"SALE_PRICE","RECORDED_DATE"
columns = ["property_id", "property_type", "physical_address", "city", "zip5", "sale_price", "sale_date", "county", "state", "source_url"]
with open("Sales.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                timestamp = int(row["RECORDED_DATE"])
                land_info = {
                    "property_id": row["PARCELPID"],
                    "property_type": " ".join(str(row["CLASS_CODE"]).upper().split()),
                    "city": " ".join(str(row["PROP_CITY"]).upper().split()),
                    "sale_price": row["SALE_PRICE"],
                    "sale_date": datetime.datetime.fromtimestamp((timestamp/1000)),
                    "county": "CHARLESTON",
                    "state": "SC",
                    "source_url": "https://gisccapps.charlestoncounty.org/arcgis/rest/services/ProVal/ParcelMap/MapServer/0/",
                }

                if "-" in row["PROP_ZIP"]:
                    land_info["zip5"] = row["PROP_ZIP"].split("-")[0]
                else:
                    land_info["zip5"] = row["PROP_ZIP"]

                # If address is in separate fields
                # "PROP_ST_NO","PROP_ST_NAME","PROP_TYPE"
                street_list = [str(row["PROP_ST_NO"]).strip(), str(row["PROP_ST_NAME"]).strip(), str(row["PROP_TYPE"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()


                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or land_info["zip5"] == "99999" or len(land_info["zip5"]) != 5 or land_info["zip5"] == "+++++":
                    land_info["zip5"] = ""

                year = land_info["sale_date"].year

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except ValueError as e:
                # print(row["RECORDED_DATE"])
                pass

            except Exception as e:
                # tb.print_exc()
                # print(int(row["RECORDED_DATE"]))
                # print(e)
                pass
