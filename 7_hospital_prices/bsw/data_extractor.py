import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# import heartrate; heartrate.trace(browser=True, daemon=True)

cms_num = {
    "Baylor University Medical Center": "450021",
    "Brenham": "450187", # This
    "Buda": "670131",
    "Centennial": "450885",
    "College Station": "670088",
    "Denton": "450893",
    "Fort Worth": "450137",
    "Grapevine": "450563",
    "Heart and Vascular Hospital": "450851",
    "Heart Plano": "670025",
    "Hillcrest": "450101",
    "Irving": "450079",
    "Lake Pointe": "450742",
    "Marble Falls": "670108",
    "McKinney":"670082",
    "Plano": "450890",
    "Round Rock": "670034", # This
    "Taylor": "451374",
    "Temple": "452105", # This
    "Waxahachie": "450372"
}

def parse_row(in_directory, file, writer, columns):
    with open(f"{in_directory}{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)
        header = input_csv.readline().split(",")
        insurance = header[(header.index("Gross Charge")):-1]
        insurances = [x.replace("\n", "") for x in insurance]
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                code = row["CPT / HCPCS Code"]
                if code == "N/A":
                    if row["NDC"] != "N/A":
                        code = row["NDC"]
                    elif row["APR-DRG"] != "N/A":
                        code = row["APR-DRG"]
                    elif row["DRG"] != "N/A":
                        code = row["DRG"]

                    elif row["NDC"] == "N/A" and row["APR-DRG"] == "N/A" and row["DRG"] == "N/A":
                        code = "NONE"

                # Default Rev Code,CPT / HCPCS Code,
                price_info = {
                    "cms_certification_num": cms_num[file[:-4]],
                    "internal_revenue_code": row["Default Rev Code"].replace("N/A", "NONE"),
                    "description": " ".join(str(row["Procedure Name"]).split()).replace("N/A", ""),
                    "code": str(code).strip().replace("N/A", "NONE"),
                    # "payer": "GROSS CHARGE",
                    # "price": row["Gross Charge"],
                    "inpatient_outpatient": str(row["Patient Type"]).upper().strip().replace("N/A", "UNSPECIFIED")
                }

                code = str(price_info["code"])
                internal_revenue_code = str(price_info["internal_revenue_code"])

                for payer in insurances:
                    bad_prices = ["**", "N/A", "-"]
                    price_info["price"] = row[payer].replace("$", "").replace(",", "")
                    if str(row[payer]).strip() in bad_prices:
                        continue

                    if "Discounted" in payer:
                        price_info["payer"] = "CASH PRICE"

                    elif payer == "Gross Charge":
                        price_info["payer"] = "GROSS CHARGE"

                    elif payer == "De-Identified Minimum Reimbursement*":
                        price_info["payer"] = "MIN"

                    elif payer == "De-Identified Maximum Reimbursement*":
                        price_info["payer"] = "MAX"
                    else:
                        price_info["payer"] = payer.strip()

                    if not price_info["code"] or price_info["code"] == "NONE":
                        price_info["code"] = "NONE"

                    if price_info["description"]:
                        price_info["code_disambiguator"] = price_info["description"] + " " + str(price_info["price"])
                    else:
                        price_info["code_disambiguator"] = str(price_info["price"])


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
    columns = ["cms_certification_num", "internal_revenue_code", "code", "description", "payer", "price", "inpatient_outpatient", "code_disambiguator"]
    in_directory = "./fixed/"
    with open(f"extracted_data.csv", "a", newline="", encoding="utf-8") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        # with ThreadPoolExecutor(max_workers=20) as executor:
        #     for file in os.listdir(in_directory):
        #         if file.endswith(".csv"):
        #             threads.append(executor.submit(parse_row, in_directory, file, writer, columns))

        for file in os.listdir(in_directory):
            if file.endswith(".csv"):
                parse_row(in_directory, file, writer, columns)
