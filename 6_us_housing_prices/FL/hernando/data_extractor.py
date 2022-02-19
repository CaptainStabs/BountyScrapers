import csv
from tqdm import tqdm
import datetime

#PARCEL_SORTNUM,,,SITUS_ADDRESS,,SITUS_CITY,SITUS_ZIP5,PCA3_LIVING_UNITS,STRUCTURE_COUNT,,LSALE_DATE,LSALE_ORBOOK,LSALE_ORPAGE,,LSALE_PRICE,COUNTY,
columns = ["property_id", "physical_address", "city", "zip5", "num_units", "sale_date", "book", "page", "sale_price", "county", "state", "source_url"]
with open("1999.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("aextracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                timestamp = int(row["LSALE_DATE"])
                land_info = {
                    "property_id": row["PARCEL_SORTNUM"],
                    "physical_address": " ".join(str(row["SITUS_ADDRESS"]).upper().split()),
                    "city": " ".join(str(row["SITUS_CITY"]).upper().split()),
                    "zip5": row["SITUS_ZIP5"],
                    "sale_date": datetime.datetime.fromtimestamp((timestamp/1000)),
                    "sale_price": row["LSALE_PRICE"],
                    "county": " ".join(str(row["COUNTY"]).upper().split()),
                    "state": "FL",
                    "source_url": "https://www.hernandocountygis-fl.us/arcgis10_3/rest/services/Parcels_Addresses_All/MapServer/5",
                }


                # Delete if no book
                # Update field
                book = str(row["LSALE_ORBOOK"]).strip()
                page = str(row["LSALE_ORPAGE"]).strip()

                try:
                    if int(book) != 0 and int(page) != 0:
                        land_info["book"] = int(book)
                        land_info["page"] = int(page)

                except ValueError:
                    pass


                # Delete if no zip5
                if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                    land_info["zip5"] = ""

                # ,PCA3_LIVING_UNITS,STRUCTURE_COUNT
                if not row["PCA3_LIVING_UNITS"] and row["STRUCTURE_COUNT"]:
                    try:
                        # Delete if no unit count
                        if int(row["STRUCTURE_COUNT"]) != 0:
                            land_info["num_units"] = row["STRUCTURE_COUNT"]
                    except ValueError:
                        pass

                elif row["PCA3_LIVING_UNITS"] and not row["STRUCTURE_COUNT"]:
                    try:
                        # Delete if no unit count
                        if int(row["PCA3_LIVING_UNITS"]) != 0:
                            land_info["num_units"] = row["PCA3_LIVING_UNITS"]
                    except ValueError:
                        pass
                elif row["PCA3_LIVING_UNITS"] and row["STRUCTURE_COUNT"]:
                    try:
                        # Delete if no unit count
                        if int(row["PCA3_LIVING_UNITS"]) != 0:
                            land_info["num_units"] = row["PCA3_LIVING_UNITS"]
                    except ValueError:
                        pass



                year = land_info["sale_date"].year
                if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                    writer.writerow(land_info)

            except ValueError as e:
                pass

            except Exception as e:
                tb.print_exc()
                print(row["DEEDDATE"])
                # print(e)
                pass
