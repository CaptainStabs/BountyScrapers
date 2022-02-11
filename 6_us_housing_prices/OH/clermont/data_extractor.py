import csv
from tqdm import tqdm
from dateutil import parser
 # ,,,,
# PIN,,PRICE,SALESDATE,,YRBLT,STYLE,HYPERLINK,
columns = ["property_id", "physical_address", "sale_price", "sale_date", "year_built", "property_type", "sale_type", "county", "state", "source_url"]
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
                    "property_id": str(row["PIN"]).strip(),
                    "sale_price": row["PRICE"],
                    "sale_date": str(parser.parse(row["SALESDATE"])),
                    "property_type": " ".join(str(row["STYLE"]).upper().split()),
                    "sale_type": str(row["SALETYPE"]).upper().strip(),
                    "county": "CLERMONT",
                    "state": "OH",
                    "source_url": row["HYPERLINK"],
                }

                # If address is in separate fields
                street_list = [str(row["ADRNO"]).strip(), str(row["ADRADD"]).strip(), str(row["ADRDIR"]).strip(), str(row["ADRSTR"]).strip(), str(row["ADRSUF"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no year_built
                try:
                    if int(row["YRBLT"]) != 0 and int(row["YRBLT"]) <= 2022:
                        land_info["year_built"] = row["YRBLT"]

                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
