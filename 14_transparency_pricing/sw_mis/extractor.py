# %%
import pandas as pd
import numpy as np
import os

# %%
def payer_category(payer):
    if 'GrossCharge' in payer:
        return 'gross'
    elif 'DiscountedCashPrice' in payer or 'SELFPAY' in payer:
        return 'cash'
    elif 'Minimun'in payer:
        return'min'
    elif 'Maximun' in payer:
        return'max'
    else:
        return 'payer'

def patient_class(payer):
    if 'Inpatient' in payer or '_IPPS' in payer:
        return 'inpatient'
    elif 'Outpatient' in payer or '_OPPS' in payer:
        return 'outpatient'
    elif 'Emergency' in payer:
        return 'emergency'
    
def rate_desc(payer):
    if 'PercentOfCharges' in payer:
        return 'PercentOfCharges'
    elif 'TieredFeeSchedule' in payer:
        return 'TieredFeeSchedule'

# %%
# file = '640468873_southwestmississippiregionalmedicalcenter_standardcharges.csv'
folder = '.\\input_files\\'
for file in os.listdir(folder):
    df = pd.read_csv(folder + file, dtype={'MSDRG': str, 'NDC': str})

    # %%
    # Skip first 3 rows
    df = df[3:]

    # %%
    df = df.rename(columns={
        'ProcedureCode': 'code',
        'Modifier': 'modifier',
        'RevenueCode': 'rev_code',
        'Description': 'description'
    })

    # %%
    # Merge column `MSDRG` and `code`
    df.loc[df['code'].notna(), 'code_prefix'] = 'hcpcs_cpt'
    df['code'] = df['code'].fillna(df['MSDRG'])
    # This is fine because any null code prefix will either be ms-drg 
    # or have a null `code` and will thus be dropped.
    df['code_prefix'] = df['code_prefix'].fillna('ms-drg')
    df.drop(columns=['MSDRG', 'RecordType', 'FileInformation'], inplace=True)

    # %%
    # Bring added columns to the beginning to make the next step easier (reorder)
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    # %%
    cols = df.columns.tolist()
    split_index = cols.index('InpatientGrossCharge')

    id_vars = cols[:split_index]
    value_vars =  cols[split_index:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_orig', value_name='rate')

    # %%
    df.dropna(subset=['rate', 'code'], inplace=True)

    # %%
    df['payer_category'] = df['payer_orig'].apply(payer_category)
    df['patient_class'] = df['payer_orig'].apply(patient_class)
    df['rate_desc'] = df['payer_orig'].apply(rate_desc)

    # %%
    # Update rate_desc based on conditions
    df.loc[(df["payer_category"] == "gross") & (df["code_prefix"] == "ms-drg"), "rate_desc"] = "averaged rate"
    
    # Drop rows where code is ms-drg and patient is outpatient per discussion with SL
    df = df[~((df['patient_class'] == 'outpatient') & (df['code_prefix'] == 'ms-drg'))]

    # I could just drop this but figure it might change in the future so best to just set na
    df['modifier'] = df['modifier'].fillna('na')
    df['rev_code'] = df['rev_code'].fillna('na')
    df['patient_class'] = df['patient_class'].fillna('na')
    # %%
    df['file_last_updated'] = '2023-02-01'
    df['url'] = 'https://pricetransparency.blob.core.windows.net/smrmc/' + file
    df['filename'] = file

    ein = file.split("_")[0]
    ein = ein[:2] + "-" + ein[2:]
    df['hospital_ein'] = ein

    name = file.split("_")[1]

    ccns = {'lawrencecountyhospital': '250063',
            'southwestmississippiregionalmedicalcenter': '250097'}
    df['hospital_ccn'] = ccns[name]
    df['payer_name'] = df['payer_orig']
    df['code_orig'] = df['code']

    df.to_csv('.\\output_files\\' + name + '.csv', index=False)


