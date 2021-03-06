import json
import csv
from tqdm import tqdm
from dateutil import parser
import traceback as tb
# ,SALE_PRC1,SALE_YR1,SALE_MO1,OR_BOOK1,OR_PAGE1,SALE_PRC2,SALE_YR2,SALE_MO2,OR_BOOK2,OR_PAGE2,
# PARCEL_ID,EFF_YR_BLT,NO_BULDNG,PHY_ADDR1,PHY_CITY,PHY_ZIPCD,
columns = ["property_id", "year_built", "num_units", "sale_price", "sale_date", "book", "page", "physical_address", "city", "zip5", "county", "state", "source_url"]
with open("unitedstateszipcodes.csv", "r") as f:
    zips = dict(filter(None, csv.reader(f)))

with open("F:\\___FL\\Parcels.csv", "r") as input_csv:
    # line_count = len([line for line in input_csv.readlines()])
    # input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("C:\\Users\\adria\\github\\BountyScrapers\\6_us_housing_prices\\FL\\fl\\extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=10542442):
            try:
                land_info = {
                    "property_id": row["PARCEL_ID"],
                    "physical_address": " ".join(str(row["PHY_ADDR1"]).upper().split()),
                    "city": " ".join(str(row["PHY_CITY"]).upper().split()),
                    "zip5": row["PHY_ZIPCD"].split(".")[0],
                    "state": "FL",
                    "source_url": "ftp://sdrftp03.dor.state.fl.us/Tax%20Roll%20Data%20Files/2021%20Final%20NAL%20-%20SDF%20DBF%20Files/",
                }

                try:
                    land_info["county"] = zips[land_info["zip5"]].strip().upper()
                except KeyError:
                    # tb.print_exc()
                    pass

                # except:
                #     tb.print_exc()

                # Delete if no year_built
                try:
                    if int(row["EFF_YR_BLT"]) != 0 and int(row["EFF_YR_BLT"]) <= 2022:
                        land_info["year_built"] = int(row["EFF_YR_BLT"])

                except ValueError:
                    pass

                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    # print(land_info["zip5"])
                    land_info["zip5"] = ""

                try:
                    # Delete if no unit count
                    if int(row["NO_BULDNG"]) != 0:
                        land_info["num_units"] = int(row["NO_BULDNG"])
                except ValueError:
                    pass

                for i in range(1,3):
                    # Delete if no book
                    # Update field
                    book = str(row[f"OR_BOOK{i}"]).strip()
                    page = str(row[f"OR_PAGE{i}"]).strip()

                    try:
                        if int(book) != 0 and int(page) != 0:
                            land_info["book"] = int(book)
                            land_info["page"] = int(page)

                    except ValueError:
                        pass
                # date_list = [str(row[f"Sale{x}D"]).strip() for x in range(1,4)]
                    try:
                        land_info["sale_date"] = str(parser.parse(str(row[f"SALE_MO{i}"]).strip() + "/15/" + str(row[f"SALE_YR{i}"]).split(".")[0]))
                        land_info["sale_price"] = row[f"SALE_PRC{i}"].split(".")[0]
                        year = land_info["sale_date"].split("-")[0]

                        if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                            writer.writerow(land_info)

                    except parser._parser.ParserError:
                        tb.print_exc()
                        pass
                    except ValueError:
                        tb.print_exc()
                        pass



            except parser._parser.ParserError:
                pass
