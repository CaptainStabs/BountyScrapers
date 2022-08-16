import csv
from tqdm import tqdm
from dateutil import parser

# ,OTALAREA,HEATEDAREA,MAXSTORIES,BEDROOMS,BATHROOMS,GARAGE,CARPORT,POOL,BOATDOCK,SEAWALL,NBLDGCOUNT,NMINBUILTY,NMAXBUILTY,NTOTALAREA,NHEATEDARE,NMAXSTORIE,NBEDROOMS,NBATHROOMS,NGARAGE,NCARPORT,NPOOL,NBOATDOCK,NSEAWALL,O_NAME,O_OTHERS,O_CAREOF,O_ADDR1,O_ADDR2,O_CITY,O_STATE,O_ZIP,O_COUNTRY,S_1DATE,S_1AMOUNT,S_1VI,S_1TC,S_1TOC,S_1OR_NUM,S_2DATE,S_2AMOUNT,S_2VI,S_2TC,S_2TOC,S_2OR_NUM,S_3DATE,S_3AMOUNT,S_3VI,S_3TC,S_3TOC,S_3OR_NUM,S_4DATE,S_4AMOUNT,S_4VI,S_4TC,S_4TOC,S_4OR_NUM,LEGAL,GARBDIST,GARBTYPE,GARBCOMCAT,GARBHEADER,GARBUNITS,CREATEYEAR,Property_U,
columns = ["property_id", "property_type", "physical_address", "city", "zip5", "num_units", "year_built", "sale_date", "sale_price", "county", "state", "source_url", "appraisal_total", "building_assessed_value", "land_assessed_value", "land_area_acres", "building_area_sqft", "building_num_stories", "building_num_beds", "building_num_baths", "sale_id"]
with open("Parcels.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": str(row["FOLIOID"]).split(".")[0],
                    "physical_address": " ".join(str(row["SITEADDR"]).upper().split()),
                    "property_type": " ".join(str(row["LANDUSEDES"]).split()),
                    "city": " ".join(str(row["SITECITY"]).upper().split()),
                    "zip5": str(row["SITEZIP"]).strip(),
                    "county": "LEE COUNTY",
                    "state": "FL",
                    "source_url": str(row["Property_U"]).strip(),
                    "assessed_total": row["ASSESSED"],
                    "building_assessed_value": row["BUILDING"],
                    "land_assessed_value": row["LAND"],
                    "land_area_acres": row["GISACRES"],
                    "building_area_sqft": row["TOTALAREA"],
                    "building_num_stories": row["MAXSTORIES"],
                    "building_num_beds": row["BEDROOMS"],
                    "building_num_baths": row["BATHROOMS"]
                }

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                try:
                    # Delete if no unit count
                    if int(row["BLDGCOUNT"]) != 0:
                        land_info["num_units"] = row["BLDGCOUNT"]
                except ValueError:
                    pass

                # Delete if no year_built
                try:
                    if int(row["MINBUILTY"]) != 0 and int(row["MINBUILTY"]) <= 2022:
                        land_info["year_built"] = row["MINBUILTY"]

                except ValueError:
                    pass

                for i in range(1,4):
                # date_list = [str(row[f"Sale{x}D"]).strip() for x in range(1,4)]
                    try:
                        land_info["sale_date"] = str(parser.parse(row[f"S_{i}DATE"]))
                        land_info["sale_price"] = str(row[f"S_{i}AMOUNT"]).split(".")[0]
                        land_info["sale_id"] = row[f"S_{i}OR_NUM"]
                        year = land_info["sale_date"].split("-")[0]

                        if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                            writer.writerow(land_info)
                    except parser._parser.ParserError:
                        pass


            except parser._parser.ParserError:
                pass
