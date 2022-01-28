import csv
from tqdm import tqdm
from dateutil import parser
# CITY,PARCEL_STREET_DIRECTION,PARCEL_STREET_NUMBER,PARCEL_STREET_NAME,PARCEL_UNIT,
# GPIN,FULL_ADDRESS,,,USE_DESCRIPTION,ZIP_CODE,NUMBER_UNITS_APARTMENT,LAST_SALE_DATE,LAST_SALE_PRICE,YEAR_BUILT,DEED_BOOK,DEED_PAGE,
columns = ["property_id", "physical_address", "property_type", "zip5", "num_units", "sale_date", "sale_price", "year_built", "book", "page", "county", "state", "source_url"]
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
                    "property_id": row["GPIN"],
                    "physical_address": " ".join(str(row["FULL_ADDRESS"]).upper().split()),
                    "property_type": str(row["USE_DESCRIPTION"]).strip().upper(),
                    "zip5": str(row["ZIP_CODE"]).strip(),
                    "sale_date": str(parser.parse(str(row["LAST_SALE_DATE"]))).replace("+00:00", ""),
                    "sale_price": row["LAST_SALE_PRICE"],
                    "county": "HENRICO",
                    "state": "VA",
                    "source_url": "https://data-henrico.opendata.arcgis.com/datasets/tax-parcels-cama-data-2",
                }

                # Delete if no book
                # Update field
                book = str(row["DEED_BOOK"]).strip()
                page = str(row["DEED_PAGE"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                # Delete if no year_built
                try:
                    if int(row["YEAR_BUILT"]) != 0 and int(row["YEAR_BUILT"]) <= 2022:
                        land_info["year_built"] = row["YEAR_BUILT"]

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                try:
                    # Delete if no unit count
                    if int(row["NUMBER_UNITS_APARTMENT"]) != 0:
                        land_info["num_units"] = row["NUMBER_UNITS_APARTMENT"]
                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]
                month = land_info["sale_date"].split("-")[1]



                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    if year == 2022 and month > 1:
                        continue
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
