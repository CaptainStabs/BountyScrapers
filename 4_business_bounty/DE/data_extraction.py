import json
import os
from tqdm import tqdm
import csv
from datetime import datetime

filename = "Delaware_Business_Licenses.csv"
output_file = "de_data.csv"
columns = ["name", "business_type", "state_registered", "state_physical", "street_physical", "city_physical", "zip5_physical", "filing_number"]

todays_date_string = "10/12/2021"
date_format = "%m/%d/%Y"
todays_date = datetime.strptime(todays_date_string, date_format)
print(todays_date)

with open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()
    total = 0
    for line in tqdm(lines):
        total += 1

    f.seek(0)

    input_fieldnames = ["business_name","trade_name","business_activity","current_license_valid_from","current_license_valid_to","address_1","address_2","city","state","zip","country","license_number", "geocoded_location"]
    reader = csv.DictReader(f, fieldnames=input_fieldnames)

    with open(output_file, "a", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=columns)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        for index, row in tqdm(enumerate(reader), total=total):
            if index == 0:
                continue

            business_info = {}
            license_expiration = datetime.strptime(row["current_license_valid_to"], date_format)

            if license_expiration > todays_date:
                business_info["name"] = row["trade_name"]

                business_type_string = row["trade_name"]

                if "COOPERATIVE" in business_type_string:
                    business_info["business_type"] = "COOP"
                    print("      [?] Translated type 1: COOP")

                if "COOP " in business_type_string:
                    business_info["business_type"] = "COOP"
                    print("      [?] Translated type 2: COOP")
                if "CORP" in business_type_string:
                    business_info["business_type"] = "CORPORATION"
                    print("      [?] Translated type 1: CORPORATION")

                if "CORP " in business_type_string:
                    business_info["business_type"] = "CORPORATION"
                    print("      [?] Translated type 2: CORPORATION")

                if "CORPORATION" in business_type_string:
                    business_info["business_type"] = "CORPORATION"
                    print("      [?] Translated type 3: CORPORATION")

                if "DBA" in business_type_string:
                    business_info["business_type"] = "DBA"
                    print("      [?] Translated type: DBA")

                if "LIMITED LIABILITY COMPANY" in business_type_string:
                    business_info["business_type"] = "LLC"
                    print("      [?] Translated type 1: LLC")

                if "LLC" in business_type_string:
                    business_info["business_type"] = "LLC"
                    print("      [?] Translated type 2: LLC")

                if "L.L.C." in business_type_string:
                    business_info["business_type"] = "LLC"
                    print("      [?] Translated type 3: LLC")

                if "L.L.C" in business_type_string:
                    business_info["business_type"] = "LLC"
                    print("      [?] Translated type 4: LLC")

                if "NON-PROFIT" in business_type_string:
                    business_info["business_type"] = "NONPROFIT"
                    print("      [?] Translated type 1: NON-PROFIT")

                if "NONPROFIT" in business_type_string:
                    business_info["business_type"] = "NONPROFIT"
                    print("      [?] Translated type 2: NONPROFIT")

                if "PARTNERSHIP" in business_type_string:
                    business_info["business_type"] = "PARTNERSHIP"
                    print("      [?] Translated type: PARTNERSHIP")

                if "SOLE PROPRIETORSHIP" in business_type_string:
                    business_info["business_type"] = "SOLE PROPRIETORSHIP"
                    print("      [?] Translated type: SOLE PROPRIETORSHIP")

                if "TRUST" in business_type_string:
                    business_info["business_type"] = "TRUST"
                    print("      [?] Translated type: TRUST")

                if "INC " in business_type_string:
                    business_info["business_type"] = "CORPORATION"
                    print("      [?] Translated type 1: INC")

                if "INC" in business_type_string:
                    business_info["business_type"] = "CORPORATION"
                    print("      [?] Translated type 2: INC")

                if "INCORPORATED" in business_type_string:
                    business_info["business_type"] = "CORPORATION"
                    print("      [?] Translated type 3: INC")

                # if "LIMITED" in business_type_string:
                #     business_info["business_type"] = "LTD"
                #     print("      [?] Translaetd type1: LTD")

                if "LTD" in business_type_string:
                    business_info["business_type"] = "LTD"
                    print("      [?] Translaetd type 2: LTD")

                if "L.T.D" in business_type_string:
                    business_info["business_type"] = "LTD"
                    print("      [?] Translaetd type 3: LTD")

                if not 
