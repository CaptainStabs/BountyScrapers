import csv
from tqdm import tqdm
import traceback as tb
import os
# import heartrate; heartrate.trace(browser=True, daemon=True)

# Facility,Type,Chargecode_DRG_CPT,Description,CPT,
# insurances = ["Aetna_W","Aetna_PPO","Anthem_Blue_Priority","Anthem_Blue_Preferred","Anthem_PPO","Aurora_Caregiver","Cigna_GPPO","Cigna_PPO","Exchange_-Common_Ground","Exchange_-Molina","Health_EOS_Plus","Health_EOS_PPO","HPS","Humana_WVN","Humana_HPN_HMO","Humana_PPO","Trilogy","UHC_HMO","UHC_PPO","WEA_State_and_Trust","WEA_Broad","WPS_Arise","WPS_Statewide","SELF_PAY","MIN","MAX"]
cms_num = {
    "NORTH VALLEY": "050766",
    "ROSEVILLE": "050309",
    "SACRAMENTO": "050108",
    "SANTA ROSA": "050291",
    "SOLANO": "050101",
    "SUTTER AMADOR": "050014",
    "SUTTER AUBURN FAITH": "050498",
    "SUTTER CENTER": "054096",
    "SUTTER COAST": "050417",
    "SUTTER DAVIS": "050537",
    "SUTTER DELTA": "050523",
    "SUTTER LAKESIDE": "051329",
    "SUTTER MATERNITY SURGERY CENTER": "050714",
    "SUTTER TRACY": "050313"

}
#  ID,SERVICE_SETTING,DESCRIPTION,CPT,NDC,REVENUE_CODE,
columns = ["cms_certification_num", "internal_revenue_code", "description", "code", "price", "inpatient_outpatient", "payer", "code_disambiguator"]
in_directory = "./input_files/"
with open(f"extracted_data.csv", "a", newline="", encoding="utf-8") as output_csv:
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
                        if str(row["CPT"]).strip() and str(row["CPT"]) != "NA":
                            price_info = {
                                "cms_certification_num": cms_num[(file.replace(".csv", "").upper())],
                                "internal_revenue_code": row["REVENUE_CODE"],
                                "code": str(row["CPT"]).upper(),
                                "description": " ".join(str(row["DESCRIPTION"]).upper().split()),
                            }
                        elif row["NDC"] and not str(row["CPT"]):
                            price_info = {
                                "cms_certification_num": cms_num[(file.replace(".csv", "").upper())],
                                "internal_revenue_code": row["REVENUE_CODE"],
                                "code": "NDC " + str(row["NDC"]).upper(),
                                "description": " ".join(str(row["DESCRIPTION"]).upper().split()),
                            }
                        else:
                            continue

                        try:
                            price_info["code_disambiguator"] = row["ID"]
                        except KeyError:
                            # Some invisible character is messing it up
                            try:
                                price_info["code_disambiguator"] = row["ï»¿ID"]
                            except KeyError:
                                print(row)

                        if not str(row["REVENUE_CODE"]):
                            price_info["internal_revenue_code"] = "NONE"

                        inpatient_outpatient = str(row["SERVICE_SETTING"]).upper()
                        if "INPATIENT" in inpatient_outpatient:
                            price_info["inpatient_outpatient"] = "INPATIENT"
                        elif "OUTPATIENT" in inpatient_outpatient:
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
