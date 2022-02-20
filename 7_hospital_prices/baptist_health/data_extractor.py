import csv
from tqdm import tqdm
import traceback as tb
import os
# import heartrate; heartrate.trace(browser=True, daemon=True)

# Facility,Type,Chargecode_DRG_CPT,Description,CPT,
# insurances = ["Aetna_W","Aetna_PPO","Anthem_Blue_Priority","Anthem_Blue_Preferred","Anthem_PPO","Aurora_Caregiver","Cigna_GPPO","Cigna_PPO","Exchange_-Common_Ground","Exchange_-Molina","Health_EOS_Plus","Health_EOS_PPO","HPS","Humana_WVN","Humana_HPN_HMO","Humana_PPO","Trilogy","UHC_HMO","UHC_PPO","WEA_State_and_Trust","WEA_Broad","WPS_Arise","WPS_Statewide","SELF_PAY","MIN","MAX"]
cms_num = {
    "CORBIN": "180080",
    "FLOYD": "150044",
    "HARDIN": "180012",
    "LAGRANGE": "180138",
    "LEXINGTON": "180103",
    "LOUISVILLE": "180130",
    "MADISONVILLE": "180093",
    "PADUCAH": "180104",
    "RICHMOND": "180049"
}

# Type,Chargecode_DRG_CPT,Description,CPT,_1_1_21_Fee,
columns = ["cms_certification_num", "internal_revenue_code", "description", "code", "price", "inpatient_outpatient", "payer"]
in_directory = "./data/"
with open(f"extracted_data.csv", "a", newline="") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    writer.writeheader()

    for file in os.listdir(in_directory):
        if file.endswith(".csv"):
            with open(f"{in_directory}{file}", "r") as input_csv:
                line_count = len([line for line in input_csv.readlines()])
                input_csv.seek(0)
                header = input_csv.readline().split(",")
                insurance = header[(header.index("Gross Charge")):]
                insurances = [x.replace("\n", "") for x in insurance]
                input_csv.seek(0)

                reader = csv.DictReader(input_csv)


                for row in tqdm(reader, total=line_count):
                    try:
                        if str(row["CPT HCPCS Code"]).strip() and str(row["CPT HCPCS Code"]) != "NA":
                            price_info = {
                                "cms_certification_num": cms_num[(file.replace(".csv", "").upper())],
                                "internal_revenue_code": row["Procedure Code"],
                                "code": str(row["CPT HCPCS Code"]).upper(),
                                "description": " ".join(str(row["Procedure Description"]).upper().split()),
                            }

                            inpatient_outpatient = str(row["Price Tier"]).upper()
                            if "INPATIENT" in inpatient_outpatient:
                                price_info["inpatient_outpatient"] = "INPATIENT"
                            elif "OUTPATIENT" in inpatient_outpatient:
                                price_info["inpatient_outpatient"] = "OUTPATIENT"

                            for payer in insurances:
                                if "Discounted" not in payer:
                                    price_info["price"] = str(row[payer]).replace(",", "")
                                    if "_EFF_" in payer:
                                        payer = payer.split("_EFF_")[0].strip()
                                    if "minimum" in payer:
                                        payer = "MIN"

                                    if "maximum" in payer:
                                        payer = "MAX"
                                    price_info["payer"] = str(payer).upper().replace("_", " ").replace("-", "").strip()

                                    if price_info["price"] != "N/A":
                                        if price_info["payer"] == "SELF PAY":
                                            price_info["payer"] = "CASH PRICE"

                                        if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                                            writer.writerow(price_info)
                                            # a = "s"
                                        else:
                                            import json; print(json.dumps(price_info, indent=2))
                    except ValueError:
                        print(row)
                        tb.print_exc()
