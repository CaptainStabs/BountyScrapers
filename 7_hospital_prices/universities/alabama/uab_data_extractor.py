import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import heartrate; heartrate.trace(browser=True, daemon=True)

cms_num = {
    "ceh2022": "010018",
    "uab2022": "010033"
}
#,,,,STANDARD CHARGE INPATIENT,STANDARD CHARGE OUTPATIENT,PAYER SPECIFIC RATE INPATIENT,PAYER SPECIFIC RATE OUTPATIENT,MINIMUM NEGOTIATED RATE INPATIENT,MINIMUM NEGOTIATED RATE OUTPATIENT,MAXIMUM NEGOTIATED RATE INPATIENT,MAXIMUM NEGOTIATED RATE OUTPATIENT,SELF PAY RATE INPATIENT,SELF PAY RATE OUTPATIENT,

def parse_row(writer, columns):
    with open(f"uab2022.csv", "r", encoding="utf-8") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)
        header = input_csv.readline().split(",")
        insurance = header[(header.index("STANDARD CHARGE INPATIENT")):-1]
        # print(insurance)
        insurances = [x.replace("\n", "") for x in insurance]
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                # PAYER NAME,,CDM Price,CPT /HCPCS/DRG Code,Rev Code
                for payer in insurances:
                    code = row["DRG / EAPG / CPT Code"]
                    price_info = {
                        "cms_certification_num": "010033",
                        "internal_revenue_code": row["REVENUE CODE"],
                        "description": " ".join(str(row["CHARGE ITEM OR SERVICE DESCRIPTION"]).split()).replace("None", ""),
                        "code": str(code).strip().replace("None", "NONE"),
                        # "payer": "GROSS CHARGE",
                        # "price": row["Gross Charge"],
                    }

                    if not str(row["DEPT"]) or str(row["DEPT"]) == "N/A":
                        price_info["internal_revenue_code"] = "NONE"
                    else:
                        price_info["internal_revenue_code"] = row["DEPT"]

                    if not str(price_info["internal_revenue_code"]):
                        price_info["internal_revenue_code"] = "NONE"


                    if not str(code).strip() or str(code) == "NA":
                        price_info["code"] = "NONE"

                    if "Inpatient" in payer:
                        price_info["inpatient_outpatient"] = "INPATIENT"
                    elif "Outpatient" in payer:
                        price_info["inpatient_outpatient"] = "OUTPATIENT"
                    else:
                        price_info["inpatient_outpatient"] = "UNSPECIFIED"

                    # ,Self Pay Rate
                    price_info["price"] = str(row[payer]).replace("$", "").replace("-","").replace(",","").strip()

                    if not str(price_info["price"]) or str(price_info["price"]) == "$-":
                        continue

                    if "STANDARD CHARGE" in payer:
                        price_info["payer"] = "GROSS CHARGE"

                    elif "PAYER SPECIFIC" in payer:
                        price_info["payer"] = str(row["PAYER NAME"]).strip()

                    elif "MINIMUM NEGOTIATED" in payer:
                        price_info["payer"] = " ".join([row["PAYER NAME"], "MIN"])

                    elif "MAXIMUM NEGOTIATED" in payer:
                        price_info["payer"] = " ".join([row["PAYER NAME"], "MAX"])

                    elif "SELF PAY RATE" in payer:
                        price_info["payer"] = "CASH PRICE"

                    else:
                        print(payer)
                        continue

                    if str(price_info["payer"]) != "Percent of Charge Payers":
                        if str(price_info["price"]) != "N/A" and str(price_info["price"]):
                            if str(price_info["price"]) and str(price_info["price"]) != "None":
                                if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                                    # print("A")
                                    writer.writerow(price_info)
                            else:
                                import json; print(json.dumps(row, indent=2))
                                break

            except ValueError:
                print(row)
                tb.print_exc()
                pass

if __name__ == "__main__":
    threads = []
    # "Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both(Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num", "code","description", "payer", "price", "inpatient_outpatient", "internal_revenue_code", "code_disambiguator"]
    with open(f"uab_extracted_data.csv", "a", newline="", encoding="utf-8") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        parse_row(writer, columns)
