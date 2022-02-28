import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# import heartrate; heartrate.trace(browser=True, daemon=True)

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
    with open(f"{in_directory}{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)
        header = input_csv.readline().split(",")
        insurance = header[(header.index("Discounted_Cash_Price")):-1]
        insurances = [x.replace("\n", "") for x in insurance]
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                code = row["Code"]
                price_info = {
                    "cms_certification_num": cms_num[file.split("-")[0]],
                    "description": " ".join(str(row["Description"]).split()).replace("None", ""),
                    "code": str(code).strip().replace("None", "NONE"),
                    "code_disambiguator": " ".join(str(row["Description"]).split()).replace("None", "")
                }

                code = str(price_info["code"])

                if not str(code).strip() or str(code) == "NA":
                    price_info["code"] = "NONE"

                for payer in insurances:
                    price_info["price"] = row[payer]
                    if "SELF PAY" in payer:
                        price_info["payer"] = "CASH PRICE" + str(payer.split("SELF PAY")[-1])

                    elif payer == "Discounted_Cash_Price":
                        price_info["payer"] = "CASH PRICE"

                    elif payer == "Min_Allowable_":
                        price_info["payer"] = "MIN"

                    elif payer == "Max_Allowable_":
                        price_info["payer"] = "MAX"

                    elif payer == "Avg Charge " or payer == "Avg Charge" or payer == "Avg_Allowable":
                            continue
                    else:
                        price_info["payer"] = str(payer).strip()

                    if str(price_info["price"]) and str(price_info["price"]) != "None":
                        if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                            # print("A")
                            writer.writerow(price_info)

                    if not price_info["code_disambiguator"]:
                        price_info["code_disambiguator"] = "NONE"
                    # else:
                        # print(file)
                        # import json; print(json.dumps(row, indent=2))
                        # break

            except ValueError:
                print(row)
                tb.print_exc()
                pass
        return file
if __name__ == "__main__":
    threads = []
    # "Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both(Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num", "code","description", "payer", "price", "code_disambiguator"]
    in_directory = "./fixed/payers/"
    with open(f"payers_extracted_data.csv", "a", newline="", encoding="utf-8") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        with ThreadPoolExecutor(max_workers=23) as executor:
            for file in os.listdir(in_directory):
                if file.endswith(".csv"):
                    threads.append(executor.submit(parse_row, in_directory, file, writer, columns))

            # for task in tqdm(as_completed(threads)):
            #     print(task.result())

        # for file in os.listdir(in_directory):
        #     if file.endswith(".csv"):
        #         parse_row(in_directory, file, writer, columns)
