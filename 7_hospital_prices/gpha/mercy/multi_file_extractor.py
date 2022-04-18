import csv
from tqdm import tqdm
import traceback as tb
import os
from quantulum3 import parser


# MINIMUM_COMMERCIAL PRICE,
payers = {
    "CHARGEMASTER_PRICE": "GROSS CHARGE",
    "DISCOUNTED CASH PRICE": "CASH PRICE",
    "MINIMUM_COMMERCIAL PRICE": "MIN",
    "MAXIMUM_COMMERCIAL PRICE": "MAX"
}

columns = ["cms_certification_num", "code","description", "payer", "price", "inpatient_outpatient", "code_disambiguator", "units"]
with open(f"Mercy-Hospital_Standard-Charges_ALL.csv", "r", encoding='utf-8') as input_csv:
    line_count = len([line for line in input_csv.readlines()]) - 1
    input_csv.seek(0)
    header = input_csv.readline().split(",")
    insurance = header[(header.index("DISCOUNTED CASH PRICE")):-1]
    # print(insurance)
    insurances = [x.replace("\n", "") for x in insurance]
    insurances.append("CHARGEMASTER_PRICE")
    input_csv.seek(0)

    reader = csv.DictReader(input_csv)

    with open(f"extracted_data.csv", "a", newline="", encoding="utf-8") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                #
                price_info = {
                    "cms_certification_num": "170075",
                    "description": " ".join(str(row["CHARGE_DESCRIPTION"]).split()).replace("None", ""),
                    "code_disambiguator": "NONE"
                }

                code = str(row["MRKS_CPT"]).strip()
                hcpcs = str(row["MRKS_HCPCS"]).strip()
                drg = str(row["DRG_CODE"]).strip()
                ndc = str(row["NDC"]).strip()
                l = [x for x in [hcpcs, drg, ndc] if x.strip()]
                if code:
                    price_info["code"] = code
                    if l:
                        price_info["code_disambiguator"] = ",".join([x for x in l if x.strip()])

                elif l:
                    code_disambiguator = [x for x in l if x.strip()]
                    price_info["code"] = code_disambiguator[0]
                    if len(code_disambiguator) > 1:
                        price_info["code_disambiguator"] = ", ".join(code_disambiguator[1:])

                else:
                    price_info["code"] = "NONE"

                desc = price_info["description"]
                if " MG/ML" in desc:
                    desc = desc.split(" ")
                    # print(desc)
                    price_info["units"] = " ".join(desc[desc.index("MG/ML")-1:]).replace("[MRKS]", "")

                    cd = price_info["code_disambiguator"]
                    if not cd:
                        price_info["code_disambiguator"] = " ".join(desc[desc.index("MG/ML")-1:]).replace("[MRKS]", "")
                    else:
                        price_info["code_disambiguator"] = ", ".join([cd, " ".join(desc[desc.index("MG/ML")-1:])]).replace("[MRKS]", "")

                elif "MG/ML" in desc:
                    desc = desc.split(" ")
                    # print("\n", desc)
                    unit_index = [x for x, elem in enumerate(desc) if "MG/ML" in elem]
                    price_info["units"] = " ".join(desc[unit_index[0]:]).replace("[MRKS]", "").replace("[MKRS]", "").replace("MRKS]", "")
                    cd = price_info["code_disambiguator"]
                    if cd == "NONE":
                        price_info["code_disambiguator"] = " ".join(desc[unit_index[0]:]).replace("[MRKS]", "")
                    else:
                        price_info["code_disambiguator"] = ", ".join([cd, " ".join(desc[unit_index[0]:])]).replace("[MRKS]", "")
                else:
                    quants = parser.parse(desc)
                    quant = [x for x in quants if x.unit.entity.name=="mass" or x.unit.entity.name=="concentration" or x.unit.entity.name=="volume"]

                    if len(quant):
                        units = " ".join([(str(q.value) + str(q.unit.symbols[-1])) for q in quant if q.unit.symbols]) + " " + str(desc.split(" ")[-1]).replace("[MRKS]", "")
                        price_info["units"] = units

                        if price_info["code_disambiguator"] == "NONE":
                            price_info["code_disambiguator"] = units.replace("[MRKS]", "")
                        else:
                            price_info["code_disambiguator"] = ", ".join([price_info["code_disambiguator"], units.replace("[MRKS]", "")])

                activity_type = str(row["ACTIVITY_TYPE"]).upper()
                if "INPATIENT" in activity_type:
                    inpatient_outpatient = "INPATIENT"
                elif "AMBULATORY" in activity_type:
                    inpatient_outpatient = "OUTPATIENT"
                elif "OBSERVATION" in activity_type:
                    inpatient_outpatient = "OUTPATIENT"
                elif "SURGERY" in activity_type:
                    inpatient_outpatient = "OUTPATIENT"
                else:
                    inpatient_outpatient = "UNSPECIFIED"

                price_info["inpatient_outpatient"] = inpatient_outpatient

                for payer in insurances:
                    price_info["price"] = str(row[payer]).strip()

                    try:
                        price_info["payer"] = payers[payer]
                    except KeyError:
                        price_info["payer"] = str(payer).strip()

                    if not str(row[payer]).strip():
                        continue


                    if str(price_info["price"]).strip() and str(price_info["price"]) != "None":
                        if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                            # print("A")
                            writer.writerow(price_info)

            except ValueError:
                print(row)
                tb.print_exc()
                pass
