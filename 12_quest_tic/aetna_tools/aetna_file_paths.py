import re 

pat = re.compile(r'(?:"filePath": )"(.*?)"')

with open("response.json", "r") as f:
    f = f.read()

    r = re.findall(pat, f)

with open("aetna_indexes.txt", "a") as f:
    for line in r:
        if "inNetworkRates" in line:
            f.write(f"{line}\n")