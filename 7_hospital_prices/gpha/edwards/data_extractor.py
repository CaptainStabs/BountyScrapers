import csv
from tqdm import tqdm
import traceback as tb

payers = {
" Hospital Price ":"GROSS CHARGE",
" Discounted Cash Price ":"CASH PRICE",
" De-Identified Minimum Negotiated rate ":"MIN",
" De-Identified Maximum Negotiated rate ":"MAX",
" Aetna and Coventry (Inpatient) ": "Aetna and Coventry",
" Aetna and Coventry (Outpatient) ": "Aetna and Coventry",
" BCBS KS  ": "BCBS KS",
" Health Partners of Kansas (Cigna and Humana Commerical product plans) - Inpatient ":"Health Partners of Kansas (Cigna and Humana Commerical product plans)",
" Health Partners of Kansas (Cigna and Humana Commerical product plans) - Outpatient ":"Health Partners of Kansas (Cigna and Humana Commerical product plans)",
" WPPA/ProviDrs Care - Inpatient ": "WPPA/ProviDrs Care",
" WPPA/ProviDrs Care - Outpatient ":"WPPA/ProviDrs Care",
" Tricare/HealthNet Federal Health Services ":"Tricare/HealthNet Federal Health Services",
" VA CCN (Optum)  ": "VA CCN (Optum)",
" United HealthCare ": "United HealthCare",
'UHC Community, Aetna Better Health, Sunflower (Medicaid)': "UHC Community, Aetna Better Health, Sunflower (Medicaid)",
"Medicare Advanatge Plans":"Medicare Advanatge Plans",
"Work Comp":"Work Comp"
}

columns = ["cms_certification_num", "payer", "code", "internal_revenue_code", "description", "price", "inpatient_outpatient", "code_disambiguator"]
with open("4510882_Edwards-County-Medical-Center_standardcharges.csv", "r", encoding="utf-8") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    header = input_csv.readline().split(",")
    insurance = header[(header.index(" Hospital Price ")):-1]
    # print(insurance)
    insurances = [x.replace("\n", "") for x in insurance]
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("extracted_data.csv", "a", newline="", encoding="utf-8") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                price_info = {
                    "cms_certification_num": "171317",
                    "code": str(row["CPT/HCPCS Codes"]),
                    "internal_revenue_code": row["Revenue Code"].strip(),
                    "description": " ".join(str(row["Description"]).split()).strip(),
                    "code_disambiguator": row["Line Item Number"]
                }

                if not str(price_info["code"]):
                    price_info["code"] = "NONE"

                if not str(row["Line Item Number"]):
                    price_info["code_disambiguator"] = "NONE"

                if not str(row["Revenue Code"]):
                    price_info["internal_revenue_code"] = "NONE"


                for payer in insurances:
                    if " Aetna Better Health" in payer or "Sunflower (Medicaid)" in payer:
                        continue

                    if "UHC Community" in payer:
                        payer = "UHC Community, Aetna Better Health, Sunflower (Medicaid)"
                    price_info["price"] = row[payer].replace("$", "").replace(",", "").replace("-", "").strip()

                    if 'UHC Community' not in payer:
                        price_info["payer"] = payers[payer]
                    else:
                        price_info["payer"] = "UHC Community, Aetna Better Health, Sunflower (Medicaid)"

                    inpatient_outpatient = str(payer).upper()
                    if "INPATIENT" in inpatient_outpatient:
                        price_info["inpatient_outpatient"] = "INPATIENT"
                    elif "OUTPATIENT" in inpatient_outpatient:
                        price_info["inpatient_outpatient"] = "OUTPATIENT"
                    else:
                        price_info["inpatient_outpatient"] = "UNSPECIFIED"


                    try:
                        if "N/A" not in str(row[payer]) and str(row[payer]).strip():
                            if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                                writer.writerow(price_info)
                            else:
                                import json; print(json.dumps(price_info, indent=2))
                    except ValueError:
                        pass
            except ValueError:
                tb.print_exc()
                # pass
