import csv
from tqdm import tqdm
from dateutil import parser
import sys
from pathlib import Path

p = Path(__file__).resolve().parents[1]
sys.path.insert(1, str(p))
from _common import date_parse

# OBJECTID,PROP_ID,LOT_SIZE,LS_DATE,LS_PRICE,USE_CODE,SITE_ADDR,ADDR_NUM,FULL_STR,LOCATION,
# CITY,ZIP,LS_BOOK,LS_PAGE,YEAR_BUILT,BLD_AREA,UNITS,STYLE,NUM_ROOMS,LOT_UNITS,TOWN_ID,MA_PROP_ID,FULL_STR_STD,STORIES_NUM,STORIES,CAMA_ID
columns = ["property_id", "land_area_acres", "sale_datetime", "sale_price", "property_city", "property_zip5", "buyer_1_name", "building_year_built", "building_area_sqft", "building_num_units", "state", "property_street_address", "source_url", "book", "page", "building_num_stories"]
with open("massachussets.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PROP_ID"],
                    "land_area_acres": row["LOT_SIZE"],
                    "sale_datetime": date_parse(row["LS_DATE"]),
                    "sale_price": row["LS_PRICE"],
                    "property_city": row["CITY"],
                    "property_zip5": row["ZIP"],
                    "buyer_1_name": "",
                    "building_year_built": row["YEAR_BUILT"],
                    "building_area_sqft": row["BLD_AREA"],
                    "building_num_units": row["UNITS"],
                    "state": "MA",
                    "source_url": "https://www.mass.gov/forms/massgis-request-statewide-parcel-data",
                    "building_num_stories": row["STORIES"]
                }

                # If address is in separate fields
                if str(row["SITE_ADDR"]).strip():
                    land_info["property_street_address"] = " ".join(str(row["SITE_ADDR"]).upper().split()).strip()
                else:
                    # ADDR_NUM,FULL_STR,LOCATION,
                    street_list = [str(row["ADDR_NUM"]).strip(), str(row["FULL_STR"]).strip(), str(row["LOCATION"]).strip()]

                    # concat the street parts filtering out blank parts
                    land_info["property_street_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no book
                # Update field
                book = str(row["LS_BOOK"]).strip()
                page = str(row["LS_PAGE"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                # Delete if no year_built
                try:
                    if int(row["YEAR_BUILT"]) != 0 and int(row["YEAR_BUILT"]) <= 2022:
                        land_info["building_year_built"] = row["YEAR_BUILT"]

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["property_zip5"] == "00000" or land_info["property_zip5"] == "0" or len(land_info["property_zip5"]) != 5:
                    land_info["property_zip5"] = ""

                year = land_info["sale_datetime"].year

                if land_info["property_street_address"] and land_info["sale_datetime"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
