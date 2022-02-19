import csv
from tqdm import tqdm
import traceback as tb

# Chargecode,Description,,CPT,1/1/22 Fee
columns = ["cms_certification_num", "payer", "code", "internal_revenue_code", "description", "price"]
with open("./input_files/aurora-baycare-standard-charges.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("cashprice_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                if str(row["CPT"]):
                    price_info = {
                        "cms_certification_num": "520193",
                        "payer": "CASH PRICE",
                        "code": "CPT " + str(row["CPT"]).upper(),
                        "internal_revenue_code": row["Chargecode"],
                        "description": " ".join(str(row["Description"]).upper().split()),
                        "price": row["1/1/22 Fee"].replace(",", "")
                    }

                    if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                        writer.writerow(price_info)
                    else:
                        import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                tb.print_exc()
