import csv
from tqdm import tqdm
import traceback as tb
import os

# CPT,Description,Charges,Discounted Cash Price,Min Negotiated,Max Negotiated,Medicare,Uhc,Caresource,Medicaid,Wellcare,Humana,Amerigroup,Umr,Aetna,Tricare,Veterans admin,Peach state,Blue cross
columns = ["cms_certification_num", "internal_revenue_code", "description", "code", "price", "payer"]
with open(f"drugs.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    header = input_csv.readline().split(",")
    insurance = header[(header.index("Charges")):]
    insurances = [x.replace("\n", "") for x in insurance]
    input_csv.seek(0)

    reader = csv.DictReader(input_csv)

    with open(f"drug_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                if str(row["DRG"]).strip() and str(row["DRG"]) != "NA":
                    price_info = {
                        "cms_certification_num": "110071",
                        "code": str(row["DRG"]).strip(),
                        "internal_revenue_code": "NONE",
                        "description": str(row["Description"]).strip(),
                    }

                    for payer in insurances:
                        price_info["price"] = str(row[payer]).replace(",", "")

                        if payer == "Discounted Cash Price":
                            payer = "CASH PRICE"

                        elif payer == "Charges":
                            payer = "GROSS CHARGE"
                        elif payer == "Min Negotiated":
                            payer = "MIN"
                        elif payer == "Max Negotiated":
                            payer = "MAX"

                        price_info["payer"] = str(payer).upper().replace("_", " ").replace("-", "")

                        if price_info["payer"] == "SELF PAY":
                            price_info["payer"] = "CASH PRICE"

                        if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                            writer.writerow(price_info)
                        else:
                            import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                tb.print_exc()
