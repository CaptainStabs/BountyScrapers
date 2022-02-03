import csv
from tqdm import tqdm
from dateutil import parser
import datetime
import usaddress

# APN,Sales_Value,,SITUS,,Year_Built,,Event_Date,
columns = ["property_id", "sale_price", "physical_address", "city", "zip5", "year_built", "sale_date", "county", "state", "source_url"]
with open("year1.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                timestamp = datetime.datetime.fromtimestamp((int(row["Event_Date"])/1000))
                land_info = {
                    "property_id": row["APN"],
                    "sale_price": row["Sales_Value"],
                    "sale_date": timestamp,
                    "county": "BUTTE",
                    "state": "CA",
                    "source_url": "http://gis.buttecounty.net/Public/index.html?viewer=dssearch",
                }

                physical_address = " ".join(str(row["SITUS"]).upper().split())
                if physical_address != "NO ADDRESS AVAILABLE":
                    try:
                        parsed_address = usaddress.tag(physical_address)
                        parse_success = True

                    except usaddress.RepeatedLabelError as e:
                        print(e)
                        parse_success = False
                else:
                    land_info["physical_address"] = "NO ADDRESS AVAILABLE"

                if parse_success:
                    try:
                        # Split the address at the city to get the street
                        street_physical = str(physical_address.split(parsed_address[0]["PlaceName"])[0]).strip(",").strip()
                        street_physical = street_physical.strip(",")
                        land_info["physical_address"] = street_physical.replace('"', '').strip(",")

                        try:
                            land_info["city"] = parsed_address[0]["PlaceName"]
                        except KeyError:
                            raise

                        try:
                            land_info["zip5"] = str(parsed_address[0]["ZipCode"]).replace('"', '').strip()
                        except KeyError:
                            raise
                            # print(physical_address)

                    except KeyError:
                        print("\n" + str(physical_address))
                    # Delete if no year_built
                    try:
                        if int(row["Year_Built"]) >= 1690 and int(row["Year_Built"]) <= 2022:
                            land_info["year_built"] = row["Year_Built"]

                    except ValueError:
                        pass

                    # Delete if no zip5
                    if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                        land_info["zip5"] = ""

                    year = land_info["sale_date"].year

                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                        writer.writerow(land_info)

            except Exception as e:
                raise e
                pass
