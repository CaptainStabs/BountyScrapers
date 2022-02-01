import csv
from tqdm import tqdm
from dateutil import parser

# PID,WebSiteLin,LASTSALEDA,GRANTEE,GRANTOR,SALEP,LANDTYPE,LOCATIONAD,,LOCATIONCI,LOCATIONZI,
columns = ["property_id", "sale_date", "buyer_name", "seller_name", "sale_price", "property_type", "physical_address", "city", "zip5", "county", "state", "source_url"]
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
                    "property_id": str(row["PID"]).strip(),
                    "sale_date": str(parser.parse(str(row["LASTSALEDA"]).strip())),
                    "buyer_name": " ".join(str(row["GRANTEE"]).upper().split()).replace(" ,", ","),
                    "seller_name": " ".join(str(row["GRANTOR"]).upper().split()).replace(" ,", ","),
                    "sale_price": str(row["SALEP"]).split(".")[0],
                    "property_type": " ".join(str(row["LANDTYPE"]).upper().split()),
                    "physical_address": " ".join(str(row["LOCATIONAD"]).upper().split()),
                    "city": str(row["LOCATIONCI"]).upper().replace("_", " "),
                    "zip5": str(row["LOCATIONZI"]).strip(),
                    "county": "MONTEZUMA",
                    "state": "CO",
                    "source_url": row["WebSiteLin"],
                }

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
