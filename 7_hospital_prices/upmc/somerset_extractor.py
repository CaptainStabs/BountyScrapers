import csv
from tqdm import tqdm
import traceback as tb
# "Type","Category","Description","NDC","CPT/HCPCS","RxQuantity","Gross Charge",
columns = ["cms_certification_num", "payer", "internal_revenue_code", "description", "price", "code_disambiguator"]
with open("./input_files/converted/UPMC-Somerset-Chargemaster.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("somerset_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                price_info = {
                    "cms_certification_num": "390039",
                    "payer": "GROSS CHARGE",
                    "internal_revenue_code": row["Chareg Code"],
                    "description": " ".join(str(row["Charge Description"]).upper().split()),
                    "price": row["Charge Amount"],
                    "code_disambiguator": " ".join(str(row["Charge Description"]).upper().split())
                }

                if str(price_info["price"]).strip() != "" and float(price_info["price"]) <= 10000000:
                    writer.writerow(price_info)
                # else:
                #     import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                tb.print_exc()
