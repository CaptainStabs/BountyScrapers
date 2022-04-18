import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
# import heartrate; heartrate.trace(browser=True, daemon=True)

def write_data(price_info, writer, insurances, file, row):
    if "code" in price_info.keys():
        if not str(price_info["code"]).strip() or str(price_info["code"]) == "NONE":
            price_info["code"] = "NONE"
            price_info["code_disambiguator"] = price_info["description"]
    else:
        price_info["code"] = "NONE"
        price_info["code_disambiguator"] = price_info["description"]

    try:
        if len(str(price_info["code"]).strip()) == 4 and str(price_info["code"])[0] == "0":
            if str(price_info["internal_revenue_code"]) != "NONE":
                print(price_info["internal_revenue_code"])
            else:
                price_info["internal_revenue_code"] = price_info["code"]
                price_info["code"] = "NONE"
                price_info["code_disambiguator"] = row["description"]
        elif str(price_info["code"]).strip() == "0250":
            print(str(price_info["code"]), str(len(price_info["code"])))
    except KeyError:
        pass

    if re.compile('^\d$').search(price_info["code_disambiguator"]):
        price_info["code_disambiguator"] = price_info["description"]
        
    if price_info["internal_revenue_code"] == "0250":
        price_info["code_disambiguator"] = price_info["description"]

    writer.writerow(price_info)

def parse_row(file, writer, columns):
    with open(f"{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()]) - 1
        input_csv.seek(0)
        header = input_csv.readline().split(",")
        # print(insurance)
        insurances = ["Cash_Discount", "DeIdentified_Max_Allowed", "Deidentified_Min_Allowed","Gross_Charge","Payer_Allowed_Amount"]
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                # Associated_Codes,description,payer,
                price_info = {
                    "cms_certification_num": row["cms_certification_num"],
                    "description": " ".join(str(row["description"]).split()),
                    "inpatient_outpatient": row["inpatient_outpatient"],
                    "price": row["price"],
                    "code_disambiguator": row["code_disambiguator"].replace("NDC", "").replace("HCPCS", "").replace("CPT", "").replace("MS-DRG", ""),
                    "internal_revenue_code": row["internal_revenue_code"],
                    "payer": row["payer"],

                }

                # if str(" ".join(str(row["description"]).split())):
                #     price_info["code_disambiguator"] = " ".join(str(row["description"]).split())

                code = str(row["code"]).strip()

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
    columns = ["cms_certification_num", "code","description", "payer", "price", "inpatient_outpatient", "code_disambiguator", "internal_revenue_code"]
    with open(f"extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        file = "bad_codes.csv"
        parse_row(file, writer, columns)
