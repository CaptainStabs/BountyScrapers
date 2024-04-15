import pandas as pd
import os
import datetime


ccn_table = {
    "BAYCARE": "520193",
    "BAY AREA": "520113",
    "BURLINGTON": "520059",
    "GRAFTON": "520207",
    "KENOSHA": "520189",
    "LAKELAND": "520102",
    "MANITOWOC": "520034",
    "OSHKOSH": "520198"

}
for file in os.listdir(".\\input_files\\"):
    df = pd.read_excel(".\\input_files\\" + file, dtype=object, header=1)
    df["file_last_updated"] = datetime.datetime.strptime(df.columns[-1].replace("Fee", "").strip(), "%d/%m/%y")
    df["filename"] = file

    df["hospital_ccn"] = df["Facility"].apply(lambda x: ccn_table[x])
    df.drop(["Facility"], axis=1, inplace=True)

    

    df = df.rename(columns={
        "Chargecode": "internal_code",
        "CC Description": "procedure_description",
        "Rev": "rev_code",
        "CPT": "code",
        "1/1/23 Fee": "rate"
        },)

    df["url"] = "https://www.aurorahealthcare.org/assets/documents/billing-insurance/hospital-standard-charges/" + file
    df["code_type"] = "cpt"


    print(df.head(2))