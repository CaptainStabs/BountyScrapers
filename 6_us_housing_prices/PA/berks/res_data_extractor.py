import csv
from tqdm import tqdm
from dateutil import parser

# PARID,DESC1,,YRBLT
columns = ["property_id","property_type", "book", "page", "sale_price", "sale_date", "physical_address", "year_built", "county", "state", "source_url"]
with open("Res.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("res_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "property_id": row["PARID"],
                    "property_type": " ".join(str(row["DESC1"]).upper().split()),
                    "county": "BERKS",
                    "state": "PA",
                    "source_url": "https://services3.arcgis.com/dGYe1jDYrTw1wwpc/ArcGIS/rest/services/Berks_Assessment_CAMA_Residential_File/FeatureServer/0"
                }
                # ,,,,
                # If address is in separate fields
                street_list = [str(row["ADRNO"]).strip(), str(row["ADRADD"]).strip(), str(row["ADRSTR"]).strip(), str(row["ADRDIR"]).strip(), str(row["ADRSUF"]).strip()]

                # concat the street parts filtering out blank parts
                land_info["physical_address"] = ' '.join(filter(None, street_list)).upper()

                # Delete if no year_built
                try:
                    if int(row["YRBLT"]) != 0 and int(row["YRBLT"]) <= 2022 and int(row["YRBLT"]) >= 1690:
                        land_info["year_built"] = row["YRBLT"]

                except ValueError:
                    pass

                for i in range(4):
                    # ,BOOK,PAGE,PRICE,SALEDT,,SALEYR1,SALEMTH1,SALEPR1,SALEYR2,SALEMTH2,SALEPR2,SALEYR3,SALEMTH3,SALEPR3,
                # date_list = [str(row[f"Sale{x}D"]).strip() for x in range(1,4)]
                    try:
                        if not i: # i = 0
                            book = str(row["BOOK"]).strip()
                            page = str(row["PAGE"]).strip()

                            try:
                                if int(book) != 0 and int(page) != 0:
                                    land_info["book"] = int(book)
                                    land_info["page"] = int(page)

                            except ValueError:
                                pass

                            land_info["sale_price"] = row["PRICE"]
                            try:
                                land_info["sale_date"] = str(parser.parse(row["SALEDT"]))
                            except parser._parser.ParserError:
                                pass

                        else:
                            land_info["sale_date"] = str(parser.parse(str(row[f"SALEMTH{i}"]) + "/01/" + str(row[f"SALEYR{i}"])))
                            land_info["sale_price"] = row[f"SALEPR{i}"]
                    except parser._parser.ParserError:
                        continue

                    try:
                        year = land_info["sale_date"].split("-")[0]

                        if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022 and int(year) >= 1690:
                            writer.writerow(land_info)

                    except KeyError:
                        pass

            except parser._parser.ParserError:
                pass
