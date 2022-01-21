import csv
from dateutil import parser
from tqdm import tqdm

# PIN15,DBOOK,DPAGE,DDATE,SALE_PRICE,,SITE_HOUSE,SITE_ST,SITE_DIR,SITE_STTYP,SITE_APTNO,SITE_CITY,Towns_Desc,Use_desc
columns = ["property_id", "book", "page", "sale_date", "sale_price", "physical_address", "city", "property_type", "state", "county", "source_url"]

with open("Tax_Parcel_Data.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PIN15"].strip(),
                    "city": " ".join(str(row["Towns_Desc"]).strip().split()),
                    "state": "NC",
                    "county": "Carteret",
                    "property_type": row["Use_desc"],
                    "source_url": "https://gisdata-cc-gis.opendata.arcgis.com/datasets/CC-GIS::tax-parcel-data/about",
                    "sale_price": row["SALE_PRICE"],
                    "sale_date": str(parser.parse(row["DDATE"])),
                }

                 # Add street parts to list
                street_list = [str(row["SITE_HOUSE"]).strip(), str(row["SITE_ST"]).strip(), str(row["SITE_DIR"]).strip(), str(row["SITE_STTYP"]).strip(), str(row["SITE_APTNO"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                book = row["DBOOK"]
                page = row["DPAGE"]

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = book
                        land_info["page"] = page

                except ValueError:
                    continue

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                continue
