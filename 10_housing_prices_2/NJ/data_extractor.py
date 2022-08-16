import csv
from tqdm import tqdm
from dateutil import parser
import functools

@functools.lru_cache(maxsize=None)
def date_parse(date):
    return parser.parse(date)

# GIS_PIN,COUNTY,MUN_NAME,PROP_LOC,,FAC_NAME,DEED_BOOK,DEED_PAGE,DEED_DATE,YR_CONSTR,,SALE_PRICE,,ZIP5
columns = ["property_id", "county", "city", "property_street_address", "property_type", "book", "page", "sale_datetime", "building_year_built", "sale_price", "zip5", "state", "source_url", "appraisal_total", "land_area_acres", "land_assessed_value", "building_assessed_value", "appraisal_total"]
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
                    "property_id": row["GIS_PIN"],
                    "county": " ".join(str(row["COUNTY"]).upper().split()),
                    "city": " ".join(str(row["MUN_NAME"]).upper().replace("CITY", "").split()),
                    "property_street_address": " ".join(str(row["PROP_LOC"]).upper().split()),
                    "property_type": " ".join(str(row["FAC_NAME"]).upper().split()),
                    "sale_datetime": str(date_parse(row["DEED_DATE"])),
                    "sale_price": row["SALE_PRICE"],
                    "zip5": str(row["ZIP5"]).strip(),
                    "state": "NJ",
                    "source_url": "https://www.arcgis.com/home/item.html?id=102a9bf3c6da4ca3b9b31f831a1e9f72",
                    "land_assessed_value": row["LAND_VAL"],
                    "building_assessed_value": row["IMPRVT_VAL"],
                    "assessed_total": row["NET_VALUE"],
                    "land_area_acres": row["CALC_ACRE"],

                }
                #
                # try:
                #     land_info["city"] = " ".join(str(row["MUN_NAME"]).upper().split())
                # except KeyError:
                #     pass

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
                    if int(row["YR_CONSTR"]) != 0 and int(row["YR_CONSTR"]) <= 2022 and int(row["YR_CONSTR"]) >= 1690:
                        land_info["building_year_built"] = row["YR_CONSTR"]

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                if "O" in land_info["zip5"]:
                    land_info["zip5"] = land_info["zip5"].replace("O", "0")

                try:
                    t = int(land_info["zip5"])
                except ValueError:
                    land_info["zip5"] = ""

                sale_date = land_info["sale_datetime"]
                year = sale_date.split("-")[0]

                if int(year) > 2021:
                    sale_date = "19" + str(year)[2:] + sale_date.replace(year, "")
                    land_info["sale_datetime"] = sale_date
                elif int(year) == 2021:
                    month = sale_date.split("-")[1]
                    day = sale_date.split("-")[2].split(" ")[0]
                    if int(month) == 12:
                        if int(day) > 13:
                            sale_date = "19" + str(year)[2:] + sale_date.replace(year, "")
                            land_info["sale_datetime"] = sale_date



                if land_info["property_street_address"] and land_info["sale_datetime"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
