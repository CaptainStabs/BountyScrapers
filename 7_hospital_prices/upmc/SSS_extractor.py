import csv
from tqdm import tqdm
import traceback as tb
import heartrate; heartrate.trace(browser=True, daemon=True)


columns = ["cms_certification_num", "code", "payer", "description", "price", "code_disambiguator", "internal_revenue_code"]
with open("./input_files/converted/73-1678377_Select_Specialty_Hospital-Pittsburgh-UPMC_standardcharges.csv", "r") as input_csv:
    line_count = len([line for line in input_csv.readlines()])
    input_csv.seek(0)
    reader = csv.DictReader(input_csv)

    with open("sss_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()

        for row in tqdm(reader, total=line_count):
            try:
                price_info = {
                    "cms_certification_num": "210027",
                    "payer": "GROSS CHARGE",
                    "description": " ".join(str(row["CHARGE_DESCRIPTION"]).upper().split()),
                    "price": row["CHARGE"],
                    "code_disambiguator": row["CHARGE_CODE"],
                    "internal_revenue_code": row["REVENUE_CODE"]
                }

                save_twice = False
                if str(row["CPT_CODE"]).strip():
                    if "/" in str(row["CPT_CODE"]).strip():
                        code_list = str(row["CPT_CODE"]).strip().split("/")
                        price_info["code"] = code_list[0]
                        save_twice = True
                    else:
                        price_info["code"] = row["CPT_CODE"]

                elif str(row["PHARMACY_NDC"]).strip():
                    price_info["code"] = row["PHARMACY_NDC"]
                else:
                    price_info["code"] = "NONE"

                if not price_info["internal_revenue_code"]:
                    price_info["internal_revenue_code"] = "NONE"

                if save_twice:
                    if str(price_info["price"]).strip() != "" and float(price_info["price"]) <= 10000000:
                        for codes in code_list:
                            price_info["code"] = codes
                            writer.writerow(price_info)

                else:
                    if str(price_info["price"]).strip() != "" and float(price_info["price"]) <= 10000000:
                        writer.writerow(price_info)
                # else:
                #     import json; print(json.dumps(price_info, indent=2))
            except ValueError:
                tb.print_exc()
