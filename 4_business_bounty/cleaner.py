import csv
import pandas as pd
import os
from tqdm import tqdm

columns = ["name", "business_type", "state_registered", "street_registered","city_registered","zip5_registered"]

df = pd.read_csv("fincen.csv")
df_columns = list(df.columns)
data_columns = ",".join(map(str, df_columns))

line_count = 0
with open("fincen.csv", "r") as f:
    for line in f:
        line_count += 1

with open("fincen_cleaned.csv", "a", encoding="utf8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)
    if os.stat("fincen_cleaned.csv").st_size == 0:
        writer.writeheader()

    with open("fincen_dirty.csv", "a", encoding="utf8") as dirty_file:
        dirty_writer = csv.DictWriter(dirty_file, fieldnames=columns)

        if os.stat("fincen_dirty.csv").st_size == 0:
            dirty_writer.writeheader()

        for index, row in tqdm(df.iterrows(), total=line_count):
            business_info = {}
            if "COOPERATIVE" in str(row["name"]).upper():
                business_info["business_type"] = "COOP"
                print("      [?] Translated type 1: COOP")

            if "COOP " in str(row["name"]).upper():
                business_info["business_type"] = "COOP"
                print("      [?] Translated type 2: COOP")

            if "CORP" in str(row["name"]).upper():
                business_info["business_type"] = "CORPORATION"
                print("      [?] Translated type 1: CORPORATION")

            if "CORP " in str(row["name"]).upper():
                business_info["business_type"] = "CORPORATION"
                print("      [?] Translated type 2: CORPORATION")

            if "CORPORATION" in str(row["name"]).upper():
                business_info["business_type"] = "CORPORATION"
                print("      [?] Translated type 3: CORPORATION")

            if "DBA" in str(row["name"]).upper():
                business_info["business_type"] = "DBA"
                print("      [?] Translated type: DBA")

            if "LIMITED LIABILITY COMPANY" in str(row["name"]).upper():
                business_info["business_type"] = "LLC"
                print("      [?] Translated type 1: LLC")

            if "LLC" in str(row["name"]).upper():
                business_info["business_type"] = "LLC"
                print("      [?] Translated type 2: LLC")

            if "L.L.C." in str(row["name"]).upper():
                business_info["business_type"] = "LLC"
                print("      [?] Translated type 3: LLC")

            if "L.L.C" in str(row["name"]).upper():
                business_info["business_type"] = "LLC"
                print("      [?] Translated type 4: LLC")


            if "NON-PROFIT" in str(row["name"]).upper():
                business_info["business_type"] = "NONPROFIT"
                print("      [?] Translated type 1: NON-PROFIT")

            if "NONPROFIT" in str(row["name"]).upper():
                business_info["business_type"] = "NONPROFIT"
                print("      [?] Translated type 2: NONPROFIT")

            if "PARTNERSHIP" in str(row["name"]).upper():
                business_info["business_type"] = "PARTNERSHIP"
                print("      [?] Translated type: PARTNERSHIP")

            if "SOLE PROPRIETORSHIP" in str(row["name"]).upper():
                business_info["business_type"] = "SOLE PROPRIETORSHIP"
                print("      [?] Translated type: SOLE PROPRIETORSHIP")

            if "TRUST" in str(row["name"]).upper():
                business_info["business_type"] = "TRUST"
                print("      [?] Translated type: TRUST")

            if "INC " in str(row["name"]).upper():
                business_info["business_type"] = "CORPORATION"
                print("      [?] Translated type: INC")

            if "INC" in str(row["name"]).upper():
                business_info["business_type"] = "CORPORATION"
                print("      [?] Translated type: INC")

            if "INCORPORATED" in str(row["name"]).upper():
                business_info["business_type"] = "CORPORATION"
                print("      [?] Translated type: INC")

            if "LIMITED" in str(row["name"]).upper():
                business_info["business_type"] = "LTD"
                print("      [?] Translaetd type: LTD")

            if "LTD" in str(row["name"]).upper():
                    business_info["business_type"] = "LTD"
                    print("      [?] Translaetd type: LTD")
            try:
                business_info["business_type"]
                no_type = False
            except KeyError:
                no_type = True
            if not no_type:
                business_info["name"] = str(row["name"]).upper().strip()
                business_info["state_registered"] = str(row["state_registered"]).upper().strip()
                business_info["street_registered"] = str(row["street_address"]).upper().strip()
                business_info["city_registered"] = str(row["city_registered"]).upper().strip()
                business_info["zip5_registered"] = str(row["zip5_registered"]).replace("'","").strip()
                writer.writerow(business_info)
            else:
                business_info["name"] = str(row["name"]).upper()
                business_info["state_registered"] = str(row["state_registered"]).upper()
                business_info["street_registered"] = str(row["street_address"]).upper()
                business_info["city_registered"] = str(row["city_registered"]).upper()
                business_info["zip5_registered"] = row["zip5_registered"]
                dirty_writer.writerow(business_info)
