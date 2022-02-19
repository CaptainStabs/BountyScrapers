import csv
from tqdm import tqdm
import datetime

# PARCEL,BOOK,PAGE,SALE_DATE,SALE_AMT,ADJ_SALE_AMT,,DOR_DESCRITION,GRANTOR,GRANTEE,BLDG_NUM,SITUS,ZIP_CODE,ZIP_CITY,
columns = ["property_id", "book", "page", "sale_date", "sale_price", "property_type", "seller_name", "buyer_name", "num_units", "physical_address", "zip5", "city", "county", "state", "source_url"]
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                timestamp = datetime.datetime.fromtimestamp((int(row["SALE_DATE"])/1000))
                land_info = {
                    "property_id": row["PARCEL"],
                    "sale_date": timestamp,
                    "sale_price": row["SALE_AMT"],
                    "property_type": " ".join(str(row["DOR_DESCRITION"]).upper().split()),
                    "seller_name": " ".join(str(row["GRANTOR"]).upper().replace(",", ", ").split()),
                    "buyer_name": " ".join(str(row["GRANTEE"]).upper().split()),
                    "physical_address": " ".join(str(row["SITUS"]).upper().split()),
                    "zip5": row["ZIP_CODE"],
                    "city": str(row["ZIP_CITY"]).upper(),
                    "county": "ORANGE",
                    "state": "FL",
                    "source_url": "https://vgispublic.ocpafl.org/server/rest/services/DYNAMIC/Sales/MapServer/2",
                }

                # Delete if no book
                # Update field
                book = str(row["BOOK"]).strip()
                page = str(row["PAGE"]).strip()

                try:
                    if int(book) > 0 and int(page) > 0:
                        land_info["book"] = book
                        land_info["page"] = page

                except ValueError:
                    pass


                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                try:
                    # Delete if no unit count
                    if int(row["BLDG_NUM"]) != 0:
                        land_info["num_units"] = row["BLDG_NUM"]
                except ValueError:
                    pass

                year = land_info["sale_date"].year

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except Exception as e:
                raise e
                pass
