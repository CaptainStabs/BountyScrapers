import csv
from tqdm import tqdm
import traceback as tb
import os
# import heartrate; heartrate.trace(browser=True, daemon=True)

# Facility,Type,Chargecode_DRG_CPT,Description,CPT,
# insurances = ["Aetna_W","Aetna_PPO","Anthem_Blue_Priority","Anthem_Blue_Preferred","Anthem_PPO","Aurora_Caregiver","Cigna_GPPO","Cigna_PPO","Exchange_-Common_Ground","Exchange_-Molina","Health_EOS_Plus","Health_EOS_PPO","HPS","Humana_WVN","Humana_HPN_HMO","Humana_PPO","Trilogy","UHC_HMO","UHC_PPO","WEA_State_and_Trust","WEA_Broad","WPS_Arise","WPS_Statewide","SELF_PAY","MIN","MAX"]
cms_num = {
    "KENOSHA": "520189",
    # "LAKELAND": "520102",
    "MANITOWOC": "520034",
    "OSHKOSH": "520198",
    "PSYCH": "524000",
    "SHEBOYGAN": "520035",
    "ST. LUKE'S": "520138",
    "SUMMIT": "520206",
    "HARTFORD": "520038",
    "WEST ALLIS": "520139"
}

# Type,Chargecode_DRG_CPT,Description,CPT,_1_1_21_Fee,
columns = ["cms_certification_num", "internal_revenue_code", "description", "code", "price", "inpatient_outpatient", "payer"]
in_directory = "./_output_files/"
for file in os.listdir(in_directory):
    if file.endswith(".csv"):
        with open(f"./_output_files/{file}", "r") as input_csv:
            line_count = len([line for line in input_csv.readlines()])
            input_csv.seek(0)
            header = input_csv.readline().split(",")
            insurance = header[(header.index("_1_1_21_Fee")+1):]
            insurances = [x.replace("\n", "") for x in insurance]
            input_csv.seek(0)

            reader = csv.DictReader(input_csv)
            if not os.path.exists(file.replace(".csv", "")):
                os.mkdir(file.replace(".csv", ""))

            with open(f"{file.replace('.csv', '').upper()}/extracted_data.csv", "a", newline="") as output_csv:
                writer = csv.DictWriter(output_csv, fieldnames=columns)
                writer.writeheader()

                for row in tqdm(reader, total=line_count):
                    try:
                        if str(row["CPT"]).strip() and str(row["CPT"]) != "NA":
                            price_info = {
                                "cms_certification_num": cms_num[row["Facility"]],
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
