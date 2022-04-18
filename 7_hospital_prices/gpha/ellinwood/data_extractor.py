import csv
from tqdm import tqdm
import traceback as tb

columns = ["cms_certification_num", "payer", "code", "internal_revenue_code", "description", "price"]
with open("EDH _Charges_12282018.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                price_info = {
                    "cms_certification_num": "171301",
                    "payer": "GROSS CHARGE",
                    "code": "NONE",
                    "internal_revenue_code": row["Charge Number"],
                    "description": " ".join(str(row["Charge Description"]).split()),
                    "price": row["Price"]
                }

                if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                    writer.writerow(price_info)
                else:
                    import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                tb.print_exc()
