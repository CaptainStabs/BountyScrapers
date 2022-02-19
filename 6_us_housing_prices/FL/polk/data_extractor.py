import csv
from tqdm import tqdm
from dateutil import parser

# "PARCEL_ID","SALEDT","PRICE","BOOK","PAGE","GRANTOR","GRANTEE",,"ZIP","CITY","DORDESC1","YR_IMPROVED"
columns = ["property_id", "sale_date", "sale_price", "book", "page", "seller_name", "buyer_name", "physical_address", "zip5", "city", "property_type", "year_built", "county", "state", "source_url"]
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
                    "property_id": row["PARCEL_ID"],
                    "sale_date": str(parser.parse(row["SALEDT"])),
                    "sale_price": row["PRICE"],
                    "seller_name": " ".join(str(row["GRANTOR"]).upper().split()),
                    "buyer_name": " ".join(str(row["GRANTEE"]).upper().split()),
                    "zip5": row["ZIP"],
                    "city": " ".join(str(row["CITY"]).upper().split()),
                    "property_type": " ".join(str(row["DORDESC1"]).upper().split()),
                    "county": "POLK",
                    "state": "FL",
                    "source_url": "https://www.polkpa.org/FTPPage/ftpdefault.aspx?url=%5CAppraisalData",
                }

                # If address is in separate fields
                # "STR_NUM","STR_NUM_SFX","STR_PFX","STR","STR_SFX","STR_SFX_DIR","STR_UNIT"
                street_list = [str(row["STR_NUM"]).strip(), str(row["STR_NUM_SFX"]).strip(), str(row["STR_PFX"]).strip(), str(row["STR"]).strip(), str(row["STR_SFX"]).strip(), str(row["STR_SFX_DIR"]).strip(), str(row["STR_UNIT"]).strip()]

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

                # Delete if no year_built
                try:
                    if int(row["YR_IMPROVED"]) > 1690 and int(row["YR_IMPROVED"]) <= 2022:
                        land_info["year_built"] = row["YR_IMPROVED"]

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
