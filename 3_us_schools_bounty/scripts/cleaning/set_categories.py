import csv
import pandas as pd
import os

columns = ["name","city","state","address","category"]

df = pd.read_csv("category_list.csv")
df_columns = list(df.columns)
data_columns = ",".join(map(str, df_columns))

with open("categories_added.csv", "a") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)
    if os.stat("categories_added.csv").st_size == 0:
        writer.writeheader()

    for index, row in df.iterrows():
        school_info = {}
        name = row["name"]
        changed = False

        if pd.isnull(row["category"]):

            if "ELEMENTARY" in str(name):
                school_info["category"] = "ELEMENTARY"
                changed = True

            if "PRESCHOOL" in str(name):
                school_info["category"] = "PRESCHOOL"
                changed = True

            if "PRESCHOOL" and "KINDERGARTEN" in str(name):
                school_info["category"] = "PRESCHOOOL & KINDERGARTEN"
                changed = True

            if "MIDDLESCHOOL" or "MIDDLE SCHOOL" in str(name):
                print("Matched MIDDLESCHOOL: " + str(name))
                school_info["category"] = "MIDDLE"
                changed = True

            if "ELEMENTARYMIDDLE" in str(name):
                school_info["category"] = "ELEMENTARY & MIDDLE"
                changed = True

            if "HIGH SCHOOL" in str(name):
                school_info["category"] = "HIGH"
                changed = True

            if "PRE-K" in str(name):
                school_info["category"] = "PREKINDERGARTEN"

            if " HS " in str(name):
                print("HS: " + str(name))
                school_info["category"] = "HIGH"
                changed = True

            if "JUNIOR HIGH" in str(name):
                print("Matched JUNIOR HIGH: " + str(name))
                school_info["category"] = "MIDDLE"
                changed = True

            if "VOCATIONAL" or " VOC " in str(name):
                school_info["category"] = "VOCATIONAL SCHOOL"
                changed = True

            if "ADULT" in str(name):
                school_info["category"] = "ADULT EDUCATION"
                changed = True

            if "PRIMARY" in str(name):
                school_info["category"] = "ELEMENTARY"
                changed = True

            if "JH" or "JHS" in str(name):
                print("Matched JH: " + str(name))
                school_info["category"] = "MIDDLE"
                changed = True

            if "ELEM " or "ELEM. " or " ELEM " or "ELEM " or " ELEM." or " ELEM. " in str(name):
                school_info["category"] = "ELEMENTRAY"
                changed = True

            if " EL " or "EL " or "EL. " or " EL. " or " EL. " in str(name):
                school_info["category"] = "ELEMENTARY"
                changed = True

            if " MS " or " MS" in str(name):
                print("Matched MS: " + str(name))
                school_info["category"] = "MIDDLE"
                changed = True

            if " K-12" in str(name):
                school_info["category"] = "K-12"
                changed = True

            if "PK-12" in str(name):
                school_info["category"] = "PK-12"
                changed = True

            if changed:
                school_info["name"] = row["name"]
                school_info["city"] = row["city"]
                school_info["state"] = row["state"]
                school_info["address"] = row["address"]
                writer.writerow(school_info)
