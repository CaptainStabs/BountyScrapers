import pandas as pd
import os
import datetime
from tqdm import tqdm

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
    "dearborn": "230020",
    "farmington": "230020",
    "grosse": "230089",
    "royal": "230130",
    "taylor": "230270",
    "trenton": "230176",
    "troy": "230269",
    "wayne": "230142"

}
in_dir = ".\\input_files\\"
for file in tqdm(os.listdir(in_dir)):
    print(file)
    df = pd.read_csv(in_dir + file, na_values='#N/A', encoding="iso-8859-1", dtype={"Code": str}, low_memory=False)
    df = df.rename(columns={
        " Code Type": "code_meta",
        "Procedure ": "internal_code",
        "Code": "code",
        "Rev Code ": "rev_code",
        "Rev Code": "rev_code",
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

    df["code_type"] = df["code"].apply(lambda x: "ms-drg" if pd.notna(x) and "MSDRG" in x else pd.NA)
    df["ms_drg"] = df["code"].apply(lambda x: x.replace("MSDRG ", "") if pd.notna(x) and "MSDRG" in x else pd.NA)


    df["file_last_updated"] = "2023-01-01"
    df["filename"] = file
    df["url"] = "https://www.beaumont.org/docs/default-source/default-document-library/cdm-documents/2023/" + file
    df["hospital_ein"] = file.split("_")[0]

    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    df["rate"] = df["rate"].apply(lambda x: x.replace("$", "").strip() if (pd.notna(x) and "$" in x) else pd.NA)

    df["code_meta"] = df["code_meta"].apply(str.lower)

    df["payer_category"] = df["payer_desc"].apply(lambda x: payer_category(x))

    df["rev_code"] = df["rev_code"].fillna("nan")

    df["hospital_ccn"] = ccn_table[file.split("-")[2]]

    df.to_csv(".\\output_files\\" + file.split("-")[2] + ".csv", index=False)