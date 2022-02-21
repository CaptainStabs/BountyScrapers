import csv
from tqdm import tqdm
from dateutil import parser
import yaml
from pathlib import Path
import sys

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))

from _sale_type.sale_type import sale_type

with open("C:\\Users\\adria\\github\\BountyScrapers\\6_us_housing_prices\\__geocoding\\us_zipcodes.yaml", "r") as f:
    zip_cty_cnty = yaml.safe_load(f)

# "PARCELNB","GRANTOR","GRANTEE","SALEP","SALEDT","DEEDTYPE","BLDGS","OCCCODE1","YRBLT","LANDTYPE",,"LOCZIP","LOCCITY"
columns = ["property_id", "seller_name", "buyer_name", "sale_price", "sale_date", "sale_type", "num_units", "property_type", "year_built", "physical_address", "zip5", "city", "county", "state", "source_url"]
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
                    "property_id": str(row["PARCELNB"]).strip(),
                    "seller_name": " ".join(str(row["GRANTOR"]).upper().split()),
                    "buyer_name": " ".join(str(row["GRANTEE"]).upper().split()),
                    "sale_price": row["SALEP"],
                    "sale_date": str(parser.parse(row["SALEDT"])),
                    "zip5": row["LOCZIP"],
                    "city": " ".join(str(row["LOCCITY"]).upper().split()),
                    "county": "WELD",
                    "state": "CO",
                    "source_url": "https://www.weldgov.com/Government/Departments/Assessor/Data-Download/All-Data-CSV",
                }

                if len(land_info["zip5"]) > 5:
                    land_info["zip5"] = land_info["zip5"][:5]

                if row["OCCCODE1"]:
                    land_info["property_type"] = str(row["OCCCODE1"]).upper().strip()
                else:
                    land_info["property_type"] = str(row["LANDTYPE"]).upper().strip()

                try:
                    land_info["sale_type"] = sale_type[str(row["DEEDTYPE"]).upper().strip()]
                except KeyError:
                    land_info["sale_type"] = str(row["DEEDTYPE"]).upper().strip()

                # If address is in separate fields
                # "","","STREETDIR","STREETSUF","STREETNAME"
                street_list = [str(row["STREETNO"]).strip(), str(row["STREETALP"]).strip(), str(row["STREETDIR"]).strip(), str(row["STREETSUF"]).strip(), str(row["STREETNAME"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no year_built
                try:
                    if int(row["YRBLT"]) != 0 and int(row["YRBLT"]) <= 2022:
                        land_info["year_built"] = row["YRBLT"]

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                if not land_info["city"]:
                    try:
                        land_info["city"] = str(zip_cty_cnty[row["zip5"]["city"]]).upper().strip()
                    except KeyError:
                        pass

                try:
                    # Delete if no unit count
                    if int(row["BLDGS"]) != 0:
                        land_info["num_units"] = row["BLDGS"]
                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "":
                    if int(year) < 2022:
                        writer.writerow(land_info)
                    else:
                        if int(year) > 2022:
                            continue
                        else:
                            month = land_info["sale_date"].split("-")[1]
                            if int(month) <= 2:
                                writer.writerow(land_info)


            except parser._parser.ParserError:
                pass
