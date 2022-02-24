import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# import heartrate; heartrate.trace(browser=True, daemon=True)

# Facility,Type,Chargecode_DRG_CPT,Description,CPT,
# insurances = ["Aetna_W","Aetna_PPO","Anthem_Blue_Priority","Anthem_Blue_Preferred","Anthem_PPO","Aurora_Caregiver","Cigna_GPPO","Cigna_PPO","Exchange_-Common_Ground","Exchange_-Molina","Health_EOS_Plus","Health_EOS_PPO","HPS","Humana_WVN","Humana_HPN_HMO","Humana_PPO","Trilogy","UHC_HMO","UHC_PPO","WEA_State_and_Trust","WEA_Broad","WPS_Arise","WPS_Statewide","SELF_PAY","MIN","MAX"]
cms_num = {
    "antioch-medical": "050760",
    "fremont-medical": "050512",
    "fresno-medical": "050710",
    "oakland-medical": "050075",
    "redwood-city": "050541",
    "richmond-medical": "050075",
    "roseville-medical": "050772",
    "sacramento-medical": "050425",
    "san-francisco": "050076",
    "san-jose": "050604",
    "san-leandro": "050777",
    "san-rafael": "050510",
    "santa-clara": "050071",
    "santa-rosa": "050690",
    "south-sacramento": "050674",
    # stockton
    "south-san": "050070",
    "vacaville-medical": "050767",
    "vallejo-medical": "050073",
    "walnut-creek": "050072"
}

def parse_row(in_directory, file, writer, columns):
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
                # Charge # (Px Code),Description,CPT / HCPCS Code,Gross Charge,Discounted Cash Charge ,Hospital Inpatient / Outpatient / Both
                price_info = {
                    "cms_certification_num": cms_num["-".join(file.split("-")[:2])],
                    "internal_revenue_code": row["Charge # (Px Code)"],
                    "description": " ".join(str(row["Description"]).split()).replace("None", ""),
                    "code": str(row["CPT / HCPCS Code"]).strip().replace("None", "NONE"),
                    "payer": "GROSS CHARGE",
                    "price": row["Gross Charge"],
                    "inpatient_outpatient": str(row["Hospital Inpatient / Outpatient / Both"]).upper().strip().replace("None", "UNSPECIFIED")
                }

                if not str(row["CPT / HCPCS Code"]).strip() or str(row["CPT / HCPCS Code"]) == "NA":
                    price_info["code"] = "NONE"

                if not str(price_info["internal_revenue_code"]):
                    price_info["internal_revenue_code"] = "NONE"
                    print("A")
                # else:
                #     price_info["code"] = str(row["Procedure Code (CPT / HCPCS)"]).strip()

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
    columns = ["cms_certification_num", "internal_revenue_code", "code","description", "payer", "price", "inpatient_outpatient"]
    in_directory = "./output_files/supply/"
    with open(f"supplies_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        with ThreadPoolExecutor(max_workers=1) as executor:
            for file in os.listdir(in_directory):
                if file.endswith(".csv"):
                    threads.append(executor.submit(parse_row(in_directory, file, writer, columns)))
