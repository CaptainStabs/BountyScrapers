import csv
from tqdm import tqdm
import traceback as tb
# import heartrate; heartrate.trace(browser=True, daemon=True)

# Current Procedural Terminology (CPT) Code,Procedure Name, Hospital Inpatient Fee in Dollars, Hospital Outpatient Fee in Dollars, "Marshall Medical Procedure Code"
columns = ["cms_certification_num", "payer", "code", "internal_revenue_code", "description", "price", "inpatient_outpatient"]
with open("HOSPITAL-SERVICES-11012021.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("hospital_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                if str(" ".join(str(row["Current Procedural Terminology (CPT) Code"]).upper().split())):
                    price_info = {
                        "cms_certification_num": "010005",
                        "payer": "CASH PRICE",
                        "code": "CPT " + " ".join(str(row["Current Procedural Terminology (CPT) Code"]).upper().split()),
                        "internal_revenue_code": row["Marshall Medical Procedure Code"],
                        "description": " ".join(str(row["Procedure Name"]).upper().split()),
                    }

                    inpatient = row["Hospital Inpatient Fee in Dollars"]
                    outpatient = row["Hospital Outpatient Fee in Dollars"]

                    if not str(inpatient):
                        price_info["price"] = outpatient.replace(",", "")
                    else:
                        price_info["price"] = inpatient.replace(",", "")

                    if str(inpatient) and str(outpatient):
                        price_info["inpatient_outpatient"] = "BOTH"
                    elif str(outpatient) and not str(inpatient):
                        price_info["inpatient_outpatient"] = "OUTPATIENT"
                    elif str(inpatient) and not str(outpatient):
                        price_info["inpatient_outpatient"] = "INPATIENT"

                    if price_info["price"]:
                        if float(price_info["price"]) <= 10000000:
                            writer.writerow(price_info)
                        else:
                            import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                tb.print_exc()
