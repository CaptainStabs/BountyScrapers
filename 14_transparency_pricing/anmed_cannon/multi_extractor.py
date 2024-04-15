import pandas as pd
import os
# import linecache
import datetime
from datetime import datetime as dt
import numpy as np
from tqdm import tqdm

def payer_category(payer):
    payers = {
        "Deidentified Minimum": 'min',
        'Deidentified Maximum': 'max'
    }

    try:
        return payers[payer]
    except KeyError:
        return 'payer'


file = 'Standard Charges_AnMed Cannon_2023.xlsx'
tin = '57-0342027'
ccn = '420011'
date_updated = '2023-01-01'

for actual_file in tqdm(os.listdir('input_files')):
    print(actual_file)
    df = pd.read_csv('.\\input_files\\' + actual_file, skiprows=4)
    
    df.rename(columns = {
    'ContractName': 'payer_name',
    'CodeType': 'code_type',
    'Code': 'code',
    'Description': 'description',
    'Service Description': 'rev_desc',
    'Base Rate Methodology': 'rev_method',
    'ServiceCode': 'patient_class',
    'Negotiated Charge / Base Rate': 'rate',
    'Negotiated Charge / Base Rate*': 'rate'
    }, inplace = True)

    df['code_orig'] = df['code']
    df['code_type'] = df['code_type'].str.lower()
    df['patient_class'] = df['patient_class'].str.replace('IP', 'inpatient',).str.replace('OP', 'outpatient')
    # Set rev_code equal to code and set code_type to None if code_type equals revenuecode
    df.loc[df["code_type"] == "revenuecode", "rev_code"] = df["code"]

    df1 = df.drop(['payer_name', 'rate'], axis=1)
    cols = df1.columns.tolist()
    value_vars = ['Deidentified Minimum', 'Deidentified Maximum']
    id_vars = [x for x in cols if x not in value_vars]

    df1 = pd.melt(df1, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='rate')


    df.drop(value_vars, axis=1, inplace=True)

    df_cols = df.columns.values.tolist()
    df_cols.sort()

    df  = df[df_cols]
    df1 = df1[df_cols]

    df3 = df.append(df1)
    df = df3

    df['rate'] = df['rate'].str.replace('$', '', regex=False).str.replace(',', '', regex=False)
    df = df[~df['rate'].str.contains('%')]


    df['payer_orig'] = df['payer_name']
    df.loc[df["code_type"] == "revenuecode", ["code", "code_type"]] = [None, None]

    # Set code_prefix based on code_type value using numpy.where
    df["code_prefix"] = np.where(df["code_type"] == "cpt", "hcpcs_cpt",
                                np.where(df["code_type"] == "drg", "apr-drg", None))
    df.loc[df["code"].str.contains("MS-"), "code_prefix"] = "ms-drg"
    # Strip "MS-" from code column
    df['code'] = df["code"].str.replace("MS-", "")
    print(df.columns)


    df['code'] = np.where(df['code_prefix'] == 'apr-drg', df['code'].str[:3] + '-' + df['code'].str[3:], df['code'])
    # Add constants
    df['hospital_ein'] = tin
    df['hospital_ccn'] = ccn
    df['filename'] = file
    df['url'] = 'https://anmed.org/sites/default/files/2023-01/Standard%20Charges_AnMed%20Cannon_2023.xlsx'
    df['apc'] = df['rev_desc'].apply(lambda x: str(x).replace('APC ', '') if 'APC' in str(x) else None)

    df['rev_code'] = df['rev_code'].fillna('na')
    df['payer_category'] = df['payer_name'].apply(payer_category)
    df['file_last_updated'] = date_updated
    df.to_csv("./output_files/" + actual_file, index=False)