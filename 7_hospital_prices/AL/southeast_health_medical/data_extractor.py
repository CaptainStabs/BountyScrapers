import csv
from tqdm import tqdm
import traceback as tb
import heartrate; heartrate.trace(browser=True, daemon=True)

columns = ["cms_certification_num", "payer", "code", "internal_revenue_code", "description", "price", "inpatient_outpatient"]
with open("Southeast-Health-Standard-Charges-2022.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                price_info = {
                    "cms_certification_num": "010001",
                    "payer": " ".join(str(row["Payer"]).upper().strip().split()),
                    "code": str(row["Code"]).upper(),
                    "internal_revenue_code": row["´╗┐Procedure"],
                    "description": " ".join(str(row["Procedure Description"]).upper().split()),
                    "price": row["IP Price"]
                }

                inpatient_outpatient = str(row["OP XR Detail"]).upper()
                if "INPATIENT" in inpatient_outpatient and "OUTPATIENT" in inpatient_outpatient:
                    price_info["inpatient_outpatient"] = "BOTH"
                elif "OUTPATIENT" in inpatient_outpatient and "INPATIENT" not in inpatient_outpatient:
                    price_info["inpatient_outpatient"] = "OUTPATIENT"
                elif "INPATIENT" in inpatient_outpatient and "OUTPATIENT" not in inpatient_outpatient:
                    price_info["inpatient_outpatient"] = "INPATIENT"
                else:
                    price_info["inpatient_outpatient"] = "UNSPECIFIED"

                # fails = {
                #     "code": 0,
                #     "payer": 0,
                #     "internal_revenue_code": 0,
                #     "price": 0
                # }
                # if not str(price_info["code"]):
                #     fails["code"] += 1
                # if not str(price_info["payer"]):
                #     fails["payer"] += 1
                # if not str(price_info["internal_revenue_code"]):
                #     fails["internal_revenue_code"] += 1
                #
                # if float(price_info["price"]) >= 10000000:
                #     fails["price"] += 1

                if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                    writer.writerow(price_info)
                else:
                    import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                tb.print_exc()

# import json; print(json.dumps(fails, indent=2))
