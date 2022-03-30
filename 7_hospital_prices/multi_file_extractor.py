import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# import heartrate; heartrate.trace(browser=True, daemon=True)

cms_num = {

}

def parse_row(in_directory, file, writer, columns):
    with open(f"{in_directory}{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()]) - 1
        input_csv.seek(0)
        header = input_csv.readline().split(",")
        insurance = header[(header.index("Gross Charge")):]
        # print(insurance)
        insurances = [x.replace("\n", "") for x in insurance]
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                code = row["code"]
                price_info = {
                    "cms_certification_num": cms_num["-".join(file.split("-")[:2])],
                    # "internal_revenue_code": row["Charge # (Px Code)"],
                    "description": " ".join(str(row["Description"]).split()).replace("None", ""),
                    "code": str(code).strip().replace("None", "NONE"),
                    # "payer": "GROSS CHARGE",
                    # "price": row["Gross Charge"],
                    "inpatient_outpatient": str(row["Hospital Inpatient / Outpatient / Both"]).upper().strip().replace("None", "UNSPECIFIED")
                }

                internal_revenue_code = str(price_info["internal_revenue_code"])

                if not str(code).strip() or str(code).strip() == "NA":
                    price_info["code"] = "NONE"

                for payer in insurances:
                    price_info["price"] = row[payer]
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
    columns = ["cms_certification_num", "code","description", "payer", "price", "inpatient_outpatient"]
    in_directory = "./output_files/CDM/"
    with open(f"CDM_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        with ThreadPoolExecutor(max_workers=1) as executor:
            for file in os.listdir(in_directory):
                if file.endswith(".csv"):
                    threads.append(executor.submit(parse_row, in_directory, file, writer, columns))
