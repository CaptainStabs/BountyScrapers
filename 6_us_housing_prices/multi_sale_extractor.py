import csv
from tqdm import tqdm
from dateutil import parser

# PIN,PropertySt,Sale1D,Sale2D,Sale3D,Sale1Amt,Sale2Amt,Sale3Amt,,CondDesc,GrantorNam,GrantorN1,GrantorN_2,,YrBuilt,
columns = ["property_id", "physical_address", "sale_date", "sale_price", "property_type", "seller_name", "year_built", "county", "state", "source_url"]
with open("Parcels_Proval_010622.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PIN"],
                    "physical_address": " ".join(str(row["PropertySt"]).upper().split()),
                    "property_type": " ".join(str(row["CondDesc"]).split()),
                    "county": "Union",
                    "state": "NC",
                    "source_url": "https://www.unioncountync.gov/government/departments-f-p/gis-mapping/downloadable-gis-data"
                }

                # Delete if no year_built
                try:
                    if int(row["YrBuilt"]) != 0 and int(row["YrBuilt"]) <= 2022:
                        land_info["year_built"] = row["YrBuilt"]

                except ValueError:
                    pass

                for i in range(1,4):
                # date_list = [str(row[f"Sale{x}D"]).strip() for x in range(1,4)]
                    try:
                        land_info["sale_date"] = str(parser.parse(row[f"Sale{i}D"]))
                        land_info["sale_price"] = row[f"Sale{i}Amt"]
                        land_info["seller_name"] = row[f"GrantorN{i}"]
                    except parser._parser.ParserError:
                        continue

                    year = land_info["sale_date"].split("-")[0]

                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                        writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
