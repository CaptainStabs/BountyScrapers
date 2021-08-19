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
                if " ISD" in district_input:
                    print("ISD: " + str(district_input))
                    district = district_input.replace("ISD", "INDEPENDENT SCHOOL DISTRICT")
                    print("   [*] ISD: " + str(district))

                elif " SSD" in district_input:
                    print("SSD: " + str(district_input))
                    district = district_input.replace("SSD", "SPECIAL SCHOOL DISTRICT")
                    print("   [*] SSD: " + str(district))

                elif "PBLC SCHS" in district_input:
                    print("PBLC SCHS: " + str(district_input))
                    district = district_input.replace("PBLC SCHS", "PUBLIC SCHOOLS")
                    print("   [*] PBLC SCHS: " + str(district))

                elif " PCS" in district_input:
                    print("PCS: " + str(district_input))
                    district = district_input.replace("PCS", "PUBLIC CHARTER SCHOOLS")
                    print("   [*] PCS: " + str(district))

                elif " DIST" in district_input:
                    print("DIST: " + str(district_input))
                    district = district_input.replace("DIST", "DISTRICT")
                    print("   [*] DIST: " + str(district))

                elif " COOP" in district_input:
                    print("COOP: " + str(district_input))
                    district = district_input.replace("COOP", "COOPERATIVE")
                    print("   [*] COOP: " + str(district))

                elif " COOP." in district_input:
                    print("COOP. : " + str(district_input))
                    district = district_input.replace("COOP.", "COOPERATIVE")
                    print("   [*] COOP.: " + str(district))

                elif "SPEC ED" in district_input:
                    print("SPEC ED: " + str(district_input))
                    district = district_input.replace("SPEC ED", "SPECIAL EDUCATION")
                    print("   [*] SPEC ED: " + str(district))

                elif "CISD" in district_input:
                    print("CISD: " + str(district_input))
                    district = district_input.replace("CISD", "CONSOLIDATED INDEPENDENT SCHOOL DISTRICT")
                    print("   [*] CISD: " + str(district))

                elif " CUSD" in district_input:
                    print("CUSD: " + str(district_input))
                    district = district_input.replace("CUSD", "CONSOLIDATED UNIT SCHOOL DISTRICT")
                    print("   [*] CUSD: " + str(district))

                elif "CORP" in district_input:
                    print("CORP: " + str(district_input))
                    district  = district_input.replace("CORP", "CORPORATION")
                    print("   [*] CORP: " + str(district))

                else:
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
