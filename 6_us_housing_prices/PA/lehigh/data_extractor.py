import csv
from tqdm import tqdm
from dateutil import parser

# ,PIN,,SMON,SYEAR,SPRICE,,,,ADDRESS,Web_WEB
columns = ["property_id", "sale_date", "sale_price", "physical_address", "county", "state", "source_url"]
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
                    "property_id": row["PIN"],
                    "sale_date": str(parser.parse((str(row["SMON"]) + "/" + "01/" + str(row["SYEAR"])))),
                    "sale_price": row["SPRICE"],
                    "physical_address": " ".join(str(row["ADDRESS"]).upper().split()),
                    "county": "LEHIGH",
                    "state": "PA",
                    "source_url": row["Web_WEB"],
                }

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
