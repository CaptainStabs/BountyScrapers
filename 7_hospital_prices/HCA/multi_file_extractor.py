import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import re
# import heartrate; heartrate.trace(browser=True, daemon=True)

def write_data(price_info, writer,  file, row):
    if "code" in price_info.keys():
        if not str(price_info["code"]).strip():
            price_info["code"] = "NONE"
    else: price_info["code"] = "NONE"

    writer.writerow(price_info)


def parse_str(num):
    num = str(num).strip()
    """
    Parse a string that is expected to contain a number.
    :param num: str. the number in string.
    :return: float or int. Parsed num.
    """
    if not isinstance(num, str): # optional - check type
        raise TypeError('num should be a str. Got {}.'.format(type(num)))
    if re.compile('^\s*\d+\s*$').search(num):
        return int(num)
    if re.compile('^\s*(\d*\.\d+)|(\d+\.\d*)\s*$').search(num):
        return float(num)
    raise ValueError('num is not a number. Got {}.'.format(num)) # optional

def parse_row(file, writer, columns):
    rep = {"CPT/HCPC": "", "ICD 9/10": "", "MS-DRG": "", " or ": "", ";", ","}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))


    with open(f"{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()]) - 1
        input_csv.seek(0)
        header = input_csv.readline().split(",")
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
                    "code_disambiguator": "NONE",
                    "internal_revenue_code": row["internal_revenue_code"],
                    "payer": row["payer"],

                }

                if str(" ".join(str(row["description"]).split())):
                    price_info["code_disambiguator"] = " ".join(str(row["description"]).split())

                code = str(row["code"]).strip()
                code = pattern.sub(lambda m: rep[re.escape(m.group(0))], code)

                if not str(code).strip() or str(code).strip() == "N/A" or str(code) == "	":
                    price_info["code"] = "NONE"
                    write_data(price_info, writer, file, row)
                else:

                    if "REV " in code.upper():
                        is_rev = True
                        code = code.replace("REV", "")
                    else: is_rev = False

                    if "," in code:
                        for c in code.split(",").strip("-"):
                            if c[0] = "0" and len(c) = 4:
                                is_rev = True
                            if "-" in c:
                                prepend = ""
                                end_pend = ""

                                x, y = c.split("-")
                                if x[0].strip().isalpha() and y[0].strip().isalpha():
                                    if x[0] == y[0]:
                                        prepend = x[0]
                                        x, y = x[1:], y[1:]
                                    else:
                                        print("AAA")
                                        print(x[0], y[0])

                                if x[-1].strip().strip(";").isalpha() and y[-1].strip().strip(";").isalpha():
                                    if x[-1] == y[-1]:
                                        end_pend = x[-1]
                                        x, y = x[:-1], y[:-1]
                                    else:
                                        print("AAA")
                                        print(x[-1], y[-1])

                                if "." in x and "." in y:
                                    isfloat = True
                                else:
                                    isfloat = False

                                # Floats are only ISD codes
                                if isfloat:
                                    step = int(y.split(".")[-1].strip()) - int(x.split(".")[-1].strip())
                                    for codes in np.linspace(parse_str(x),parse_str(y), num=step):
                                        if is_rev:
                                            price_info["internal_revenue_code"] = str(codes)
                                            price_info["code"] = "NONE"
                                            # print(str(codes))
                                        else:
                                            # price_info["code"] = "{:.2f}".format(codes)
                                            # print("{:.2f}".format(codes))
                                            price_info["code"] = "".join([prepend, "{:.2f}".format(codes), end_pend]))

                                    write_data(price_info, writer, file, row)
                                else:
                                    for codes in np.arange(parse_str(x),parse_str(y)):
                                        if is_rev:
                                            price_info["internal_revenue_code"] = str(codes)
                                            price_info["code"] = "NONE"
                                            # print(str(codes))
                                        else:
                                            price_info["code"] = str(codes).zfill(3).strip(";")
                                            print(str(codes).zfill(3).strip(";"))

                                        if prepend or end_pend:
                                            print("".join([prepend, str(codes), end_pend]))
                            else:
                                if not str(c).strip() or str(c).strip() == "N/A" or str(c) == "	":
                                    price_info["code"] = "NONE"
                                else:
                                    if
                                    if is_rev:
                                        price_info["internal_revenue_code"] = c.strip().strip(";")
                                    else:
                                        price_info["code"] = c.strip().strip(";")
                                write_data(price_info, writer, file, row)
                    else:
                        if code[0] = "0" and len(code) == 4:
                            price_info["code"] = "NONE"
                            price_info["internal_revenue_code"] = code
                        write_data(price_info, writer, file, row)

            except ValueError:
                print(row)
                tb.print_exc()
                pass
def d_split(c, price_info, writer, file, row):

if __name__ == "__main__":
    threads = []
    # "Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both(Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num", "code","description", "payer", "price", "inpatient_outpatient", "code_disambiguator", "internal_revenue_code"]
    with open(f"extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        file = "hca.csv"
        parse_row(file, writer, columns)
