import csv
from tqdm import tqdm
import traceback as tb
# Procedure Code,Procedure Description,Unit Charge in Dollars
columns = ["cms_certification_num", "payer", "code", "description", "inpatient_outpatient", "price"]
with open("MMC-Clinic-Service-Charges-11012021.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("clinic_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                price_info = {
                    "cms_certification_num": "010005",
                    "payer": "CASH PRICE",
                    "code": "HCPCS " + str(row["Procedure Code"]).upper(),
                    "description": " ".join(str(row["Procedure Description"]).upper().split()),
                    "price": row["Unit Charge in Dollars"]
                }
                if "OUTPT" in price_info["description"]:
                    price_info["inpatient_outpatient"]: "OUTPATIENT"
                elif "INPT" in price_info["description"]:
                    price_info["inpatient_outpatient"]: "INPATIENT"


                if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                    writer.writerow(price_info)
                else:
                    import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                tb.print_exc()
