import csv
from tqdm import tqdm
import traceback as tb
import os

payer_dict = {
"De-Identified Minimum Inpatient Allowable Rate Per Day or Total": "MIN",
"De-Identified Maximum Inpatient Allowable Rate Per Day or Total": "MAX",
"De-identified minimum negotiated charge": "MIN",
"De-identified maximum negotiated charge": "MAX",
}


columns = ["cms_certification_num", "payer", "code", "description", "price", "inpatient_outpatient"]
# ,,,,Medicare Inpatient Allowable Rate Per Day,Blue Cross Inpatient Allowable Rate,United Healthcare Inpatient Allowable Rate,Cigna Inpatient Allowable Rate,Aetna Inpatient Allowable Rate,WPPA Inc Inpatient Allowable Rate Per Day
with open("KCH_Online_CDM_Posting_Final_2022.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    header = input_csv.readline().split(",")
    insurance = header[(header.index("Average Total Charges")):]
    insurances = [x.replace("\n", "") for x in insurance]
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("cdm_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                price_info = {
                    "cms_certification_num": "171313",
                    # "code": str(row["DRG Code"]).upper(),
                    "description": " ".join(str(row["DRG Description"]).upper().split()),
                    "inpatient_outpatient": "INPATIENT"
                }

                code = str(row["DRG Code"]).strip()

                if code:
                    price_info["code"] = code.strip()
                else:
                    price_info["code"] = "NONE"

                for payer in insurances:
                    price_info["price"] = row[payer].replace("$", "").replace(",", "").replace("-", "")
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
