import csv
from tqdm import tqdm
from dateutil import parser
# import heartrate; heartrate.trace(browser=True, daemon=True)

# ,PIN,,propUse,saleDate,salePrice,deedType,BldgCount,locCity,theAddress,
columns = ["property_id", "property_type", "sale_date", "sale_price", "num_units", "city", "physical_address", "sale_type", "county", "state", "source_url"]
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        skipped = 0
        failed = 0
        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PIN"],
                    "property_type": " ".join(str(row["propUse"]).upper().split()),
                    "sale_date": str(parser.parse(row["saleDate"])),
                    "sale_price": row["salePrice"],
                    "sale_type": row["deedType"].upper().strip(),
                    "city": " ".join(str(row["locCity"]).upper().split()),
                    "physical_address": " ".join(str(row["theAddress"]).upper().split()),
                    "county": "ROUTT",
                    "state": "CO",
                    "source_url": "https://data-routtgis.opendata.arcgis.com/datasets/parcels/",
                }

                if land_info["sale_type"] == "DEED":
                    land_info["sale_type"] = ""

                try:
                    # Delete if no unit count
                    if int(row["BldgCount"]) != 0:
                        land_info["num_units"] = row["BldgCount"]
                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)
                else:
                    skipped += 1
            except parser._parser.ParserError:
                failed += 1
                pass

        print(skipped)
        print(failed)
