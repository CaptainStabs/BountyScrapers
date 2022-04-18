import csv
from tqdm import tqdm
import traceback as tb
import os

payer_dict = {
"Gross Charge": "GROSS CHARGE",
"Discounted Cash Price": "CASH PRICE",
"De-identified minimum negotiated charge": "MIN",
"De-identified maximum negotiated charge": "MAX",
}

# Gross Charge,Discounted Cash Price,De-identified minimum negotiated charge,De-identified maximum negotiated charge,Blue_PPO,PROVIDRS_CARE_
columns = ["cms_certification_num", "payer", "code", "internal_revenue_code", "description", "price", "inpatient_outpatient", "code_disambiguator", "units"]

for file in os.listdir("./"):
    if file.endswith(".csv"):
        with open(file, "r") as input_csv:
            line_count = len([line for line in input_csv.readlines()])
            input_csv.seek(0)
            header = input_csv.readline().split(",")
            insurance = header[(header.index("Gross Charge")):-1]
            insurances = [x.replace("\n", "") for x in insurance]
            input_csv.seek(0)
            reader = csv.DictReader(input_csv)

            with open("extracted_data.csv", "a", newline="") as output_csv:
                writer = csv.DictWriter(output_csv, fieldnames=columns)
                writer.writeheader()

                for row in tqdm(reader, total=line_count):
                    try:
                        price_info = {
                            "cms_certification_num": "171300",
                            # "code": str(row["Procedure Code"]).upper(),
                            "internal_revenue_code": row["Revenue Code"],
                            # "description": " ".join(str(row["CPT"]).upper().split()),
                            "code_disambiguator": " ".join([str(row["Procedure Code"]).strip(), str(row["Procedure Description"]).strip()])
                        }

                        code = str(row["CPT HCPCS Code"]).strip()
                        ndc = str(row["NDC Code"]).strip()
                        code_disambiguator = str(price_info["code_disambiguator"]).strip()

                        if code and ndc:
                            price_info["code"] = code.strip()
                            price_info["code_disambiguator"] = " ".join([code_disambiguator, ndc]).strip()
                        elif code and not ndc:
                            price_info["code"] = code
                        elif ndc and not code:
                            price_info["code"] = ndc
                        else:
                            price_info["code"] = "NONE"

                        if str(row["CPT HCPCS Desc"]).strip():
                            price_info["description"] = str(row["CPT HCPCS Desc"]).strip()
                        elif str(row["Procedure Description"]).strip() and not str(row["CPT HCPCS Desc"]).strip():
                            price_info["description"] = str(row["Procedure Description"]).strip()

                        inpatient_outpatient = str(row["Price Tier"]).upper()
                        if "INPATIENT" in inpatient_outpatient and "OUTPATIENT" in inpatient_outpatient:
                            price_info["inpatient_outpatient"] = "BOTH"
                        elif "OUTPATIENT" in inpatient_outpatient and "INPATIENT" not in inpatient_outpatient:
                            price_info["inpatient_outpatient"] = "OUTPATIENT"
                        elif "INPATIENT" in inpatient_outpatient and "OUTPATIENT" not in inpatient_outpatient:
                            price_info["inpatient_outpatient"] = "INPATIENT"
                        elif "AMBULATORY" in inpatient_outpatient:
                            price_info["inpatient_outpatient"] = "OUTPATIENT"
                        else:
                            price_info["inpatient_outpatient"] = "UNSPECIFIED"

                        units = str(row["Rx Unit Multiplier"]).strip()
                        if units and units != "0" and units != "NA":
                            price_info["units"] = str(row["Rx Unit Multiplier"]).strip()

                        if not str(price_info["internal_revenue_code"]).strip():
                            price_info["internal_revenue_code"] = "NONE"

                        if len(price_info["description"]) >= 2048:
                            price_info["description"] = str(price_info["description"])[:2048]

                        #  ,,
                        for payer in insurances:
                            price_info["price"] = row[payer]
                            try:
                                price_info["payer"] = payer_dict[payer]
                            except KeyError:
                                price_info["payer"] = payer.strip()

                            if str(price_info["price"]) and str(price_info["price"]) != "N/A":
                                if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                                    writer.writerow(price_info)
                                else:
                                    import json; print(json.dumps(price_info, indent=2))
                    except ValueError:
                        tb.print_exc()
