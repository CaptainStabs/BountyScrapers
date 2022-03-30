import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# import heartrate; heartrate.trace(browser=True, daemon=True)
# "Procedure"|"Code Type"|"Revenue Code"|"Procedure Description"|"Quantity"|"Payer"|"Plan"|"Inpatient Gross Charges"|"Inpatient Expected Reimbursement"|"Inpatient Max Reimbursement"|"Inpatient Minimal Reimbursement"|"Outpatient Gross Charges"|"Outpatient Expected Reimbursement"|"Outpatient Max Reimbursement"|"Outpatient Minimal Reimbursement"
# "Procedure"|"Code Type"|"Revenue Code"|"Procedure Description"|"Quantity"|"Payer"|"Plan"|"Inpatient Gross Charges"|"Inpatient Expected Reimbursement"|"Inpatient Max Reimbursement"|"Inpatient Minimal Reimbursement"|"Outpatient Gross Charges"|"Outpatient Expected Reimbursement"|"Outpatient Max Reimbursement"|"Outpatient Minimal Reimbursement"

cms_num = {
    "BAILEYMEDICALCENTER": "370228",
    "BSAHOSPITAL": "450231",
    "HILLCRESTHOSPITALCLAREMORE": "370039",
    "HILLCRESTHOSPITALCUSHING": "370099",
    "HILLCRESTHOSPITALHENRYETTA": "370183",
    "HILLCRESTHOSPITALPRYOR": "370015",
    "HILLCRESTHOSPITALSOUTH": "370202",
    "HILLCRESTMEDICALCENTER": "370001",
    "LOVELACEMEDICALCENTER": "320009",
    "LOVELACEREHABILITATIONHOSPITAL": "323028",
    "LOVELACEWESTSIDEHOSPITAL": "320074",
    "LOVELACEWOMENSHOSPITAL": "320017",
    "ROSWELLREGIONALHOSPITAL": "320086",
    "SETONMEDICALCENTER": "670080",
    "TULSASPINEANDSPECIALTY": "370216",
    "UKHST.FRANCISMEDICALCENTER": "170016",
    "UTHEALTHATHENSHOSPITAL": "450389",
    "UTHEALTHCARTHAGEHOSPITAL": "420210",
    "UTHEALTHHENDERSONHOSPITAL": "450475",
    "UTHEALTHJACKSONVILLEHOSPITAL": "450194",
    "UTHEALTHNORTHHOSPITAL": "450690",
    "UTHEALTHPITTSBURGHOSPITAL": "451367",
    "UTHEALTHQUITMANHOSPITAL": "451380",
    "UTHEALTHREHABHOSPITALL": "453072",
    "UTHEALTHSPECIALTYHOSPITAL": "452051",
    "UTHEALTHTYLERHOSPITAL": "450083"
}

payers = {
    "Inpatient Gross Charges": "INPATIENT",
    "Inpatient Max Reimbursement": "INPATIENT",
    "Inpatient Minimal Reimbursement": "INPATIENT",
    "Inpatient Expected Reimbursement": "INPATIENT",
    "Outpatient Gross Charges": "OUTPATIENT",
    "Outpatient Expected Reimbursement": "OUTPATIENT",
    "Outpatient Max Reimbursement": "OUTPATIENT",
    "Outpatient Minimal Reimbursement": "OUTPATIENT"
}

def parse_row(in_directory, file, writer, columns):
    with open(f"{in_directory}{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()]) - 1
        input_csv.seek(0)
        header = input_csv.readline().split("|")
        insurance = header[(header.index('"Inpatient Gross Charges"')):-1]
        # print(insurance)
        insurances = [x.replace("\n", "").replace('"', "") for x in insurance]
        input_csv.seek(0)

        reader = csv.DictReader(input_csv, delimiter="|")

        for row in tqdm(reader, total=line_count):
            try:
                description = " ".join(str(row["Procedure Description"]).split()).replace("None", "")
                price_info = {
                    "cms_certification_num": cms_num[(file.split("_")[1]).upper()],
                    "internal_revenue_code": row["Revenue Code"],
                    "description": description,
                    "code": "NONE",
                    "code_disambiguator": " ".join([row["Procedure"].strip(), row["Quantity"].strip()]),#, row["Code Type"].strip()]), #description]),
                    "units": row["Quantity"].strip(),
                    # "payer": "GROSS CHARGE",
                    # "price": row["Gross Charge"],
                    # "inpatient_outpatient": str(row["Hospital Inpatient / Outpatient / Both"]).upper().strip().replace("None", "UNSPECIFIED")
                }

                if not str(row["Revenue Code"]):
                    price_info["internal_revenue_code"] = "NONE"

                for payer in insurances:
                    try:
                        price_info["inpatient_outpatient"] = payers[payer]
                    except KeyError:
                        print(payer)
                        price_info["inpatient_outpatient"] = "UNSPECIFIED"


                        # print(payer)
                    # else:
                    #     price_info["inpatient_outpatient"] = "UNSPECIFIED"


                    price = row[payer].replace(",","")
                    if not str(price).strip():
                        continue

                    # |"Inpatient Expected Reimbursement"|"Inpatient Max Reimbursement"|"Inpatient Minimal Reimbursement
                    price_info["price"] = price
                    if "Gross Charges" in payer:
                        price_info["payer"] = "GROSS CHARGE"

                    elif "Expected Reimbursement" in payer:
                        price_info["payer"] = " ".join([row["Payer"].strip(), row["Plan"].strip()])

                    elif " Max " in payer:
                        price_info["payer"] = "MAX"

                    elif "Minimal" in payer:
                        price_info["payer"] = "MIN"

                    else:
                        print("AAA")
                        # price_info["payer"] = " ".join([row["Plan"].strip(), payer.strip()])

                    if price_info["inpatient_outpatient"] == "INPATIENT":
                        print("A")

                    if str(price_info["price"]) and str(price_info["price"]) != "None":
                        if str(price_info["payer"]) and float(price_info["price"]) <= 10000000:
                            # print("A")
                            writer.writerow(price_info)
                    else:
                        print(file)
                        import json; print(json.dumps(row, indent=2))
                        # break

            except ValueError:
                print(row)
                tb.print_exc()
                pass

if __name__ == "__main__":
    threads = []
    # "Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both(Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num", "code","description", "payer", "price", "inpatient_outpatient", "code_disambiguator", "internal_revenue_code", "units"]
    in_directory = "./fixed/"
    with open(f"extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        for file in tqdm(os.listdir(in_directory)):
            if file.endswith(".txt"):
                print(file)
                parse_row(in_directory, file, writer, columns)
        # with ThreadPoolExecutor(max_workers=1) as executor:
        #     for file in tqdm(os.listdir(in_directory)):
        #         if file.endswith(".txt"):
        #             print(file)
        #             threads.append(executor.submit(parse_row, in_directory, file, writer, columns))
        #
        #     for task in tqdm(as_completed(threads)):
        #         print(task.result())
