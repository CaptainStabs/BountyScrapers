import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import re
import logging
logging.basicConfig(level=logging.INFO)
# import heartrate; heartrate.trace(browser=True, daemon=True)

def write_data(price_info, writer,  file, row):
    if "code" in price_info.keys():
        if not str(price_info["code"]).strip():
            price_info["code"] = "NONE"
    else: price_info["code"] = "NONE"

    code = price_info["code"]
    if str(code)[0] == "0" and len(str(code)) == 4 and "." not in str(code):
        if price_info["internal_revenue_code"] == "NONE":
            price_info["internal_revenue_code"] = code
            price_info["code"] = "NONE"
            print("Rev in code")
        else:
            print("Rev in code, rev occupided:", price_info["internal_revenue_code"])

    price_info["code"] = str(code).strip().strip("-")
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
    rep = {"CPT/HCPC ": "", "ICD 9/10": "", "MS-DRG": "", " or ": "", ";": ",", "codes":"", "Codes":"", "Includes CPT4 Codes": "",  "Code": "", "code":"", "HCPCS":"", "ICD9 s": "", "(": "", ")":"", "'": "", "CPT": "", ":": "", "and/or": ",", " or ": ", ", "MS-DRG": "", " CPT/HCPC": ""}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))


    with open(f"{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines() if line.strip()]) - 1
        input_csv.seek(0)
        header = input_csv.readline().split(",")
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for i, row in enumerate(tqdm(reader, total=line_count)):
            # if i < 358917:
            #     continue
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

                # if str(" ".join(str(row["description"]).split())):
                #     price_info["code_disambiguator"] = " ".join(str(row["description"]).split())

                # Make my life easier and filter out garbage
                code = str(row["code"]).strip()
                code = pattern.sub(lambda m: rep[re.escape(m.group(0))], code)
                code = code.replace(" CPT/HCPC", "")

                if not str(code).strip() or str(code).strip() == "N/A" or str(code) == "	":
                    price_info["code"] = "NONE"
                    write_data(price_info, writer, file, row)
                elif "level" in code.lower(): # edge case for emergency level stuff
                    price_info["code"] = row["code"].replace("CPT/HCPC ", "").strip()
                else:
                    if "REV " in code.upper() or "REV" in code.upper():
                        is_rev = True
                        code = code.replace("REV", "").strip()
                    else: is_rev = False

        		    # regex for detecting ICD codes
                    p2 = re.compile("\d\d\d\d\d/\d\d\d\d\d-\d\d")
                    # print(bool(p2.match(code)))
                    if "," in code:
                        if "excluding" in code.lower() or "excluded" in code.lower():
                            price_info["code"] = code
                            write_data(price_info, writer, file, row)

                        else:
                            comma_loop(code, price_info, writer, file, row, is_rev)
                    # elif "-" in code.strip("-").strip("-") and " - " not in code:
                    #     if bool(p2.search(code)) or "28890/28890-50" in code:
                    #         write_data(price_info, writer, file, row)
                    #     else:
                    #         d_split(code, price_info, writer, file, row, is_rev)
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
def comma_loop(code, price_info, writer, file, row, is_rev):
    # ICD 9/10 regex filters
    p = re.compile('[0-9]{1}[a-zA-Z]{1}[a-zA-Z0-9]{1}.{1}[a-zA-Z0-9]{0,4}')
    p2 = re.compile("\d\d\d\d\d/\d\d\d\d\d-\d\d")
    p3 = re.compile("\d\d\d-\d\d-\d\d\d\d\d")
    # logging.debug("Comma loop main loop")
    for c in code.strip("-").split(","):
        if not p2.match(c) and "28890/28890-50" not in c and not p3.match(c.strip()):
            if "-" in c.strip().strip("-") and not bool(p.search(c.strip().split("-")[0].strip())):
                if not c.split("-")[0].strip(): print(c.strip("-"))
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
        else:
            price_info["code"] = c
            # print(c)
            write_data(price_info, writer, file, row)
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

    has_letter = False
    still_loop = True
    prepend = ""
    end_pend = ""

    if  "or" in c.lower():
        if is_rev:
            price_info["internal_revenue_code"] = c
            price_info["code"] = "NONE"
            write_data(price_info, writer, file, row)
        else:
            price_info["code"] = c
            write_data(price_info, writer, file, row)
    else:

        # Split by - to get min and max
        try:
            x, y = c.split("-")
        except ValueError:
            print("x,y split failed, too many values\n", row["code"])
            import sys; sys.exit()
        x, y = x.strip().strip(")"), y.strip().strip(")")
        # I feel that the last item in the range is more likely to have a semicolon
        y = y.strip(";")
        if x and y:
            # Check if the first character is a letter, so that I can add it back in later
            if x[0].strip().strip("-").isalpha() and y[0].strip().strip("-").isalpha():
                has_letter = True
                if x[0] == y[0]:
                    prepend = x[0]
                    # print("prepend:", prepend)
                    # Remove the first character to prevent errors
                    x2, y2 = x.strip()[1:], y.strip()[1:]

                else:
                    print("AAA")
                    print(x, y)
                    still_loop = False
                    price_info["code"] = c
                    write_data(price_info, writer, file, row)
            # Check last if last character is a letter, so that I can add it back in later
            if x[-1].strip().strip(";").isalpha() and y[-1].strip().strip(";").isalpha():
                has_letter = True
                if x[-1] == y[-1]:
                    end_pend = x[-1]
                    # print(end_pend)
                    x2, y2 = x.strip()[:-1], y.strip()[:-1]


                else:
                    print("BBB")
                    print(x, y)
                    print(x[-1], y[-1])
                    still_loop = False
                    price_info["code"] = c
                    write_data(price_info, writer, file, row)

                if still_loop:
                    if not has_letter:
                        print(x,y)
                        x2, y2 = x, y

                    if int(x2.strip()) + 1 == int(y2.strip()):
                        if still_loop:
                            # Naive way to check if x is a float
                            if "." in x and "." in y:
                                isfloat = True
                            else:
                                isfloat = False

                            # Floats are only ICD 9/10 codes afaict

                            try:
                                logging.debug("Non float loop")
                                # if int(y) >= 60000:
                                #     print(row["code"])
                                for codes in [x, y]:
                                    if is_rev:
                                        price_info["internal_revenue_code"] = str(codes).zfill(4)
                                        price_info["code"] = "NONE"
                                        write_data(price_info, writer, file, row)

                                    else:
                                        if has_letter:
                                            price_info["code"] = "".join([prepend, codes, end_pend])
                                        else:
                                            price_info["code"] = str(codes)
                                        write_data(price_info, writer, file, row)

                            except Exception as e:
                                print(e)
                                print(f"\nLine 192 failure: ({x}, {y})", c)
                                import sys; sys.exit(1)

        else:
            price_info["code"] = c
            write_data(price_info, writer, file, row)

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
    out_file = "F:\\hospital-price-transparency-v4\\extracted_data2.csv"
    if os.path.exists(out_file):
        os.remove(out_file)

    with open(out_file, "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        file = "HCA2.csv"
        parse_row(file, writer, columns)
