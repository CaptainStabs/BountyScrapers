import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# import heartrate; heartrate.trace(browser=True, daemon=True)

cms_num = {
    "362739299": "160104",
    "362739300": "140280",
    "370661223": "140209",
    "370681540": "140013",
    "370692351": "140120",
    "390806367": "520089",
    "420504780": "160045",
    "420680337": "160013",
    "420680452": "160082",
    "420698265": "160110",
    "420933383": "160147",
    "421009175": "160016",
    "421487967": "161306",
    "815034179": "160001"
}

payers = {
    "Cash_Discount": "CASH PRICE",
    "DeIdentified_Max_Allowed": "MAX",
    "DeIdentified_Min_Allowed": "MIN",
    "Gross_Charge": "GROSS CHARGE",
}

def write_data(price_info, writer, insurances, file, row):
    if "code" in price_info.keys():
        if not str(price_info["code"]).strip():
            price_info["code"] = "NONE"
    else: price_info["code"] = "NONE"

    for payer in insurances:
        if row[payer] == "N/A" or row[payer] == "-":
            continue

        price_info["price"] = row[payer].replace("$", "").replace(",", "")

        try:
            price_info["payer"] = payers[payer]

        except KeyError:
            price_info["payer"] = row["payer"].upper().strip()

        if str(price_info["price"]) and str(price_info["price"]) != "None":
            if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                # print("A")
                writer.writerow(price_info)

            else:
                print(file)
                import json; print(json.dumps(row, indent=2))
                break



def parse_row(in_directory, file, writer, columns):
    with open(f"{in_directory}{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()]) - 1
        input_csv.seek(0)
        header = input_csv.readline().split(",")
        # print(insurance)
        insurances = ["Cash_Discount", "DeIdentified_Max_Allowed", "Deidentified_Min_Allowed","Gross_Charge","Payer_Allowed_Amount"]
        input_csv.seek(0)
        print(cms_num["".join(file.split("_")[0])])

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                # Associated_Codes,description,payer,
                price_info = {
                    "cms_certification_num": cms_num["".join(file.split("_")[0])],
                    "description": " ".join(str(row["description"]).split()),
                    "inpatient_outpatient": str(row["iobSelection"]).upper().strip().replace("None", "UNSPECIFIED"),
                }

                if str(price_info["description"]):
                    price_info["code_disambiguator"] = price_info["description"]

                if not str(price_info["inpatient_outpatient"]):
                    price_info["inpatient_outpatient"] = "UNSPECIFIED"

                if price_info["inpatient_outpatient"] == "OUPATIENT":
                    price_info["inpatient_outpatient"] = "OUTPATIENT"

                code = str(row["Associated_Codes"]).strip()

                if not str(code).strip() or str(code).strip() == "N/A" or str() or str(code) == "	":
                    price_info["code"] = "NONE"
                    write_data(price_info, writer, insurances, file, row)
                else:
                    if "," in code:
                        for c in code.split(","):
                            if "-" in c:
                                x, y = c.split("-")
                                for codes in range(int(x),int(y)):
                                    if not str(c).strip() or str(c).strip() == "N/A" or str(c) == "	":
                                        price_info["code"] = "NONE"
                                    else:
                                        price_info["code"] = str(codes).zfill(3)
                                    write_data(price_info, writer, insurances, file, row)
                            else:
                                if not str(c).strip() or str(c).strip() == "N/A" or str(c) == "	":
                                    price_info["code"] = "NONE"
                                else:
                                    price_info["code"] = c.strip()
                                write_data(price_info, writer, insurances, file, row)
                    else:
                        write_data(price_info, writer, insurances, file, row)

            except ValueError:
                print(row)
                tb.print_exc()
                pass

if __name__ == "__main__":
    threads = []
    # "Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both(Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num", "code","description", "payer", "price", "inpatient_outpatient", "code_disambiguator"]
    in_directory = "./output_files/"
    with open(f"extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        for file in os.listdir(in_directory):
            if file.endswith(".csv"):
                parse_row(in_directory, file, writer, columns)
