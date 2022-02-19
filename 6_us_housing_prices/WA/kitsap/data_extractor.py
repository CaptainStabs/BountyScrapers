import csv
from tqdm import tqdm
from dateutil import parser

# "RP_ACCT_ID","SALE_DATE","PRICE","FULL_ADDR","CITY","STATE","ZIP_CODE","USE_CLASS"
columns = ["property_id", "sale_date", "sale_price", "physical_address", "city", "zip5", "property_type", "county", "state", "source_url"]
with open("Parcel.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["RP_ACCT_ID"],
                    "sale_date": str(parser.parse(row["SALE_DATE"])),
                    "sale_price": str(row["PRICE"]).split(".")[0],
                    "physical_address": " ".join(str(row["FULL_ADDR"]).upper().split()),
                    "city": " ".join(str(row["CITY"]).upper().split()),
                    "state": str(row["STATE"]).upper(),
                    "zip5": row["ZIP_CODE"],
                    "property_type": " ".join(str(row["USE_CLASS"]).upper().split()),
                    "county": "KITSAP",
                    "state": "WA",
                    "source_url": "https://www.kitsapgov.com/dis/Pages/resources.aspx",
                }


                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
