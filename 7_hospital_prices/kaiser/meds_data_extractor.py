import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# import heartrate; heartrate.trace(browser=True, daemon=True)

# Facility,Type,Chargecode_DRG_CPT,Description,CPT,
# insurances = ["Aetna_W","Aetna_PPO","Anthem_Blue_Priority","Anthem_Blue_Preferred","Anthem_PPO","Aurora_Caregiver","Cigna_GPPO","Cigna_PPO","Exchange_-Common_Ground","Exchange_-Molina","Health_EOS_Plus","Health_EOS_PPO","HPS","Humana_WVN","Humana_HPN_HMO","Humana_PPO","Trilogy","UHC_HMO","UHC_PPO","WEA_State_and_Trust","WEA_Broad","WPS_Arise","WPS_Statewide","SELF_PAY","MIN","MAX"]
cms_num = {
    "central-hospital": "500052",
    "moanalua-medical": "120011"
}


def parse_row(in_directory, file, writer, columns):
    with open(f"{in_directory}{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)
        header = input_csv.readline().split(",")
        insurance = header[(header.index("Gross Charge")):-1]
        insurances = [x.replace("\n", "") for x in insurance]
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                # CPT / HCPCS Code or Charge #,Description,,Medication Quantity,Medication Units,Gross Charge,Hospital Inpatient / Outpatient / Both
                price_info = {
                    "cms_certification_num": cms_num["-".join(file.split("-")[:2])],
                    # "internal_revenue_code": row["CPT / HCPCS Code or Charge #"],
                    "description": " ".join(str(row["Description"]).split()).replace("None", ""),
                    "code": str(row["CPT / HCPCS Code or Charge #"]).strip().replace("None", "NONE"),
                    "units": " ".join([row["Medication Quantity"], row["Medication Units"]]),
                    # "payer": "GROSS CHARGE",
                    # "price": row["Gross Charge"],
                    "inpatient_outpatient": str(row["Hospital Inpatient / Outpatient / Both"]).upper().strip().replace("None", "UNSPECIFIED")
                }

                if not str(row["CPT / HCPCS Code or Charge #"]).strip() or str(row["CPT / HCPCS Code or Charge #"]) == "NA":
                    price_info["code"] = "NONE"
                # else:
                #     price_info["code"] = str(row["Procedure Code (CPT / HCPCS)"]).strip()

                for payer in insurances:
                    price_info["price"] = row[payer].replace(",", "").replace("$", "").strip()
                    if "Discounted" in payer:
                        price_info["payer"] = "CASH PRICE"
                    elif payer == "Gross Charge":
                        price_info["payer"] = "GROSS CHARGE"

                    elif "Kaiser Foundation" in payer:
                        price_info["payer"] = payer
                    else:
                        continue

                    if str(price_info["price"]) and str(price_info["price"]) != "None":
                        if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                            writer.writerow(price_info)

                            # a = "s"
                        else:
                            import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                print(row)
                tb.print_exc()

if __name__ == "__main__":
    threads = []
    # CPT / HCPCS Code or Charge #,Description,,Medication Quantity,Medication Units,Gross Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num","code","description", "units", "payer", "price", "inpatient_outpatient"]
    in_directory = "./output_files/meds/"
    with open(f"meds_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        with ThreadPoolExecutor(max_workers=1) as executor:
            for file in os.listdir(in_directory):
                if file.endswith(".csv"):
                    threads.append(executor.submit(parse_row(in_directory, file, writer, columns)))
