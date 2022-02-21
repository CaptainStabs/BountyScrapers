import csv
from tqdm import tqdm
import traceback as tb

# NDC Code,HCPCS,MEDICATION NAME,INPT PRICE,OUTPT PRICE
columns = ["cms_certification_num", "payer", "code", "description", "price", "inpatient_outpatient", "code_disambiguator"]
with open("Pharmacy-Services-11012021.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("pharm_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                if str(row["HCPCS"]):
                    price_info = {
                        "cms_certification_num": "010005",
                        "payer": "CASH PRICE",
                        "code": "HCPCS " + str(row["HCPCS"]).upper().strip(),
                        "description": " ".join(str(row["MEDICATION NAME"]).upper().split()),
                        "code_disambiguator": "NDC " + str(row["NDC Code"])
                    }

                if not str(row["HCPCS"]):
                    price_info = {
                        "cms_certification_num": "010005",
                        "payer": "CASH PRICE",
                        "code": "NDC " + str(row["NDC Code"]).upper().strip(),
                        "description": " ".join(str(row["MEDICATION NAME"]).upper().split()),
                        "code_disambiguator": "NDC " + str(row["NDC Code"])
                    }

                inpatient = row["INPT PRICE"].strip().replace("-", "")
                outpatient = row["OUTPT PRICE"].strip().replace("-", "")

                if not str(inpatient):
                    price_info["price"] = outpatient.replace(",", "")
                else:
                    price_info["price"] = inpatient.replace(",", "")

                if str(inpatient) and str(outpatient):
                    price_info["inpatient_outpatient"] = "BOTH"
                elif str(outpatient) and not str(inpatient):
                    price_info["inpatient_outpatient"] = "OUTPATIENT"
                elif str(inpatient) and not str(outpatient):
                    price_info["inpatient_outpatient"] = "INPATIENT"

                if str(price_info["price"]):
                    if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                        writer.writerow(price_info)
            except ValueError:
                tb.print_exc()
