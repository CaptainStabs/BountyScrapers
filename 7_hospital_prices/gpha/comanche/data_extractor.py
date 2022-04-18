import csv
from tqdm import tqdm
import traceback as tb

columns = ["cms_certification_num", "payer", "code", "internal_revenue_code", "description", "price"]
with open("comanche_combined.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                # "ITEM","DESCRIPTION","CPT","PRICE"
                price_info = {
                    "cms_certification_num": "171312",
                    "payer": "GROSS CHARGE",
                    "code": str(row["CPT"]).strip(),
                    "internal_revenue_code": row["ITEM"],
                    "description": " ".join(str(row["DESCRIPTION"]).split()),
                    "price": row["PRICE"]
                }

                if not str(row["CPT"]).strip():
                    price_info["code"] = "NONE"

                if str(price_info["price"]).strip() and str(price_info["price"]).strip() != "":
                    if float(price_info["price"]) <= 10000000:
                        writer.writerow(price_info)
                    else:
                        import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                tb.print_exc()
