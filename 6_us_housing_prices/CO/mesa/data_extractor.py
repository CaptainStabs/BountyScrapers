import csv
from tqdm import tqdm
import datetime
from pathlib import Path
import sys
# import heartrate; heartrate.trace(browser=True, daemon=True)

p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p))

from _sale_type.sale_type import sale_type

# PARCEL_NUM,,LOCATION,SITUS_CITY,SITUS_ZIP,,POINTER,GRANTEE,GRANTOR,SPRICE,SDATE,SQUAL,PROPTYPE,EFFYRBLT1ST,TOTNOUNITS,
columns = ["property_id", "physical_address", "city", "zip5", "buyer_name", "seller_name", "sale_date", "sale_price", "sale_type", "property_type", "year_built", "num_units", "county", "state", "source_url"]
with open("Parcels.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                if str(row["SDATE"]):
                    timestamp = (int(row["SDATE"])/1000)
                    if timestamp < 0:
                        sec = 0
                        microsec = 0
                        if isinstance(timestamp, int):
                            sec = timestamp
                        else:
                            whole, frac = str(timestamp).split(".")
                            sec = int(whole)
                            microsec = int(frac) * -1
                        dt = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=sec, microseconds=microsec)
                    else:
                        dt = datetime.datetime.fromtimestamp(timestamp)

                    land_info = {
                        "property_id": row["PARCEL_NUM"],
                        "physical_address": " ".join(str(row["LOCATION"]).upper().split()),
                        "city": str(row["SITUS_CITY"]).upper().strip(),
                        "zip5": row["SITUS_ZIP"][:5],
                        "buyer_name": " ".join(str(row["GRANTEE"]).upper().split()),
                        "seller_name": " ".join(str(row["GRANTOR"]).upper().split()),
                        "sale_price": row["SPRICE"],
                        "sale_date": dt,
                        "property_type": " ".join(str(row["PROPTYPE"]).upper().split()),
                        "county": "MESA",
                        "state": "CO",
                        "source_url": row["POINTER"],
                    }

                    try:
                        land_info["sale_type"] = sale_type[row["SQUAL"]]
                    except KeyError:
                        # print(row["SQUAL"])
                        land_info["sale_type"] = row["SQUAL"]

                    # Delete if no year_built
                    try:
                        if int(row["EFFYRBLT1ST"]) != 0 and int(row["EFFYRBLT1ST"]) <= 2022:
                            land_info["year_built"] = row["EFFYRBLT1ST"]

                    except ValueError:
                        pass

                    # Delete if no zip5
                    if land_info["zip5"] == "00000" or land_info["zip5"] == "0" or len(land_info["zip5"]) != 5:
                        land_info["zip5"] = ""

                    try:
                        # Delete if no unit count
                        if int(row["TOTNOUNITS"]) != 0:
                            land_info["num_units"] = row["TOTNOUNITS"]
                    except ValueError:
                        pass

                    year = land_info["sale_date"].year
                    if land_info["physical_address"] and land_info["sale_date"] and land_info["sale_price"] != "" and int(year) <= 2022:
                        writer.writerow(land_info)

            except ValueError:
                import traceback as tb
                tb.print_exc()
                pass

            except OSError:
                print(f"\n`{row['SDATE']}`")
