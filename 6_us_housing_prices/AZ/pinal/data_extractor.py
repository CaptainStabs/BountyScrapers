import csv
from tqdm import tqdm
from dateutil import parser
import usaddress

# ,,SITEADDRESS,RESYRBLT,RESSTRTYP,GlobalID,SALEDATE,SALEPRICE,
columns = ["physical_address", "city", "zip5", "year_built", "property_id", "property_type", "sale_date", "sale_price", "county", "state", "source_url"]
with open("Parcels.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                land_info = {
                    "sale_date": str(parser.parse(row["SALEDATE"])),
                    "sale_price": row["SALEPRICE"],
                    "property_type": " ".join(str(row["RESSTRTYP"]).upper().split()),
                    "property_id": row["GlobalID"],
                    "county": "PINAL",
                    "state": "AZ",
                    "source_url": "https://pinal.maps.arcgis.com/apps/webappviewer/index.html",
                }

                physical_address = " ".join(str(row["SITEADDRESS"]).upper().split())
                try:
                    parsed_address = usaddress.tag(physical_address)
                    parse_success = True

                except usaddress.RepeatedLabelError as e:
                    print(e)
                    parse_success = False

                if parse_success:
                    try:
                        street_physical = str(physical_address.split(parsed_address[0]["PlaceName"])[0]).strip(",").strip()
                        street_physical = street_physical.strip(",")
                        land_info["physical_address"] = street_physical.replace('"', '').strip(",")

                        try:
                            land_info["city"] = parsed_address[0]["PlaceName"]
                        except KeyError:
                            raise

                        try:
                            land_info["zip5"] = str(parsed_address[0]["ZipCode"]).replace('"', '').strip()
                            # Delete if no zip5
                            if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                                land_info["zip5"] = ""
                        except KeyError:
                            raise
                    except KeyError:
                        pass
                        # print("\n" + str(physical_address))

                    # Delete if no year_built
                    try:
                        if int(row["RESYRBLT"]) >= 1690 and int(row["RESYRBLT"]) <= 2022:
                            land_info["year_built"] = row["RESYRBLT"]

                    except ValueError:
                        pass


                    try:
                        year = land_info["sale_date"].split("-")[0]
                        month = land_info["sale_date"].split("-")[1]
                        if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) < 2022:
                            writer.writerow(land_info)
                        elif int(year) == 2022 and int(month) <= 2:
                            writer.writerow(land_info)
                    except KeyError:
                        pass

            except parser._parser.ParserError:
                pass
