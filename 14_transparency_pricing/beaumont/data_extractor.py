import pandas as pd
import os
import datetime

def payer_category(payer_category):
    cats = {
        "GROSS CHARGE": "gross",
        "DE-IDENTIFIED  MINIMUM": "min",
        "DE-IDENTIFIED MAXIMUM": "max",
        "CASH PRICE": "cash"
    }

    try:
        return cats[payer_category]
    except KeyError:
        return "payer"


ccn_table = {
    "752379007": "100131",
    "BAY AREA": "520113",
    "BURLINGTON": "520059",
    "GRAFTON": "520207",
    "KENOSHA": "520189",
    "LAKELAND": "520102",
    "MANITOWOC": "520034",
    "OSHKOSH": "520198"

}
in_dir = ".\\input_files\\"
# for file in os.listdir(in_dir):
    # df = pd.read_excel(in_dir + file, dtype=object, header=1)
file = "2_381405141_beaumont-hospital-dearborn-hospital_standardcharges.csv"
df = pd.read_csv(file, encoding="iso-8859-1")
# df["hospital_ccn"] = ccn_table[file.split("_")[0]]

df = df.rename(columns={
    " Code Type": "code_meta",
    "Procedure ": "internal_code",
    "Code": "code",
    "Rev Code ": "rev_code",
    "Procedure Description": "procedure_desc",
    })


# Get the columns after `procedure_desc` (which are all payers)
cols = df.columns.tolist()
payers = cols[cols.index("procedure_desc")+1:]
id_vars = cols[:cols.index("procedure_desc")+1]

df_new = pd.melt(df, id_vars=id_vars, value_vars=payers)

df = df_new.rename(columns={
    "variable": "payer_desc",
     "value": "rate"
    }
)

df["code_type"] = df["code"].apply(lambda x: "ms-drg" if "MSDRG" in x else pd.NA)
df["ms_drg"] = df["code"].apply(lambda x: x.replace("MSDRG ", "") if "MSDRG" in x else pd.NA)


df["file_last_updated"] = "2023-01-01"
df["filename"] = file

df_obj = df.select_dtypes(['object'])
df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

df["code_meta"] = df["code_meta"].apply(str.lower)

df["payer_category"] = df["payer_desc"].apply(lambda x: payer_category(x))

print(df)
# df.to_csv("test.csv", index=False)