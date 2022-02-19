import csv
from tqdm import tqdm
from dateutil import parser
from pathlib import Path
import sys

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))

from _sale_type.sale_type import sale_type

# ,PIN,DWBook,DWPage,Sale_Date,Sale_Yr,Sales_Price,Dwelling_Style,,HouseNumber,SDIR,STREET,STYPE,ST_SUFFIX,TownshipLocationDescription,
columns = ["property_id", "book", "page", "sale_date", "sale_price", "property_type", "physical_address", "sale_type", "city", "county", "state", "source_url"]
with open("TaxSQL_Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": str(row["PIN"]).split(".")[0],
                    "sale_date": str(parser.parse(row["Sale_Date"])),
                    "sale_price": row["Sales_Price"],
                    "property_type": " ".join(str(row["Dwelling_Style"]).strip().split()).upper(),
                    "city": " ".join(str(row["TownshipLocationDescription"]).upper().strip().split()),
                    "county": "IREDELL",
                    "state": "NC",
                    "source_url": "https://iredell-datadown-iredell.opendata.arcgis.com/datasets/3433d6293c594e51ac2a6466103c808f_0"
                }

                try:
                    land_info["sale_type"] = sale_type[row["DocType"].upper().replace("_", "").strip()]

                except KeyError:
                    land_info["sale_type"] = str(row["DocType"]).upper().strip()

                # If address is in separate fields
                street_list = [str(row["HouseNumber"]).strip(), str(row["SDIR"]).strip(), str(row["STREET"]).strip(), str(row["STYPE"]).strip(), str(row["ST_SUFFIX"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no book
                # Update field
                book = str(row["DWBook"]).strip()
                page = str(row["DWPage"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                year = row["Sale_Yr"]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
