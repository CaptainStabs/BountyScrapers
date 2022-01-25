import csv
from tqdm import tqdm
from dateutil import parser
import os

# Parid,Saledt,Price,Book,Page,Adrno,Adrdir,Adrstr,Adrsuf,,Unitdesc,

columns = ["property_id", "sale_date", "sale_price", "book", "page", "physical_address", "property_type", "county", "state", "source_url"]
directory = ".\\input_files\\"

with open("extracted_data.csv", "a", newline="") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    writer.writeheader()

for file in os.listdir(directory):
    with open(directory + file, "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)
        reader = csv.DictReader(input_csv)

        with open("extracted_data.csv", "a", newline="") as output_csv:
            writer = csv.DictWriter(output_csv, fieldnames=columns)

            for row in tqdm(reader, total=line_count):
                try:
                    land_info = {
                        "property_id": row["Parid"],
                        "sale_date": str(parser.parse(row["Saledt"])),
                        "sale_price": str(row["Price"]).strip(".")[0],
                        "property_type": " ".join(str(row["Unitdesc"]).strip().split()),
                        "county": "Lee",
                        "state": "NC",
                        "source_url": "https://leecountync.gov/Departments/GISStrategicServices/SalesData"
                    }

                    # If address is in separate fields
                    try:
                        street_list = [str(row["Adrno"]).strip(), str(row["Adrdir"]).strip(), str(row["Adrstr"]).strip(), str(row["Adrsuf"]).strip()]

                    except KeyError:
                        street_list = [str(row["Adrno"]).strip(), str(row["Adrstr"]).strip(), str(row["Adrsuf"]).strip()]

                    # concat the street parts filtering out blank parts
                    land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                    # Delete if no book
                    # Update field
                    book = row["Book"]
                    page = row["Page"]

                    try:
                        if int(book) != 0 and int(page) != 0:
                            land_info["book"] = book
                            land_info["page"] = page

                    except ValueError:
                        pass


                    year = land_info["sale_date"].split("-")[0]

                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                        writer.writerow(land_info)

                except parser._parser.ParserError:
                    pass

                except IndexError:
                    pass
                    # print(row["Price"])
