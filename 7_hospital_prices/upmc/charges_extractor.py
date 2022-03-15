import csv
from tqdm import tqdm
import traceback as tb
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
# import heartrate; heartrate.trace(browser=True, daemon=True)

cms_num = {
    "UPMC Altoona Hospital": "390073",
    "UPMC Bedford Hospital": "390117",
    "UPMC Chautauqua Hospital": "330239",
    "UPMC Childrens Hospital": "393302",
    "UPMC East Hospital": "390328",
    "UPMC Hamot Hospital": "390063",
    "UPMC Horizon Hospital": "390178",
    "UPMC Jameson Hospital": "390016",
    "UPMC Lockhaven": "390071",
    "UPMC Lock Haven Hospital": "390071",
    "UPMC Magee Womens Hospital": "390114",
    "UPMC McKeesport Hospital": "390002",
    "UPMC Mercy Hospital": "390028",
    "UPMC Muncy Valley Hospital": "391301",
    "UPMC Northwest Hospital": "390091",
    "UPMC Passavant Hospital": "390107",
    "UPMC Presbyterian Shadyside Hospital": "390164",
    "UPMC St. Margaret Hospital": "390102",
    "UPMC Wellsboro Hospital": "391316",
    "UPMC Williamsport Hospital":"390045",
    "UPMC CARLISLE": "390058",
    "UPMC Cole": "391313",
    "UPMC HANOVER": "390233",
    "UPMC Kane ": "390104",
    "UPMC LITITZ": "390068",
    "UPMC MEMORIAL": "390101",
    "UPMC PINNACLE HARRISBURG ": "390067"

}

def parse_row(in_directory, file, writer, columns):
    with open(f"{in_directory}{file}", "r") as input_csv:
        line_count = len([line for line in input_csv.readlines()])
        input_csv.seek(0)
        reader = csv.DictReader(input_csv)

        for row in tqdm(reader, total=line_count):
            try:
                price_info = {
                    "cms_certification_num": cms_num[row["Hospital"]],
                    "description": " ".join(str(row["Description"]).split()).replace("None", ""),
                    "payer": "GROSS CHARGE",
                    "price": row["Standard Charge"].replace(",", "").replace("$", ""),
                    "code_disambiguator": " ".join(str(row["Description"]).split()).replace("None", ""),
                }


                if str(price_info["price"]).upper().strip() != "VARIABLE":
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
            except KeyError:
                print(file)
                raise KeyError

if __name__ == "__main__":
    threads = []
    # "Charge # (Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both(Px Code)",Procedure Name,Procedure Code (CPT / HCPCS),Default Modifier,Gross Charge,Discounted Cash Charge,Hospital Inpatient / Outpatient / Both
    columns = ["cms_certification_num", "description", "payer", "price", "code_disambiguator"]
    in_directory = "./input_files/converted/charge/"
    with open(f"charges_extracted_data.csv", "a", newline="") as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=columns)
        writer.writeheader()
        with ThreadPoolExecutor(max_workers=1) as executor:
            for file in os.listdir(in_directory):
                if file.endswith(".csv"):
                    # threads.append(executor.submit(parse_row, in_directory, file, writer, columns))
                    parse_row(in_directory, file, writer, columns)
