import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# import heartrate; heartrate.trace(browser=True, daemon=True)

# code,code type,code description,payer,patient_class,
def parse_row(in_directory, file, writer, columns):
    with open(f"{in_directory}{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)
        header = input_csv.readline().split(",")
        insurance = header[(header.index("gross charge")):-1]
        # print(insurance)
        insurances = [x.replace("\n", "") for x in insurance]
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                code = row["code"]
                price_info = {
                    "cms_certification_num": file.replace(".csv", ""),
                    "description": " ".join(str(row["code description"]).split()).replace("None", ""),
                    # "code": str(code).strip().replace("None", "NONE"),
                    # "payer": "GROSS CHARGE",
                    # "price": row["Gross Charge"],
                    "code_disambiguator": " ".join(str(row["code description"]).split()).replace("None", ""),
                }

                if not str(price_info["code_disambiguator"]):
                    price_info["code_disambiguator"] = "NONE"

                if row["code type"] == "cpt":
                    price_info["code"] = str(row["code"]).strip()
                    price_info["internal_revenue_code"] = "NONE"
                elif row["code type"] == "revCode":
                    price_info["internal_revenue_code"] = str(row["code"]).strip()
                    price_info["code"] = "NONE"

                elif row["code type"] == "ms-drg":
                    price_info["code"] = str(row["code"]).strip()
                    price_info["internal_revenue_code"] = "NONE"

                if str(row["patient_class"]).upper() == "O":
                    price_info["inpatient_outpatient"] = "OUTPATIENT"
                elif str(row["patient_class"]).upper() == "I":
                    price_info["inpatient_outpatient"] = "INPATIENT"
                else:
                    price_info["inpatient_outpatient"] = "UNSPECIFIED"

                for payer in insurances:
                    # gross charge,de-identified minimum negotiated charge,de-identified maximum negotiated charge,payer-specific negotiated charge,discounted cash price
                    price_info["price"] = row[payer]
                    if payer == "payer-specific negotiated charge":
                        price_info["payer"] = str(row["payer"]).strip()

                    elif payer == "de-identified minimum negotiated charge":
                        price_info["payer"] = "MIN"

                    elif payer == "de-identified maximum negotiated charge":
                        price_info["payer"] = "MAX"

                    elif payer == "gross charge":
                        price_info["payer"] = "GROSS CHARGE"

                    elif payer == "discounted cash price":
                        price_info["payer"] = "CASH PRICE"
                    else:
                        print("payer:", payer)

                    if str(price_info["price"]).upper().strip() == "NONE":
                        continue

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
    # # code,code type,code description,payer,patient_class,
    columns = ["cms_certification_num", "code","description", "payer", "price", "inpatient_outpatient", "internal_revenue_code", "code_disambiguator"]
    in_directory = "./input_files/"
    with open(f"extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        with ThreadPoolExecutor(max_workers=11) as executor:
            for file in os.listdir(in_directory):
                if file.endswith(".csv"):
                    # threads.append(executor.submit(parse_row, in_directory, file, writer, columns))
                    parse_row(in_directory, file, writer, columns)
