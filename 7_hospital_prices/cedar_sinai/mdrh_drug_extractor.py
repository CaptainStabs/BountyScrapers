import csv
from tqdm import tqdm
import traceback as tb
import os

columns = ["cms_certification_num", "internal_revenue_code", "description", "code", "price", "inpatient_outpatient", "payer", "units"]
in_directory = "./input_files/"
with open(f"drugs_extracted_data.csv", "a", newline="", encoding="utf-8") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    writer.writeheader()

    with open("mdrh_drugs.csv", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                # internal_revenue_code,description,code,OP_price,IP_price
                price_info = {
                    "cms_certification_num": "050740",
                    "internal_revenue_code": row["internal_revenue_code"],
                    "description": row["description"].strip(),
                    "units": row["units"].strip()
                }

                if str(row["cpt"]):
                    price_info["code"] = row["cpt"]

                elif not str(row["cpt"]) and str(row["ndc"]):
                    price_info["code"] = row["ndc"]
                else:
                    price_info["code"] = "NONE"

                if str(row["OP_price"]).strip():
                    price_info["inpatient_outpatient"] = "OUTPATIENT"

                    price_info["price"] = str(row["OP_price"]).replace("$", "").replace(",", "").strip()
                    price_info["payer"] = "CASH PRICE"

                    if str(price_info["price"]) and str(price_info["price"]) != "None":
                        if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                            writer.writerow(price_info)
                                # a = "s"
                        else:
                            import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                print(row)
                tb.print_exc()
