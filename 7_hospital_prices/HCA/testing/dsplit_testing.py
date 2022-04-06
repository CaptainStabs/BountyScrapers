import re

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

price_info = {}
c = "G0630-G0638"

is_rev = False
still_loop = True
prepend = ""
end_pend = ""

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
    if x[0].isalpha() and y[0].isalpha():
        if x[0] == y[0]:
            prepend = x[0]
            print("prepend", prepend)
            # Remove the first character to prevent errors
            x, y = x.strip()[1:], y.strip()[1:]
            if x[0] == "0":
                # Preserve any and all padding
                padding = len(x)
        else:
            print("AAA")
            print(x[0], y[0])
            still_loop = False
            # write_data(price_info, writer, file, row)
    # Check last if last character is a letter, so that I can add it back in later
    if x[-1].strip().strip(";").isalpha() and y[-1].strip().strip(";").isalpha():
        if x[-1] == y[-1]:
            end_pend = x[-1]
            print(end_pend)
            x, y = x.strip()[:-1], y.strip()[:-1]

            if x[0] == "0":
                padding = len(x)
        else:
            print("BBB")
            print(x, y)
            print(x[-1], y[-1])
            still_loop = False
            # write_data(price_info, writer, file, row)

    if still_loop:
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

                    # write_data(price_info, writer, file, row)
            else:
                if str(y2[-1].strip()):
                    price_info["code"] = y.strip()
                    print("y2")
                    # write_data(price_info, writer, file, row)
                elif str(x2[-1].strip()):
                    price_info["code"] = x.strip()
                    print("x2")
                    # write_data(price_info, writer, file, row)
                else:
                    print("\nMissing an x or y for", c)
        else:
            try:
                for codes in range(parse_str(x, c),parse_str(y, c) + 1):
                    if is_rev:
                        price_info["internal_revenue_code"] = str(codes).zfill(4)
                        price_info["code"] = "NONE"

                    else:
                        # Only need this here because it is within the generator
                        if len(str(x)) == 3 and len(str(y)) == 3:
                            price_info["code"] = str(codes).zfill(3).strip(";")
                            print(str(codes).zfill(3).strip(";"))

                        else:
                            price_info["code"] = "".join([prepend, str(codes).zfill(padding), end_pend])
                            print("".join([prepend, str(codes).zfill(padding), end_pend]))
                        # print(str(codes).zfill(3).strip(";"))
            except Exception as e:
                print(e)
                print(f"\nLine 192 failure: ({x}, {y})", c)
                import sys; sys.exit(1)
else:
    print("\nx or y is null: ", ",".join([x,y]), row["code"])
