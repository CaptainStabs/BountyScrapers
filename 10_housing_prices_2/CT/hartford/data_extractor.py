import csv
from dateutil import parser
from tqdm import tqdm
import functools

columns = ["state", "county", "city", "sale_datetime", "property_street_address", "sale_price", "property_type", "source_url", "property_lat", "property_lon", "appraisal_total"]

@functools.lru_cache(maxsize=None)
def date_parse(date):
    return parser.parse(date)

with open("Real_Estate_sales_2001-2019_GL.csv", "r") as input_csv:
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader):
            try:
                land_info = {
                    "state": "CT",
                    "county": "HARTFORD",
                    "city": row["Town"].upper(),
                    "sale_datetime": date_parse(row["Date Recorded"]),
                    "property_street_address": " ".join(str(row["Address"]).upper().strip().split()),
                    "sale_price": row["Sale Amount"].split(".")[0],
                    "property_type": row["Property Type"].upper(),
                    "source_url": "https://data.ct.gov/Housing-and-Development/Real-Estate-Sales-2001-2019-GL/5mzw-sjtu",
                    "appraisal_total": row["Assessed Value"]
                }

                if row["Location"]:
                    coords = row["Location"].replace("POINT (", "").strip(")")
                    coords = coords.split()
                    land_info["property_lat"], land_info["property_lon"] = coords[0], coords[1]


                writer.writerow(land_info)
            except Exception as e:
                print(e)
