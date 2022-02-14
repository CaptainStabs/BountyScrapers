import csv
from tqdm import tqdm
from dateutil import parser

#PARID,DESC1,,BOOK,PAGE,PRICE,SALEDT,,LIVUNIT
columns = ["property_id", "property_type", "physical_address", "book", "page", "sale_price", "sale_date", "num_units", "county", "state", "source_url"]
with open("MasterParcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data_master.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PARID"],
                    "property_type": " ".join(str(row["DESC1"]).upper().split()),
                    "sale_price": row["PRICE"],
                    "sale_date": str(parser.parse(row["SALEDT"])),
                    "county": "BERKS",
                    "state": "PA",
                    "source_url": "https://services3.arcgis.com/dGYe1jDYrTw1wwpc/ArcGIS/rest/services/Berks_Assessment_CAMA_Master_File/FeatureServer",
                }

                # ,,,,
                # If address is in separate fields
                street_list = [str(row["ADRNO"]).strip(), str(row["ADRADD"]).strip(), str(row["ADRDIR"]).strip(), str(row["ADRSTR"]).strip(), str(row["ADRSUF"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no book
                # Update field
                book = str(row["BOOK"]).strip()
                page = str(row["PAGE"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                try:
                    # Delete if no unit count
                    if int(row["LIVUNIT"]) != 0:
                        land_info["num_units"] = row["LIVUNIT"]
                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022 and int(year) >= 1690:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
