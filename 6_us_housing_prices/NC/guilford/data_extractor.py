import csv
from tqdm import tqdm
from dateutil import parser

    #,PIN_PLUS_EXT,,PHYADDR_ZIP,LOCATION_ADDR,DEED_DATE,DEED_BK_PG_NUM,REVENUE_STAMPS,TOTAL_UNITS,YEAR_BUILT,,BLDG_DESC
columns = ["property_id", "zip5", "physical_address", "sale_date", "book", "page", "sale_price", "num_units", "year_built", "property_type", "county", "state", "source_url"]
with open("MyFile_20220124110904.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PIN_PLUS_EXT"],
                    "zip5": row["PHYADDR_ZIP"],
                    "physical_address": " ".join(str(row["LOCATION_ADDR"]).upper().strip().split()),
                    "property_type": " ".join(str(row["BLDG_DESC"]).upper().strip().split()),
                    "county": "Guilford",
                    "state": "NC",
                    "source_url": "http://gis.guilfordcountync.gov/DataMining/default.aspx"
                }


                # Delete if no book
                # Update field
                try:
                    book = row["DEED_BK_PG_NUM"].split("-")[0]
                    page = row["DEED_BK_PG_NUM"].split("-")[1]

                    try:
                        if int(book) != 0 and int(page) != 0:
                            land_info["book"] = book
                            land_info["page"] = page

                    except ValueError:
                        pass
                except IndexError:
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

                # Delete if no unit count
                try:
                    if int(row["TOTAL_UNITS"]) != 0:
                        land_info["num_units"] = row["TOTAL_UNITS"]

                except ValueError:
                    pass

                if row["PKG_SALE_DATE"] and row["LAND_SALE_DATE"]:
                    for i in range(2):
                        if i == 0:
                            if row["PKG_SALE_DATE"]:
                                land_info["sale_date"] = str(parser.parse(row["PKG_SALE_DATE"]))
                                land_info["sale_price"] = row["PKG_SALE_PRICE"]
                        else:
                            if row["LAND_SALE_DATE"]:
                                land_info["sale_date"] = str(parser.parse(row["LAND_SALE_DATE"]))
                                land_info["sale_price"] = row["LAND_SALE_PRICE"]


                        year = land_info["sale_date"].split("-")[0]

                        if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                            writer.writerow(land_info)
                elif row["PKG_SALE_DATE"] and not row["LAND_SALE_DATE"]:
                    land_info["sale_date"] = str(parser.parse(row["PKG_SALE_DATE"]))
                    land_info["sale_price"] = row["PKG_SALE_PRICE"]

                    year = land_info["sale_date"].split("-")[0]
                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                        writer.writerow(land_info)

                elif row["LAND_SALE_DATE"] and not row["PKG_SALE_DATE"]:
                    land_info["sale_date"] = str(parser.parse(row["LAND_SALE_DATE"]))
                    land_info["sale_price"] = row["LAND_SALE_PRICE"]

                    year = land_info["sale_date"].split("-")[0]
                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                        writer.writerow(land_info)


            except parser._parser.ParserError:
                pass
