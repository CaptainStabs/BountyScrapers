import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from quantulum3 import parser
# import heartrate; heartrate.trace(browser=True, daemon=True)

# Facility,Type,Chargecode_DRG_CPT,Description,CPT,
# insurances = ["Aetna_W","Aetna_PPO","Anthem_Blue_Priority","Anthem_Blue_Preferred","Anthem_PPO","Aurora_Caregiver","Cigna_GPPO","Cigna_PPO","Exchange_-Common_Ground","Exchange_-Molina","Health_EOS_Plus","Health_EOS_PPO","HPS","Humana_WVN","Humana_HPN_HMO","Humana_PPO","Trilogy","UHC_HMO","UHC_PPO","WEA_State_and_Trust","WEA_Broad","WPS_Arise","WPS_Statewide","SELF_PAY","MIN","MAX"]
cms_num = {
    "270036480BANNER": "034004",
    "270036484BANNER": "030089",
    "270036499BANNER": "030002",
    "363386394BANNER": "030088",
    "450233470BANNER": "030016",
    "450233471BANNER": "031318",
    "470395795OGALLALA": "281355",
    "680422620BANNER": "051320",
    "830249708WASHAKIE": "531306",
    "830249710PLATTE": "531305",
    "840826331STERLING": "060076",
    "840826332MCKEE": "060030",
    "840826336EAST": "061303",
    "841287638NORTH": "060001",
    "860394148PAGE": "031304",
    "861035549BANNER": "030105",
    "900054201BANNER": "030065",
    "900065118BANNER": "030115",
    "900220728BANNER": "030122",
    "900412842BANNER": "030130",
    "900981239BANNER": "030134",
    "901074557BANNER": "030064",
    "901074558BANNER": "030111",
}

def parse_row(in_directory, file, writer, columns):
    with open(f"{in_directory}{file}", "r", encoding="utf-8") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)
        # header = input_csv.readline().split(",")
        # insurance = header[(header.index("Gross Charge")):-1]
        # print(insurance)
        # insurances = [x.replace("\n", "") for x in insurance]
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                # ,Default Modifier,Gross Charge,Discounted Cash Charge ,Hospital Inpatient / Outpatient / Both
                #  "payer", "price", "inpatient_outpatient"]
                price_info = {
                    "cms_certification_num": cms_num[file.split("-")[0]],
                    "description": " ".join(str(row["Charge Description"]).split()).replace("None", ""),
                    "code": str(row["CDM CPT Code"]).strip().replace("None", "NONE"),
                    "price": row["Price"],
                    "payer": "GROSS CHARGE"
                }

                desc = price_info["description"]
                if " MG/ML" in desc:
                    desc = desc.split(" ")
                    # print(desc)
                    price_info["units"] = " ".join(desc[desc.index("MG/ML")-1:])
                    price_info["code_disambiguator"] = " ".join(desc[desc.index("MG/ML")-1:])
                elif "MG/ML" in desc:
                    desc = desc.split(" ")
                    # print("\n", desc)
                    unit_index = [x for x, elem in enumerate(desc) if "MG/ML" in elem]
                    price_info["units"] = " ".join(desc[unit_index[0]:])
                    price_info["code_disambiguator"] = " ".join(desc[unit_index[0]:])
                else:
                    quants = parser.parse(desc)
                    quant = [x for x in quants if x.unit.entity.name=="mass" or x.unit.entity.name=="concentration" or x.unit.entity.name=="volume"]

                    if len(quant):
                        units = " ".join([(str(q.value) + str(q.unit.symbols[-1])) for q in quant if q.unit.symbols]) + " " + str(desc.split(" ")[-1])
                        price_info["units"] = units
                        price_info["code_disambiguator"] = units
                    else:
                        # price_info["code_disambiguator"] = "NONE"
                        price_info["code_disambiguator"] = price_info["description"]

                if not price_info["code_disambiguator"]:
                    print("\nNOT CODE DISAMBIGUATOR")
                    price_info["code_disambiguator"] = "NONE"


                code = str(str(row["CDM CPT Code"]).strip().replace("None", "NONE"))


                if not code or code == "NA":
                    price_info["code"] = "NONE"

                if str(price_info["price"]) and str(price_info["price"]) != "None":
                    if float(price_info["price"]) <= 10000000:
                        # print("A")
                        # a = ""
                        writer.writerow(price_info)
                else:
                    print(file)
                    import json; print(json.dumps(row, indent=2))
                    break

                            # a = "s"
                        # else:
                        #     import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                print(row)
                tb.print_exc()
                pass

if __name__ == "__main__":
    threads = []
    # "Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both(Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num", "code","description", "payer", "price", "units", "code_disambiguator"]
    in_directory = "./fixed/cdm/"
    with open(f"CDM_extracted_data.csv", "a", newline="", encoding="utf-8") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        with ThreadPoolExecutor(max_workers=5) as executor:
            for file in tqdm(os.listdir(in_directory)):
                if file.endswith(".csv"):
                    threads.append(executor.submit(parse_row(in_directory, file, writer, columns)))
