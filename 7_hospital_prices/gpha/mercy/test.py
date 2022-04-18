import csv
from tqdm import tqdm
import traceback as tb
import os

columns = ["cms_certification_num", "code","description", "payer", "price", "inpatient_outpatient"]
with open(f"Mercy-Hospital_Standard-Charges_ALL.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()]) - 1
    input_csv.seek(0)

    reader = csv.DictReader(input_csv)

    for row in tqdm(reader, total=line_count):
        code = str(row["MRKS_CPT"]).strip()
        hcpcs = str(row["MRKS_HCPCS"]).strip()
        drg = str(row["DRG_CODE"]).strip()
        ndc = str(row["NDC"]).strip()

        if code and hcpcs and drg and ndc:
            print("A")

        if code:
            # l = [hcpcs, drg, ndc]
            l = [x for x in [hcpcs, drg, ndc] if x.strip()]
            if l:
                code_disambiguator = " ".join([x for x in l if x.strip()])
                print(code_disambiguator)
        else:
            l = [x for x in [hcpcs, drg, ndc] if x.strip()]
            if l:
                code_disambiguator = " ".join([x for x in l if x.strip()])
                print(code_disambiguator)

        # if code:
        #     if hcpcs and drg:
        #         print("A")
        #
        #     if  hcpcs and ndc:
        #         print("B")
        #
        #     if hcpcs and ndc and drg:
        #         print("C")
