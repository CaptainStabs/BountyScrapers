import csv
from tqdm import tqdm
import traceback as tb

columns = ["cms_certification_num", "code", "units", "payer", "description", "price", "code_disambiguator"]
with open("./input_files/converted/western maryland.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("wester_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                price_info = {
                    "cms_certification_num": "210027",
                    "payer": "GROSS CHARGE",
                    "description": " ".join(str(row["Description"]).upper().split()),
                    "price": row["Gross Charge"],
                    "units": row["RxQuantity"],
                    "code_disambiguator": " ".join([row["Type"], row["Category"], row["RxQuantity"]])
                }

                if str(row["CPT/HCPCS"]).strip():
                    price_info["code"] = row["CPT/HCPCS"]
                elif str(row["NDC"]).strip():
                    price_info["code"] = row["NDC"]
                else:
                    price_info["code"] = "NONE"

                if str(price_info["price"]).strip() != "" and float(price_info["price"]) <= 10000000:
                    writer.writerow(price_info)
                # else:
                #     import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                tb.print_exc()
