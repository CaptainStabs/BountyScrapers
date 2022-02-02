import csv
from tqdm import tqdm
import datetime
import traceback as tb

# NEWPIN,,DEEDBOOK,DEEDPAGE,DEEDDATE,SALE_PRICE,,SITUS_ADDRESS,
columns = ["property_id", "book", "page", "sale_date", "sale_price", "physical_address", "county", "state", "source_url"]
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                temp_timestamp = int(row["DEEDDATE"])
                if temp_timestamp < 0:
                    timestamp = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=temp_timestamp/1000)
                    print(timestamp)
                else:
                    timestamp = temp_timestamp

                land_info = {
                    "property_id": str(row["NEWPIN"]).strip(),
                    "sale_date": datetime.datetime.fromtimestamp((timestamp/1000)),
                    "sale_price": row["SALE_PRICE"],
                    "physical_address": " ".join(str(row["SITUS_ADDRESS"]).upper().split()),
                    "county": "WARREN",
                    "state": "NC",
                    "source_url": "https://arcgis5.roktech.net/arcgis/rest/services/Warren/RokMap/MapServer/3",
                }


                # Delete if no book
                # Update field
                book = str(row["DEEDBOOK"]).strip()
                page = str(row["DEEDPAGE"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                year = land_info["sale_date"].year

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except ValueError as e:
                print(e)
                pass
            except Exception as e:
                # tb.print_exc()
                print(row["DEEDDATE"])
                print(e)
                pass
