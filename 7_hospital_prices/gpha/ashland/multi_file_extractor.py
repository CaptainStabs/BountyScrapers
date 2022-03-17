import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# import heartrate; heartrate.trace(browser=True, daemon=True)

def parse_row(in_directory, file, writer, columns):
    with open(f"{in_directory}{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)
        header = input_csv.readline().split(",")
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                code = row["CPT Code"]
                price_info = {
                    "cms_certification_num": "171304",
                    # "internal_revenue_code": row["Charge # (Px Code)"],
                    "description": " ".join(str(row["Description"]).split()).replace("None", ""),
                    "code": str(code).strip().replace("None", "NONE"),
                    "payer": "GROSS CHARGE",
                    "price": row["Pricing"].strip().replace("$", "").replace(",", "").split("|")[0],
                    "code_disambiguator": " ".join(str(row["Description"]).split()).replace("None", "")
                }

                # if price_info["description"].split(" ")[0].strip().isdigit():
                #     price_info["code_disambiguator"] = str(price_info["description"].split(" ")[0]).strip()

                if not str(code).strip() or str(code).strip() == "NA":
                    price_info["code"] = "NONE"

                if not str(price_info["code_disambiguator"]):
                    print("A")
                    price_info["code_disambiguator"] = "NONE"

                if str(price_info["price"]) and str(price_info["price"]) != "None":
                    if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                        # print("A")
                        writer.writerow(price_info)
                else:
                    print(file)
                    import json; print(json.dumps(row, indent=2))
                    break

            except ValueError:
                print(row)
                tb.print_exc()
                pass

if __name__ == "__main__":
    threads = []
    # "Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both(Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num", "code","description", "payer", "price", "code_disambiguator"]
    in_directory = "./input/"
    with open(f"extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        for file in os.listdir(in_directory):
            if file.endswith(".csv"):
                parse_row(in_directory, file, writer, columns)
