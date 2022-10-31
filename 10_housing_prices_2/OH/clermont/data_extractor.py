import csv
from tqdm import tqdm
from dateutil import parser
import sys
from pathlib import Path

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))
from _common import date_parse

 # ,,,,
# PIN,,PRICE,SALESDATE,,YRBLT,STYLE,HYPERLINK,
# ACRES,DISTRICT,  ,CLASS,TAXCLASS,LAND_USE,,CARD_,SQ_FT,,,,FIXBATH,FIREPLCE,YRBLT,STYLE,CONSTR,BASEMENT,HEATING,CDU,CDPCT,GRADE,GRDFACT,MKTADJ,,PRCLID,HYPERLINK,IMPDATE,Shape_STAr,Shape_STLe
columns = ["property_id", "property_street_address", "sale_price", "sale_datetime", "building_year_built", "property_type", "sale_type", "property_county", "state", "source_url", "land_area_acres", "property_township", "building_area_sqft", "building_num_stories", "building_num_beds", "building_num_baths"]
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": str(row["PIN"]).strip(),
                    "sale_price": row["PRICE"],
                    "sale_datetime": str(date_parse(row["SALESDATE"])),
                    "property_type": " ".join(str(row["STYLE"]).upper().split()),
                    "sale_type": str(row["SALETYPE"]).upper().strip(),
                    "property_county": "CLERMONT",
                    "state": "OH",
                    "source_url": row["HYPERLINK"],
                    "land_area_acres": row["ACRES"],
                    "property_township": row["DISTRICT"],
                    "building_area_sqft": row["SQ_FT"],
                    "building_num_stories": row["STORIES"],
                    "building_num_beds": row["RMBED"],
                    "building_num_baths": row["FIXBATH"],
                }

                # If address is in separate fields
                street_list = [str(row["ADRNO"]).strip(), str(row["ADRADD"]).strip(), str(row["ADRDIR"]).strip(), str(row["ADRSTR"]).strip(), str(row["ADRSUF"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["property_street_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no year_built
                try:
                    if int(row["YRBLT"]) != 0 and int(row["YRBLT"]) <= 2022:
                        land_info["building_year_built"] = row["YRBLT"]

                except ValueError:
                    pass

                year = land_info["sale_datetime"].split("-")[0]

                if land_info["property_street_address"] and land_info["sale_datetime"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
