import numpy as np
import re

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

# code = "93563-,0408T-0415T, 0543T-0545T, 0569T-0570T, 0613T, f33017-f33019"
code = "10.01-10.09,11-14"
is_rev = False
if "," in code:
    for c in code.split(","):
        c = c.strip("-").strip()
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

            if isfloat:
                step = int(y.split(".")[-1].strip()) - int(x.split(".")[-1].strip())
                for codes in np.linspace(parse_str(x),parse_str(y), num=step):
                    if is_rev:
                        # price_info["internal_revenue_code"] = str(codes)
                        # price_info["code"] = "NONE"
                        print(str(codes))
                    else:
                        # price_info["code"] = str(codes).zfill(3).strip(";")
                        print("{:.2f}".format(codes))

                    if prepend or end_pend:
                        print("".join([prepend, str(codes), end_pend]))
            else:
                for codes in np.arange(parse_str(x),parse_str(y)):
                        if is_rev:
                            # price_info["internal_revenue_code"] = str(codes)
                            # price_info["code"] = "NONE"
                            print(str(codes))
                        else:
                            # price_info["code"] = str(codes).zfill(3).strip(";")
                            print(str(codes).zfill(3).strip(";"))

                        if prepend or end_pend:
                            print("".join([prepend, str(codes), end_pend]))
