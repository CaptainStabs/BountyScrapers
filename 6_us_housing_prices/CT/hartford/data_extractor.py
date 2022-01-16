import csv
from dateutil import parser
from tqdm import tqdm

columns = ["state", "county", "city", "sale_date", "physical_address", "sale_price", "property_type"]

with open("Real_Estate_sales_2001-2019_GL.csv", "r") as input_csv:
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)

        for row in tqdm(reader):
            try:
                land_info = {
                    "state": "CT",
                    "county": "HARTFORD",
                    "city": row["Town"].upper(),
                    "sale_date": parser.parse(row["Date Recorded"]),
                    "physical_address": " ".join(str(row["Address"]).upper().strip().split()),
                    "sale_price": row["Sale Amount"].split(".")[0],
                    "property_type": row["Property Type"].upper(),
                }

                writer.writerow(land_info)
            except Exception as e:
                print(e)
