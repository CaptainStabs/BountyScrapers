import csv
from tqdm import tqdm
from dateutil import parser

# PARID,ADRNO,ADRADD,ADRDIR,ADRSTR,ADRSUF,ADRSUF2,UNITDESC,UNITNO,LOC2,CITYNAME,ZIP1,SALEDT,BOOK,PAGE,PRICE
# ,,,,,,,,
columns = ["property_id", "physical_address", "city", "zip5", "sale_date", "book", "page", "sale_price", "county", "state", "source_url"]
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data_test.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PARID"].strip(),
                    "city": " ".join(str(row["CITYNAME"]).upper().split()),
                    "zip5": row["ZIP1"].strip(),
                    "sale_date": str(parser.parse(row["SALEDT"].strip())),
                    "sale_price": row["PRICE"].split(".")[0],
                    "county": "VOLUSIA",
                    "state": "FL",
                    "source_url": "https://vcpa.vcgov.org/download/database#gsc.tab=0",
                }

                # If address is in separate fields
                street_list = [str(row["ADRNO"]).strip(), str(row["ADRADD"]).strip(), str(row["ADRDIR"]).strip(), str(row["ADRSTR"]).strip(), str(row["ADRSUF"]).strip(), str(row["ADRSUF2"]).strip(), str(row["UNITDESC"]).strip(), str(row["UNITNO"]).strip(), str(row["LOC2"]).strip()]

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

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""


                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
