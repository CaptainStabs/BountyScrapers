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


def parse_str(num,c):
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
    raise ValueError('num is not a number. Got "{}". {}'.format(num, c)) # optional
    import sys; sys.exit()

def parse_row(file, writer, columns):
    rep = {"CPT/HCPC ": "", "ICD 9/10": "", "MS-DRG": "", " or ": "", ";": ",", "Code": "", "code":"", "codes":"", "Codes":"", "Includes CPT4 Codes": "", "HCPCS":"", "Excluded CPTs from the surgery range:":"", "ICD9 s": "", "(": "", ")":"", "'": ""}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))


    with open(f"{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines() if line.strip()]) - 1
        input_csv.seek(0)
        header = input_csv.readline().split(",")
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                # Associated_Codes,description,payer,
                price_info = {
                    "cms_certification_num": row["cms_certification_num"],
                    "payer": row["payer"],
                    "internal_revenue_code": row["internal_revenue_code"],
                    "units": row["units"],
                    "description": " ".join(str(row["description"]).split()),
                    "inpatient_outpatient": row["inpatient_outpatient"],
                    "price": row["price"],
                    "code_disambiguator": "NONE",
                }

                if str(" ".join(str(row["description"]).split())):
                    price_info["code_disambiguator"] = " ".join(str(row["description"]).split())

                code = str(row["code"]).strip()
                code = pattern.sub(lambda m: rep[re.escape(m.group(0))], code)

                if not str(code).strip() or str(code).strip() == "N/A" or str(code) == "	":
                    price_info["code"] = "NONE"
                    write_data(price_info, writer, file, row)
                elif "level" in code.lower():
                    price_info["code"] = row["code"].replace("CPT/HCPC ")
                else:
                    if "REV " in code.upper() or "REV" in code.upper():
                        is_rev = True
                        code = code.replace("REV", "").strip()
                    else: is_rev = False

                    if "," in code:
                        p = re.compile('[a-zA-Z]{1}[0-9]{1}[a-zA-Z0-9]{1}.{1}[a-zA-Z0-9]{0,4}')
                        if "excluding" in code.lower():
                            c_s = code.split("excluding")
                            c_range, exclusions = c_s[0], c_s[1]

                            
                        for c in code.strip("-").split(","):
                            if "-" in c.strip("-") and not bool(p.search(c.split("-")[0].strip())):
                                d_split(c, price_info, writer, file, row, is_rev)
                            else:
                                if not is_rev:
                                    # Double check to confirm
                                    is_rev = rev_checker(c)

                                if not str(c).strip() or str(c).strip() == "N/A" or str(c) == "	":
                                    price_info["code"] = "NONE"
                                else:
                                    if is_rev:
                                        price_info["internal_revenue_code"] = c.strip().strip(";")
                                        price_info["code"] = "NONE"

                                    else:
                                        price_info["code"] = c.strip().strip(";")

                                    write_data(price_info, writer, file, row)
                    elif "-" in code.strip("-"):
                        d_split(code, price_info, writer, file, row)
                    else:
                        if rev_checker(code):
                            price_info["code"] = "NONE"
                            price_info["internal_revenue_code"] = code

                        else:
                            write_data(price_info, writer, file, row)

            except ValueError:
                print("\nValueError", row["code"])
                tb.print_exc()
                import sys; sys.exit()
                pass

def d_split(c, price_info, writer, file, row, is_rev):
    padding = 0
    if "REV " in c.upper() or "REV" in c.upper():
        is_rev = True
        # Probably ineffecient to do this everytime the function is called,
        # but I'm too lazy to move it into the main part of the code and add all args...
        rep = {"rev": "", "Rev": "", "REV": "", "Codes": ""}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        c = pattern.sub(lambda m: rep[re.escape(m.group(0))], c)

    else: is_rev = rev_checker(c)

    prepend = ""
    end_pend = ""

    # Split by - to get min and max
    x, y = c.split("-")
    x, y = x.strip().strip(")"), y.strip().strip(")")
    # I feel that the last item in the range is more likely to have a semicolon
    y = y.strip(";")
    if x and y:
        # Check if the first character is a letter, so that I can add it back in later
        if x[0].isalpha() and y[0].isalpha():
            if x[0] == y[0]:
                prepend = x[0]
                # Remove the first character to prevent errors
                x, y = x.strip()[1:], y.strip()[1:]
                if x[0] == "0":
                    # Preserve any and all padding
                    padding = len(x)
            else:
                print("AAA")
                print(x[0], y[0])
        # Check last if last character is a letter, so that I can add it back in later
        if x[-1].strip().strip(";").isalpha() and y[-1].strip().strip(";").isalpha():
            if x[-1] == y[-1]:
                end_pend = x[-1]
                x, y = x.strip()[:-1], y.strip()[:-1]

                if x[0] == "0":
                    padding = len(x)
            else:
                print("BBB")
                print(x[-1], y[-1])

        # Naive way to check if x is a float
        if "." in x and "." in y:
            isfloat = True
        else:
            isfloat = False

        # Floats are only ICD 9/10 codes afaict
        if isfloat:
            # Number of steps between the two numbers, i.e. num of steps between 9 and 1 is 8
            x2, y2 = x.split("."), y.split(".")
            # Confirm that there is in fact numbers after the decimal point
            if str(y2[-1].strip()) and str(x2[-1].strip()):
                step = int(y.split(".")[-1].strip()) - int(x.split(".")[-1].strip())


                for codes in np.linspace(parse_str(x, c),parse_str(y, c), num=step):
                    if is_rev:
                        # Figured I might as well leave this in just in case I'm wrong
                        price_info["internal_revenue_code"] = str(codes)
                        price_info["code"] = "NONE"
                    else:
                        # Re-add the removed letters
                        price_info["code"] = "".join([prepend, "{:.2f}".format(codes), end_pend])

                    write_data(price_info, writer, file, row)
            else:
                print("\nMissing an x or y for", c)
        else:
            try:
                for codes in range(parse_str(x, c),parse_str(y, c) + 1):
                    if is_rev:
                        price_info["internal_revenue_code"] = str(codes)
                        price_info["code"] = "NONE"

                    else:
                        # Only need this here because it is within the generator
                        if len(str(x)) == 3 and len(str(y)) == 3:
                            price_info["code"] = str(codes).zfill(3).strip(";")
                        else: price_info["code"] = "".join([prepend, str(codes).zfill(padding), end_pend])
                        # print(str(codes).zfill(3).strip(";"))
            except:
                print("192 failure", c)
                import sys; sys.exit(1)
    else:
        print("\nx or y is null: ", ",".join([x,y]))

def rev_checker(c):
    c = c.strip()
    if "." in c:
        return False
        print("\nc has a period, returning false", c)
    else:
        try:
            if c[0] == "0" and len(c) == 4:
                return True
            else: return False
        except IndexError:
            # print("\nindex error", c)
            return False
if __name__ == "__main__":
    threads = []
    # "Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both(Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num", "code","description", "payer", "price", "inpatient_outpatient", "code_disambiguator", "internal_revenue_code", "units"]
    if os.path.exists("extracted_data.csv"):
        os.remove("extracted_data.csv")

    with open(f"extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        file = "hca.csv"
        parse_row(file, writer, columns)
