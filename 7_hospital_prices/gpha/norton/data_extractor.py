import csv
from tqdm import tqdm
import traceback as tb
import os

payer_dict = {
"Price": "GROSS CHARGE",
"De-Identified Minimum Outpatient Allowable Rate": "MIN",
"De-Identified Maximum Outpatient Allowable Rate": "MAX",
"Medicare Outpatient Allowable Rate": "Medicare"
}

# ,,,Price,,,,,Blue Cross Outpatient Allowable Rate,United Healthcare Outpatient Allowable Rate,Corizon Outpatient Allowable Rate,WPPA Outpatient Allowable Rate,Coventry Outpatient Allowable Rate
columns = ["cms_certification_num", "payer", "code", "internal_revenue_code", "description", "price", "inpatient_outpatient", "code_disambiguator", "units"]

for file in os.listdir("./"):
    if file.endswith(".csv"):
        with open(file, "r") as input_csv:
            line_count = len([line for line in input_csv.readlines()])
            input_csv.seek(0)
            header = input_csv.readline().split(",")
            insurance = header[(header.index("De-Identified Minimum Outpatient Allowable Rate")):-1]
            insurances = [x.replace("\n", "") for x in insurance]
            insurances.append("Price")
            input_csv.seek(0)
            reader = csv.DictReader(input_csv)

            with open("extracted_data.csv", "a", newline="") as output_csv:
                writer = csv.DictWriter(output_csv, fieldnames=columns)
                writer.writeheader()

                for row in tqdm(reader, total=line_count):
                    try:
                        price_info = {
                            "cms_certification_num": "171309",
                            "code": str(row["CPT_CODE"]).upper().strip(),
                            "internal_revenue_code": row["RevCode"].strip(),
                            "description": " ".join(str(row["ChargeDesc"]).split()).strip(),
                            "code_disambiguator": str(row["ChargeID"]).strip().strip()
                        }

                        inpatient_outpatient = [str(row["ChargeDesc"]).upper(), str(row["Department Description"]).upper()]
                        if "INPATIENT" in inpatient_outpatient:
                            price_info["inpatient_outpatient"] = "INPATIENT"
                        elif "OUTPATIENT" in inpatient_outpatient:
                            price_info["inpatient_outpatient"] = "OUTPATIENT"
                        elif "AMBULATORY" or "AMBULANCE" in inpatient_outpatient:
                            price_info["inpatient_outpatient"] = "OUTPATIENT"
                        else:
                            price_info["inpatient_outpatient"] = "UNSPECIFIED"

                        if not str(price_info["internal_revenue_code"]).strip():
                            price_info["internal_revenue_code"] = "NONE"

                        if not str(row["CPT_CODE"]):
                            price_info["code"] = "NONE"

                        #  ,,
                        for payer in insurances:
                            price_info["price"] = row[payer].replace("$", "").replace(",", "")
                            try:
                                price_info["payer"] = payer_dict[payer]
                            except KeyError:
                                price_info["payer"] = payer.split("Outpatient")[0].strip()

                            if str(price_info["price"]) and str(price_info["price"]) != "N/A":
                                if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                                    writer.writerow(price_info)
                                else:
                                    import json; print(json.dumps(price_info, indent=2))
                    except ValueError:
                        tb.print_exc()
