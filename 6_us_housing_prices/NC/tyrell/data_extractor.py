import csv
from tqdm import tqdm
from dateutil import parser

#pin,card,cardcount,situsstree,situsnum,yearbuilt,,deedbook,deedpage,,saledate,saleamount,f911housen,situsroad,f911street
columns = ["property_id", "physical_address", "year_built", "book", "page", "sale_date", "sale_price", "county", "state", "source_url"]
with open("TaxParcel.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["pin"],
                    "sale_date": str(parser.parse(row["saledate"])),
                    "sale_price": row["saleamount"],
                    "county": "Tyrrell",
                    "state": "NC",
                    "source_url": "https://agdonline.maps.arcgis.com/apps/webappviewer/index.html?id=1c2493cb8eb1484eb1ecc571131f5ee6"

                }

                # If address is in separate fields
                street_list = []
                try:
                    if str(row["f911housn"]) != "NULL" and row["f911housn"] != "":
                        street_list.append(str(row["f911housn"]).strip())
                except KeyError:
                    pass
                    
                try:
                    if str(row["situsnum"]) != "NULL" and row["situsnum"] != "":
                        street_list.append(str(row["situsnum"]).strip())
                except KeyError:
                    pass


                if str(row["situsstree"]) != "NULL":
                    street_list.append(str(row["situsstree"]).strip())

                if str(row["situsroad"]) != "NULL":
                    street_list.append(str(row["situsroad"]).strip())

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no book
                # Update field
                book = str(row["deedbook"]).strip()
                page = str(row["deedpage"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass

                # Delete if no year_built
                try:
                    if int(row["yearbuilt"]) != 0 and int(row["yearbuilt"]) <= 2022:
                        land_info["year_built"] = row["yearbuilt"]

                except ValueError:
                    pass

                year = land_info["sale_date"].split("-")[0]

                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except parser._parser.ParserError:
                pass
