import csv
from tqdm import tqdm
from dateutil import parser

# PIN83,PARID,,BK_PG,SALE_PRICE,DATE_RECOR,PARCEL_ADD,,USE_DESC,YEAR_BUILT,
columns = ["property_id", "book", "page", "sale_price", "sale_date", "physical_address", "property_type", "year_built", "county", "state", "source_url"]

with open("halifax_co_nc_parcels_2021_final_map.csv", "r") as input_csv:
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader):
            land_info = {
                "state": "NC",
                "county": "Halifax",
                "source_url": "https://halifaxnctax.com/geographic-information-systems/"
            }

            if row["DATE_RECOR"]:
                land_info["sale_date"] = parser.parse(row["DATE_RECOR"])

                if int(str(land_info["sale_date"]).split("-")[0]) <= 2022:
                    if row["\u00ef\u00bb\u00bfPIN83"]:
                        land_info["property_id"] = row["\u00ef\u00bb\u00bfPIN83"].strip()

                    else:
                        land_info["PARID"]

                    if row["BK_PG"]:
                        book = row["BK_PG"].split("/")[0].strip()
                        page = row["BK_PG"].split("/")[1].strip()

                        try:
                            if int(book) != 0 and int(page) != 0:
                                land_info["book"] = book
                                land_info["page"] = page

                        except ValueError:
                            pass
                            # print(book, page)

                    land_info["sale_price"] = row["SALE_PRICE"].split(".")[0]

                    land_info["physical_address"] = " ".join(str(row["PARCEL_ADD"]).strip().upper().split())
                    land_info["property_type"] = row["USE_DESC"]

                    if row["YEAR_BUILT"].split(".")[0] != "0":
                        land_info["year_built"] = row["YEAR_BUILT"].split(".")[0]

                    if land_info["physical_address"]:
                        writer.writerow(land_info)

                else:
                    print(land_info["sale_date"])
