import csv
from tqdm import tqdm
from dateutil import parser

#ParcelID,,DeedBook,DeedPage,SalePrice,DeedDate,GrantorName,GranteeName,IsQualified,
columns = ["property_id", "book", "page", "sale_price", "sale_date", "seller_name", "buyer_name", "county", "state", "source_url"]
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
                    "property_id": row["ParcelID"],
                    "sale_price": row["SalePrice"],
                    "sale_date": str(parser.parse(row["DeedDate"])),
                    "seller_name": " ".join(str(row["GrantorName"]).split()),
                    "buyer_name": " ".join(str(row["GranteeName"]).split()),
                    "county": "Swain",
                    "state": "NC",
                    "source_url": "http://www.swaincountync.gov/page_files/maps/shapeFiles/"

                }

                # If address is in separate fields
                street_list = [str(row["Street#"]).strip(), str(row["Direction"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no book
                # Update field
                book = str(row["DWBook"]).strip()
                page = str(row["DWPage"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                # Delete if no year_built
                try:
                    if int(row["YEARBLT"]) != 0 and int(row["YEARBLT"]) <= 2022:
                        land_info["year_built"] = row["YEARBLT"]

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                try:
                    # Delete if no unit count
                    if int(row["TOTAL_UNITS"]) != 0:
                        land_info["num_units"] = row["TOTAL_UNITS"]
                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
