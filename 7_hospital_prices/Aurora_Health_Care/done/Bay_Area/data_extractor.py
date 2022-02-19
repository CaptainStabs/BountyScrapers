import csv
from tqdm import tqdm
import traceback as tb
# Facility,Type,Chargecode_DRG_CPT,Description,CPT,
insurances = ["Aetna","Anthem_Blue_Priority","Anthem_Blue_Preferred","Anthem_PPO","Aurora_Caregiver","Cigna","Exchange_-Common_Ground","Health_EOS","Humana_WVN","Humana_HMO","Humana_PPO","Trilogy","UHC_HMO","UHC_PPO","WEA","WPS_Arise","WPS_Statewide","SELF_PAY","MIN","MAX"]
# Type,Chargecode_DRG_CPT,Description,CPT,_1_1_21_Fee,
columns = ["cms_certification_num", "internal_revenue_code", "description", "code", "price", "inpatient_outpatient", "payer"]
with open("./input_files/insurance.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("./output_files/insurances_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                if str(row["CPT"]).strip() and str(row["CPT"]) != "NA":
                    price_info = {
                        "cms_certification_num": "520113",
                        "code": str(row["CPT"]).upper(),
                        "internal_revenue_code": row["Chargecode_DRG_CPT"],
                        "description": " ".join(str(row["Description"]).upper().split()),
                    }

                    inpatient_outpatient = str(row["Type"]).upper()
                    if "IP" in inpatient_outpatient:
                        price_info["inpatient_outpatient"] = "INPATIENT"
                    elif "OP" in inpatient_outpatient:
                        price_info["inpatient_outpatient"] = "OUTPATIENT"

                    for payer in insurances:
                        price_info["price"] = str(row[payer]).replace(",", "")
                        price_info["payer"] = str(payer).upper().replace("_", " ").replace("-", "")

                        if price_info["payer"] == "SELF PAY":
                            price_info["payer"] = "CASH PRICE"

                        if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                            writer.writerow(price_info)
                        else:
                            import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                tb.print_exc()
