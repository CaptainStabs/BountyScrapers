import csv
from dateutil import parser
import re
from tqdm import tqdm
#,TOTAL_UNITS,BLDG_DESC,BLDG_TYPE,UNITS,YEAR_BUILT
columns = ["property_id", "physical_address", "county", "state", "sale_date", "sale_price", "book", "page", "property_type", "num_units", "year_built", "source_url"]

with open("Parcels.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    # Seek back to 0 to allow csv to read full file
    input_csv.seek(0)

    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["NAD83_PIN"],
                    "physical_address": " ".join(str(row["LOCATION_ADDR"]).upper().strip().split()).strip(),
                    "county": "Cumberland",
                    "state": "NC",
                    "source_url": "https://co-cumberlandgis.opendata.arcgis.com/datasets/CumberlandGIS::parcels/about",
                    "property_type": " ".join(str(row["BLDG_DESC"]).split()).strip()
                }

                # If neither pkg_sale_date nor land_sale, try deed_date
                land_info["sale_date"] = str(parser.parse(row["DEED_DATE"]))
                land_info["sale_price"] = row["REVENUE_STAMPS"]

                book = row["DEED_BOOK"]
                page = row["DEED_PAGE"]

                # For some reason this prevents some rows from saving, but I have no idea why
                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = book
                        land_info["page"] = page
                except ValueError:
                    continue
                except Exception as e:
                    print(e)

                if int(row["TOTAL_UNITS"]) != 0:
                    land_info["num_units"] = row["TOTAL_UNITS"]

                if row["YEAR_BUILT"] != "0":
                    land_info["year_built"] = row["YEAR_BUILT"]

                if land_info["physical_address"] and land_info["sale_date"]:
                    writer.writerow(land_info)
                # else:
                #     import json
                #     print(json.dumps(land_info, indent=2))

            except parser._parser.ParserError:
                continue
