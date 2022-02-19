import csv
import mysql.connector
from tqdm import tqdm

columns = ["property_id", "sale_date", "sale_price", "book", "page", "physical_address", "sale_type", "city", "state", "zip5"]
with open("Sales_Data.csv", "r") as input_csv:
    line_count = 0
    # Count lines in file
    for line in input_csv.readlines():
        line_count += 1

    # Seek back to 0 to allow csv to read full file
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        with mysql.connector.connect(host="localhost", port="3306", user="root", password="") as connection:
            cursor = connection.cursor()

            for row in tqdm(reader, total=line_count):
                land_info = {
                    "property_id": row["PARID"],
                    "sale_date": row["SALEDT"],
                    "sale_price": row["PRICE"],
                    "book": row["BOOK"],
                    "page": row["PAGE"],
                    "sale_type": " ".join(str(row["SALEVAL_DESC"]).upper().split())
                }

                cursor.execute(f"select ADDRESS1, CITY, STATE, ZIP from db.property_address where PARID = '{land_info['property_id']}';")

                results = cursor.fetchone()
                if results:
                    land_info["physical_address"] = " ".join(str(results[0]).upper().strip().split())

                    land_info["city"] = str(results[1]).upper()
                    land_info["state"] = str(results[2]).upper()

                    if "-" in results[3]:
                        land_info["zip5"] = results[3].split("-")[0]
                    else:
                        land_info["zip5"] = results[3]


                    if land_info["physical_address"] and land_info["sale_date"]:
                        writer.writerow(land_info)
