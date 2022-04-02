import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
# import heartrate; heartrate.trace(browser=True, daemon=True)

cms_num = {
    "JOHNSTON MEMORIAL": "490053",
    "SMYTH COUNTY": "490038",
    "FRANKLIN WOODS": "330184",
    "INDIAN PATH": "440176",
    "JOHNSON CITY": "440063",
    "JOHNSON COUNTY": "441304",
    "RUSSELL COUNTY": "490002",
    "SYCAMORE SHOALS": "440018",
    "UNICOI COUNTY": "440001",
    "GREENEVILLE COMMUNITY": "440050",
    "BRISTOL REGIONAL": "440012",
    "HANCOCK COUNTY": "441313",
    "HOLSTON VALLEY": "440017",
    "LONESOME PINE": "490114",
    "HAWKINS COUNTY": "440032",
    "DICKENSON COMMUNITY": "491303",
    "A A.CSV": "490001"
}

payers = {
    "Gross IP Price": "GROSS CHARGE",
    "Gross OP Price": "GROSS CHARGE",
    "Self Pay-Self Pay": "CASH PRICE",
    "De-Identified Minimum": "MIN",
    "De-Identified Maximum": "MAX"
}

def parse_row(in_directory, file, writer, columns):
    print(file)
    with open(f"{in_directory}{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()]) - 1
        input_csv.seek(0)
        header = re.split(r',(?=(?:"[^"]*?(?: [^"]*)*))|,(?=[^",]+(?:,|$))', input_csv.readline())
        try:
            insurance = header[(header.index("Gross IP Price")):]
        except:
            print(header[0:16])
            a = b
        insurances = [x.replace("\n", "").replace('"', "") for x in insurance]
        insurances.pop(insurances.index("ProcedureDescription"))
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                price_info = {
                    "cms_certification_num": cms_num[" ".join(file[10:].split(" ")[:2]).upper()],
                    "internal_revenue_code": row["Rev Code"],
                    "description": " ".join(str(row["ProcedureDescription"]).split()).replace("None", ""),
                    "units": row["Quantity"],
                    "code_disambiguator": "NONE"
                }

                cpt = str(row["CPT"]).strip()
                ndc = str(row["NDC"]).strip()
                mcr = ""

                if price_info["cms_certification_num"] == "490053":
                    mcr = str(row["MCR"]).strip()


                # l = [hcpcs, drg, ndc]
                l = [x for x in [cpt, mcr, ndc] if x.strip()]

                if l:
                    price_info["code"] = l[0]

                    if len(l) > 1:
                        code_disambiguator = l[1:]
                    else: code_disambiguator = "NONE"

                else:
                    price_info["code"] = "NONE"
                    price_info["code_disambiguator"] = code_disambiguator

                proc, code_type, char_code = row["Procedure"], row["CodeType"], row["Charge Code"]
                l = [x for x in [proc, code_type, char_code] if x.strip()]

                if price_info["code_disambiguator"] == "NONE":
                    price_info["code_disambiguator"] = " ".join(l)
                else:
                    price_info["code_disambiguator"] = " ".join([price_info["code_disambiguator"], " ".join(l)])


                if not str(price_info["internal_revenue_code"]):
                    price_info["internal_revenue_code"] = "NONE"

                for payer in insurances:
                    price_info["price"] = row[payer]

                    if row[payer] == "NA" or row[payer] == "nan":
                        continue

                    try:
                        price_info["payer"] = payers[payer]
                    except KeyError:
                        price_info["payer"] = payer

                    if " IP " in payer:
                        price_info["inpatient_outpatient"] = "INPATIENT"
                    elif " OP " in payer:
                        price_info["inpatient_outpatient"] = "OUTPATIENT"
                    else:
                        price_info["inpatient_outpatient"] = "UNSPECIFIED"

                    if str(price_info["price"]) and str(price_info["price"]) != "None":
                        if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                            writer.writerow(price_info)
                    else:
                        print(file)
                        print(row[payer])
                        break

            except ValueError:
                # print(row)
                print(file)
                tb.print_exc()
                pass

if __name__ == "__main__":
    threads = []
    # "Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both(Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num", "code","description", "payer", "price", "inpatient_outpatient", "code_disambiguator", "internal_revenue_code", "units"]
    in_directory = "./fixed/"
    with open(f"extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        for file in os.listdir(in_directory):
            if file.endswith(".csv"):
                parse_row(in_directory, file, writer, columns)
