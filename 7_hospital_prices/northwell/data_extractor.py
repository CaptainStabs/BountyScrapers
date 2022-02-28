import csv
from tqdm import tqdm
import traceback as tb
import os
# import heartrate; heartrate.trace(browser=True, daemon=True)

# Facility,Type,Chargecode_DRG_CPT,Description,CPT,
# insurances = ["Aetna_W","Aetna_PPO","Anthem_Blue_Priority","Anthem_Blue_Preferred","Anthem_PPO","Aurora_Caregiver","Cigna_GPPO","Cigna_PPO","Exchange_-Common_Ground","Exchange_-Molina","Health_EOS_Plus","Health_EOS_PPO","HPS","Humana_WVN","Humana_HPN_HMO","Humana_PPO","Trilogy","UHC_HMO","UHC_PPO","WEA_State_and_Trust","WEA_Broad","WPS_Arise","WPS_Statewide","SELF_PAY","MIN","MAX"]
cms_num = {
    "Glen Cove Hospital": "330181",
    "Huntington Hospital": "330045",
    "Lenox Hill Hospital": "330119",
    "North Shore University Hospital": "330106",
    "Plainview Hospital": "330331",
    "South Shore University Hospital": "330395",
    "Staten Island University Hospital": "330160",
}

# Type,Chargecode_DRG_CPT,Description,CPT,_1_1_21_Fee,
columns = ["cms_certification_num","code", "price", "payer"]
in_directory = "./data/"
with open(f"extracted_data.csv", "a", newline="") as output_csv:
    writer = csv.DictWriter(output_csv, fieldnames=columns)
    writer.writeheader()
    with open(f"mrf.csv", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)


        for row in tqdm(reader, total=line_count):
            try:
                price_info = {
                    "cms_certification_num": cms_num[row["Hospital_Name"].strip()],
                    "code": str(row["Code_TXT"]).upper(),
                    "payer": str(row["Payor"]).replace("_", " ").replace("-", "").strip(),

                }

                if not str(row["Code_TXT"]).strip() or str(row["Code_TXT"]) == "NA":
                    price_info["code"] = "NONE"
                else:
                    price_info["code"] = str(row["Code_TXT"]).strip()


                price_info["price"] = str(row["Rate"]).replace(",", "")

                try:
                    if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                        writer.writerow(price_info)
                        # a = "s"
                    else:
                        import json; print(json.dumps(price_info, indent=2))
                except ValueError:
                    pass

            except ValueError:
                print(row)
                tb.print_exc()

            except KeyError:
                pass
