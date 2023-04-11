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
    
def code_type(x):
    if pd.notna(x):
        if "MSDRG" in x:
            return "ms-drg"
        elif len(x) == 5:
            return "hcpcs_cpt"

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
    df = pd.read_csv(in_dir + file, na_values='#N/A', encoding="iso-8859-1", dtype={"Code": str, 'Rev Code': str, 'Rev Code ': str}, low_memory=False)
    df = df.rename(columns={
        " Code Type": "code_meta",
        "Procedure ": "procedure_code",
        "Code": "code",
        "Rev Code ": "rev_code",
        "Rev Code": "rev_code",
        "Procedure Description": "description",
        " NDC ": "ndc"
        })

    # Get the columns after `description` (which are all payers)
    cols = df.columns.tolist()
    payers = cols[cols.index("description")+1:]
    id_vars = cols[:cols.index("description")+1]

    # Melt payers into new rows
    df = pd.melt(df, id_vars=id_vars, value_vars=payers, var_name='payer_orig', value_name='rate')

    df = df.dropna(subset=['rate'])

    # Get code types and explode into separate columns
    df["code_type"] = df["code"].apply(code_type)
    # df["ms_drg"] = df["code"].str.replace("MSDRG ", "").where(df["code"].str.contains("MSDRG"), pd.NA)
    # df["hcpcs_cpt"] = df["code"].where(df["code"].str.len() == 5, pd.NA)
    # df = df[~df["code"].isin(["SURG", "MANUL"]) & ~df["hcpcs_cpt"].isin(["SURG", "MANUL"])]
    df = df[~df["code"].isin(["SURG", "MANUL"])]

    # Remove dollar sign and strip rate
    df['code_orig'] = df['code']
    df["code"] = df["code"].str.replace('MSDRG ', '')
    df['rate'] = df['rate'].str.replace(',', '').str.replace('$','').str.strip() # col is not object so is not stripped below
    df = df[(df['rate'] != '-') & (df['rate'] != '#VALUE!')]

    df = df.dropna(subset=['code', 'code_type', 'rate'])


    df["file_last_updated"] = "2023-01-01"
    df["filename"] = file
    df["url"] = "https://www.beaumont.org/docs/default-source/default-document-library/cdm-documents/2023/" + file

    # Strip all objects
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())


    df["code_meta"] = df["code_meta"].str.lower()

    df["payer_category"] = df["payer_orig"].apply(payer_category)

    # df["rev_code"] = df["rev_code"].str.rstrip(".")
    df["rev_code"] = df["rev_code"].fillna("na")
    df['ndc'] = df['ndc'].fillna('na')

    tin = file.split("_")[0]
    tin = tin[:2] + "-" + tin[2:]
    df['hospital_tin'] = tin
    df["hospital_ccn"] = ccn_table[file.split("-")[2]]

    df.to_csv(".\\output_files\\" + file.split("-")[2] + ".csv", index=False)