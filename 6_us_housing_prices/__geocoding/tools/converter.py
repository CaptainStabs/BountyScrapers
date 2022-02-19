

with open("all_us_zipcodes.yaml", "r") as f:
    with open("us_zipcodes.yaml", "a") as fo:
        for line in f:
            if "- code: " in line:
                line = line.replace("- code: ", "").strip("\n") + ":\n"
            else:
                line = line

            fo.write(line)
