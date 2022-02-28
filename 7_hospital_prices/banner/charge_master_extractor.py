import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from quantulum3 import parser
# import heartrate; heartrate.trace(browser=True, daemon=True)

cms_num = {
    "Banner Boswell": "030061",
    "Banner Del": "030093",
    "WR Churchill": "291313",
    "WR Fort": "060126"
}

def parse_row(in_directory, file, writer, columns):
    with open(f"{in_directory}{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)

        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                code_name = row["CDM CPT Code"]
                price_info = {
                    "cms_certification_num": cms_num[" ".join(file.split()[:2]).strip(".csv")],
                    # "internal_revenue_code": row["Charge # (Px Code)"],
                    "description": " ".join(str(row["Charge Description"]).split()).replace("None", ""),
                    "code": str(code_name).strip().replace("None", "NONE"),
                    "payer": "GROSS CHARGE",
                    "price": row["Price"]
                }

                code = str(price_info["code"])
                # internal_revenue_code = str(price_info["internal_revenue_code"])

                if not str(code_name).strip() or str(code_name) == "NA":
                    price_info["code"] = "NONE"

                desc = price_info["description"]
                if " MG/ML" in desc:
                    desc = desc.split(" ")
                    # print(desc)
                    price_info["units"] = " ".join(desc[desc.index("MG/ML")-1:])
                    price_info["code_disambiguator"] = " ".join(desc[desc.index("MG/ML")-1:])

                elif "MG/ML" in desc:
                    desc = desc.split(" ")
                    # print("\n", desc)
                    unit_index = [x for x, elem in enumerate(desc) if "MG/ML" in elem]
                    price_info["units"] = " ".join(desc[unit_index[0]:])
                    price_info["code_disambiguator"] = " ".join(desc[unit_index[0]:])
                else:
                    quants = parser.parse(desc)
                    quant = [x for x in quants if x.unit.entity.name=="mass" or x.unit.entity.name=="concentration" or x.unit.entity.name=="volume"]

                    if len(quant):
                        units = " ".join([(str(q.value) + str(q.unit.symbols[-1])) for q in quant if q.unit.symbols]) + " " + str(desc.split(" ")[-1])
                        price_info["units"] = units
                        price_info["code_disambiguator"] = units
                    else:
                        price_info["code_disambiguator"] = price_info["description"]
                try:
                    if not price_info["code_disambiguator"]:
                        price_info["code_disambiguator"] = "NONE"
                except KeyError:
                    price_info["code_disambiguator"] = "NONE"

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

    return file


if __name__ == "__main__":
    threads = []
    # "Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both(Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num", "code","description", "payer", "price", "units", "code_disambiguator"]
    in_directory = "./fixed/chargemaster/"
    with open(f"Charge_extracted_data.csv", "a", newline="", encoding="utf-8") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        with ThreadPoolExecutor(max_workers=4) as executor:
            for file in os.listdir(in_directory):
                if file.endswith(".csv"):
                    threads.append(executor.submit(parse_row(in_directory, file, writer, columns)))

                # for task in tqdm(as_completed(threads)):
                #     print(task.result())
