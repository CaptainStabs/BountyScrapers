import csv
from tqdm import tqdm
from dateutil import parser
from pathlib import Path
import sys

from pathlib import Path
import sys

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))
from _sale_type.sale_type import sale_type


# "strap","Tdate","deed_type","price",,"city","bldgClassDscr","builtYear","UnitCount"
columns = ["property_id", "sale_date", "sale_type", "sale_price", "physical_address", "city", "property_type", "year_built", "unit_count",  "zip5", "county", "state", "source_url"]
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
                    "property_id": str(row["strap"]).strip(),
                    "sale_date": str(parser.parse(row["Tdate"])),
                    "sale_price": row["price"],
                    "city": " ".join(str(row["city"]).upper().split()),
                    "property_type": " ".join(str(row["bldgClassDscr"]).upper().split()),
                    "county": "BOULDER",
                    "state": "CO",
                    "source_url": "https://hub.arcgis.com/documents/d39100d04be34354b97ad52874f5e7d4/explore",
                }

                # "mailingAddr1","mailingCity","mailingState","mailingZip",
                # If address is in separate fields
                # "str_num","str_pfx","str","str_sfx","str_unit"
                street_list = [str(row["str_num"]).strip(), str(row["str_pfx"]).strip(), str(row["str"]).strip(), str(row["str_sfx"]).strip(), str(row["str_unit"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                if " ".join(str(row["mailingAddr1"]).upper().split()) == land_info["physical_address"]:
                    land_info["zip5"] = row["mailingZip"][:5]

                # Delete if no year_built
                try:
                    if int(row["builtYear"]) != 0 and int(row["builtYear"]) <= 2022:
                        land_info["year_built"] = row["builtYear"]

                except ValueError:
                    pass

                try:
                    # Delete if no zip5
                    if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                        land_info["zip5"] = ""
                except KeyError:
                    pass

                try:
                    # Delete if no unit count
                    if int(row["UnitCount"]) != 0:
                        land_info["num_units"] = row["UnitCount"]
                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
