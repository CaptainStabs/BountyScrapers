import csv
from tqdm import tqdm
import datetime

# PARCEL,SALE_DATE,SITUS,SALE_AMOUNT,CITY_SITUS,ZIP_SITUS
columns = ["property_id", "sale_date", "sale_price", "physical_address", "zip5", "city", "county", "state", "source_url"]
with open("CondoSales.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("condos_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                timestamp = datetime.datetime.fromtimestamp((int(row["SALE_DATE"])/1000))
                land_info = {
                    "property_id": row["PARCEL"],
                    "sale_date": timestamp,
                    "sale_price": row["SALE_AMOUNT"],
                    "physical_address": " ".join(str(row["SITUS"]).upper().split()),
                    "zip5": row["ZIP_SITUS"],
                    "city": str(row["CITY_SITUS"]).upper(),
                    "county": "ORANGE",
                    "state": "FL",
                    "source_url": "https://vgispublic.ocpafl.org/server/rest/services/DYNAMIC/Sales/MapServer/2",
                }


                year = land_info["sale_date"].year

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except Exception as e:
                raise e
                pass
