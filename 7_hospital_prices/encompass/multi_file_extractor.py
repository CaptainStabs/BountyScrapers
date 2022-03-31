import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from re import sub
from decimal import Decimal
import decimal
# import heartrate; heartrate.trace(browser=True, daemon=True)

payers = {
    "GROSS_CHARGE": "GROSS CHARGE",
    "DISCOUNTED_CASH_PRICE": "CASH PRICE",
    "DEIDENTIFIED_MIN_NEGOTIATED_CHARGE": "MIN",
    "DEIDENTIFIED_MAX_NEGOTIATED_CHARGE": "MAX"
}

bad_prices = ["Note 2", "NO"]
def parse_row(in_directory, file, writer, columns):
    with open(f"{in_directory}{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()]) - 1
        input_csv.seek(0)
        # header = input_csv.readline().split(",")
        # insurance = header[(header.index("GROSS_CHARGE")):-1]
        # print(insurance)

        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            header = list(row.keys())
            insurance = header[(header.index("GROSS_CHARGE")):]
            insurances = [x.replace("\n", "") for x in insurance]
            try:
                price_info = {
                    "cms_certification_num": file[:-4],
                    "internal_revenue_code": row["BILLING_REVENUE_SERVICE_CODE"],
                    "description": " ".join(str(row["ITEM_SERVICE_PACKAGE"]).split()).replace("None", "")[:2048],
                    "code": "NONE",
                    "code_disambiguator": "NONE"
                }

                internal_revenue_code = str(price_info["internal_revenue_code"])
                multi_rev = False

                if internal_revenue_code == "250":
                    price_info["code_disambiguator"] = price_info["description"][:2048]
                elif internal_revenue_code == "118; 120; 128; 138; 148; 158":
                    price_info["code_disambiguator"] = price_info["description"][:2048]
                    multi_rev = True

                pat_type = row["PATIENT_TYPE"].upper()
                if "INPATIENT" and "OUTPATIENT" in pat_type:
                    price_info["inpatient_outpatient"] = "BOTH"
                elif "INPATIENT" and not "OUTPATIENT" in pat_type:
                    price_info["inpatient_outpatient"] = "INPATIENT"
                elif "OUTPATIENT" and not "INPATIENT" in pat_type:
                    price_info["inpatient_outpatient"] = "OUTPATIENT"
                else:
                    price_info["inpatient_outpatient"] = "UNSPECIFIED"


                if not multi_rev:
                    for payer in insurances:
                        if "NO" in row[payer]:
                            continue

                        try:
                            price_info["price"] =   Decimal(sub(r'[^\d.]', '', row[payer]))
                        except decimal.InvalidOperation:
                            # print(row[payer])
                            continue

                        try:
                            price_info["payer"] = payers[payer]
                        except KeyError:
                            price_info["payer"] = payer.replace(" negotiated charge", "").strip()


                        if str(price_info["price"]) and str(price_info["price"]) != "None":
                            if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                                # print("A")
                                writer.writerow(price_info)
                        else:
                            print(file)
                            import json; print(json.dumps(row, indent=2))
                            break
                else:
                    for rev_code in internal_revenue_code.split("; "):
                        price_info["internal_revenue_code"] = rev_code
                        price_info["code_disambiguator"] = price_info["description"]

                        for payer in insurances:
                            if "NO" in row[payer]:
                                continue

                            try:
                                price_info["price"] =   Decimal(sub(r'[^\d.]', '', row[payer]))
                            except decimal.InvalidOperation:
                                # print(row[payer])
                                continue

                            try:
                                price_info["payer"] = payers[payer]
                            except KeyError:
                                price_info["payer"] = payer.replace(" negotiated charge", "").strip()


                            if str(price_info["price"]) and str(price_info["price"]) != "None":
                                if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                                    # print("A")
                                    writer.writerow(price_info)
                            else:
                                print(file)
                                import json; print(json.dumps(row, indent=2))
                                break


            except ValueError:
                print(row)
                tb.print_exc()
                pass

if __name__ == "__main__":
    threads = []
    # "Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both(Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num", "code","description", "internal_revenue_code", "payer", "price", "inpatient_outpatient", "code_disambiguator"]
    in_directory = "./output_files/"
    with open(f"F:/hospital-price-transparency-v4/2hospital_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        # with ThreadPoolExecutor(max_workers=5) as executor:
        #     for file in os.listdir(in_directory):
        #         if file.endswith(".csv"):
        #             threads.append(executor.submit(parse_row, in_directory, file, writer, columns))
        #
        #     for task in tqdm(as_completed(threads), total=124):
        #         a = "A"
        #
        for file in tqdm(os.listdir(in_directory)):
            if file.endswith(".csv"):
                parse_row(in_directory, file, writer, columns)
