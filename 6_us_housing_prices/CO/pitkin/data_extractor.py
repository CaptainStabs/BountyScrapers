import csv
from tqdm import tqdm
from dateutil import parser

# PIN,SITUS_ADDR,CITY,,SALE_PRICE,SALE_DATE,MODEL_TYPE,ACTUAL_YR_,
columns = ["property_id", "physical_address", "city", "sale_price", "sale_date", "property_type", "year_built", "county", "state", "source_url"]
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
                    "property_id": str(row["PIN"]).split(".")[0].strip(),
                    "physical_address": " ".join(str(row["SITUS_ADDR"]).upper().split()),
                    "city": str(row["CITY"]).strip(),
                    "sale_price": row["SALE_PRICE"],
                    "sale_date": str(parser.parse(row["SALE_DATE"])),
                    "property_type": str(row["MODEL_TYPE"]).strip(),
                    "county": "PITKIN",
                    "state": "CO",
                    "source_url": "https://pitkincounty.com/875/Land-Records"
                }

                # Delete if no year_built
                try:
                    if int(row["ACTUAL_YR_"]) != 0 and int(row["ACTUAL_YR_"]) <= 2022:
                        land_info["year_built"] = row["ACTUAL_YR_"]

                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
