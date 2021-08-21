import csv
import pandas as pd
import os

columns = ["name", "city", "state", "address", "district"]

def step_one():
    with open("districts_added.csv", "r", encoding="utf-8") as input_source:
        df = pd.read_csv(input_source)
        df_columns = list(df.columns)
        data_columns = ",".join(map(str, df_columns))

        with open("fix_districts.csv", "a", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=columns)
            if os.stat("fix_districts.csv").st_size == 0:
                writer.writeheader()

            for index, row in df.iterrows():

                district_input = row["district"]
                # Yes, this is terrible code, but I'm lazy
                changed = False
                if "DISTRICT" not in district_input:
                    if " DIST" in district_input:
                        print("DIST: " + str(district_input))
                        district = district_input.replace("DIST", "DISTRICT")
                        print("   [*] DIST: " + str(district))
                        changed = True

                if " ISD" in district_input:
                    print("ISD: " + str(district_input))
                    district = district_input.replace("ISD", "INDEPENDENT SCHOOL DISTRICT")
                    print("   [*] ISD: " + str(district))
                    changed = True

                if " SSD" in district_input:
                    print("SSD: " + str(district_input))
                    district = district_input.replace("SSD", "SPECIAL SCHOOL DISTRICT")
                    print("   [*] SSD: " + str(district))
                    changed = True

                if "PBLC SCHS" in district_input:
                    print("PBLC SCHS: " + str(district_input))
                    district = district_input.replace("PBLC SCHS", "PUBLIC SCHOOLS")
                    print("   [*] PBLC SCHS: " + str(district))
                    changed = True

                if " PCS" in district_input:
                    print("PCS: " + str(district_input))
                    district = district_input.replace("PCS", "PUBLIC CHARTER SCHOOLS")
                    print("   [*] PCS: " + str(district))
                    changed = True

                if " COOP" in district_input:
                    print("COOP: " + str(district_input))
                    district = district_input.replace("COOP", "COOPERATIVE")
                    print("   [*] COOP: " + str(district))
                    changed = True

                if " COOP." in district_input:
                    print("COOP. : " + str(district_input))
                    district = district_input.replace("COOP.", "COOPERATIVE")
                    print("   [*] COOP.: " + str(district))
                    changed = True

                if "SPEC ED" in district_input:
                    print("SPEC ED: " + str(district_input))
                    district = district_input.replace("SPEC ED", "SPECIAL EDUCATION")
                    print("   [*] SPEC ED: " + str(district))
                    changed = True

                if "CISD" in district_input:
                    print("CISD: " + str(district_input))
                    district = district_input.replace("CISD", "CONSOLIDATED INDEPENDENT SCHOOL DISTRICT")
                    print("   [*] CISD: " + str(district))
                    changed = True

                if " CUSD" in district_input:
                    print("CUSD: " + str(district_input))
                    district = district_input.replace("CUSD", "CONSOLIDATED UNIT SCHOOL DISTRICT")
                    print("   [*] CUSD: " + str(district))
                    changed = True

                if "CORP" in district_input:
                    print("CORP: " + str(district_input))
                    district  = district_input.replace("CORP", "CORPORATION")
                    print("   [*] CORP: " + str(district))
                    changed = True

                if not changed:
                    district = district_input



                school_info = {}
                school_info["name"] = row["name"].upper()
                school_info["city"] = row["city"].upper()
                school_info["state"] = row["state"].upper()
                school_info["district"] = district.upper()
                writer.writerow(school_info)

def step_two():
    with open("fix_districts.csv", "r", encoding="utf-8") as input_source:
        df = pd.read_csv(input_source)
        df_columns = list(df.columns)
        data_columns = ",".join(map(str, df_columns))

        with open("fix_districts2.csv", "a", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=columns)
            if os.stat("fix_districts2.csv").st_size == 0:
                writer.writeheader()

            for index, row in df.iterrows():
                district_input = row["district"]
                if "DISTRICTRICT" in district_input:
                    district = district_input.replace("DISTRICTRICT", "DISTRICT")

                elif "DISTRICTRICT" in district_input:
                    district = district_input.replace("DISTRICTRICT", "DISTRICT")

                else:
                    district = district_input.upper()

                school_info = {}
                school_info["name"] = row["name"].upper()
                school_info["city"] = row["city"].upper()
                school_info["state"] = row["state"].upper()
                school_info["district"] = district_input.upper()
                writer.writerow(school_info)

step_one()
# step_two()
