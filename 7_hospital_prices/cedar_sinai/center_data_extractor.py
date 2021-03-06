import csv
from tqdm import tqdm
import traceback as tb
import os

columns = ["cms_certification_num", "internal_revenue_code", "description", "code", "price", "inpatient_outpatient", "payer"]
in_directory = "./input_files/"
with open(f"extracted_data.csv", "a", newline="", encoding="utf-8") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    writer.writeheader()

    with open("MDRH.csv", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)
        header = input_csv.readline().split(",")
        insurance = header[(header.index("GROSS CHARGE")):]
        insurances = [x.replace("\n", "") for x in insurance]
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                if str(row["CPT_CODE"]).strip() and str(row["CPT_CODE"]) != "NA":
                    price_info = {
                        "cms_certification_num": "050625",
                        "internal_revenue_code": row["CHARGE_CODE"],
                        "code": str(row["CPT_CODE"]).strip(),
                        "description": str(row["CHARGE_DESC"]),
                    }
                elif str(row["NDC_CODE"]) and not str(row["CPT_CODE"]):
                    price_info = {
                        "cms_certification_num": "050625",
                        "internal_revenue_code": row["CHARGE_CODE"],
                        "code": row["NDC_CODE"].strip(),
                        "description": row["CHARGE_DESC"],
                    }
                else:
                    continue

                if not str(row["CHARGE_DESC"]) and row["MEDICATION_NAME"]:
                    price_info["description"] = str(row["MEDICATION_NAME"]).strip()

                if not str(row["CHARGE_CODE"]):
                    price_info["internal_revenue_code"] = "NONE"

                if not str(row["NDC_CODE"]) and not str(row["CPT_CODE"]):
                    price_info["code"] = "NONE"

                inpatient_outpatient = str(row["Inpatient/Outpatient"]).upper()
                if " IP" in inpatient_outpatient:
                    price_info["inpatient_outpatient"] = "INPATIENT"
                elif " OP" in inpatient_outpatient:
                    price_info["inpatient_outpatient"] = "OUTPATIENT"

                # Gross Charge,Discounted Cash Price,Aetna Commercial Out of Network,Aetna HMO/PPO,Alignment Medicare Adv_ HMO / PPO,Anthem Commercial Out of Network,Anthem HMO/PPO,Anthem Medi-Cal,Anthem Medicare Adv_ HMO / PPO,Blue Shield Commercial Out of Network,Blue Shield HMO / PPO,Blue Shield Individual,Blue Shield Medicare Adv_ HMO / PPO,Cigna Commercial Out of Network,Cigna HMO/PPO,Health Net Commercial Out of Network,Health Net HMO / PPO,Health Net Medi-Cal / California Health & Wellness,Health Net Medicare Adv_ HMO / PPO,HealthSmart PPO,Humana Medicare Adv_ HMO,Multiplan PPO,Stanford Advantage Medicare Adv_ HMO,Sutter | Aetna Fully Insured,Sutter | Aetna Self Insured,Sutter Health Plus HMO,United Commercial Out of Network,United HMO / POS,United Medicare Adv_ HMO,United PPO,United Signature Value Alliance,Minimum Negotiated Price,Maximum Negotiated Price
                for payer in insurances:
                    if "Discounted" not in payer:
                        if str(row[payer]).strip():
                            price_info["price"] = str(row[payer]).replace(",", "").replace("$", "").strip()
                            if "_EFF_" in payer:
                                payer = payer.split("_EFF_")[0].strip()
                            if payer == "MINIMUM NEGOTIATED PRICE":
                                payer = "MIN"

                            if payer == "MAXIMUM NEGOTIATED PRICE":
                                payer = "MAX"
                            price_info["payer"] = " ".join(str(payer).upper().replace("_", " ").replace("-", "").replace(" / ", "/").strip().split())

                            if price_info["price"] != "No standard uninsured rate":
                                if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                                    writer.writerow(price_info)
                                    # a = "s"
                                else:
                                    import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                print(row)
                tb.print_exc()
