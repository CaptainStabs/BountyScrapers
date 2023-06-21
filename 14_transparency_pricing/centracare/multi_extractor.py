import pandas as pd
import re
import os
from tqdm import tqdm



def fix_decimal_precision(value):
    try:
        if not pd.isna(value):
            if re.match(r'^\d+\.\d+$', value):
                return "{:.3f}".format(float(value))
            else:
                return value
        else:
            return value
    except TypeError:
        print(value)


folder = '.\\input_files\\'
# file = '411924645_centracare-long-prairie-hospital_standardcharges.csv'

for file in tqdm(os.listdir(folder)):
        
    df = pd.read_csv(folder + file, dtype=str, skiprows=1)


    df.rename(columns={
        'Procedure': 'local_code',
        'Code Type': 'line_type',
        'Code': 'code',
        'NDC': 'ndc',
        'Rev Code': 'rev_code',
        'Procedure Description': 'description',
        'Quantity': 'drug_quantity',
    }, inplace=True)


    df['line_type'] = df['line_type'].str.lower()


    cols = df.columns.tolist()
    id_vars = cols[:7]
    value_vars = cols[7:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')

    df.loc[df['standard_charge'].str.strip() == 'N/A', 'standard_charge'] = pd.NA
    df.dropna(subset='standard_charge', inplace=True)


    df['rev_code'] = df['rev_code'].str.split(' -').str[0]


    mask = (~df['code'].isna()) & (df['code'].str.startswith('CPT®'))
    df.loc[mask, 'hcpcs_cpt'] = df['code'].str.replace('CPT® ', '')


    mask = (~df['code'].isna()) & (df['code'].str.startswith('HCPCS'))
    df.loc[mask, 'hcpcs_cpt'] = df['code'].str.replace('HCPCS ', '')


    mask = (~df['code'].isna()) & (df['code'].str.startswith('MS-DRG'))
    df.loc[mask, 'ms_drg'] = df['code'].str.replace('MS-DRG V39 (FY 2022) ', '')


    mask = (~df['code'].isna()) & (df['line_type'] == 'apr-drg' )
    df.loc[mask, 'apr_drg'] = df['code'].str.zfill(3)


    df.loc[df['drug_quantity'] == '1', 'drug_quantity'] = pd.NA


    payer_mapping = {
        'Charge': 'gross',
        'Max': 'max',
        'Min': 'min',
        'Discounted Cash Price': 'cash'
    }

    df['payer_category'] = df['payer_name'].map(payer_mapping).fillna('payer')


    mask = ~(df['hcpcs_cpt'].astype(str).str.match(r'^[A-Z][0-9]{4}$|^[0-9]{5}$|^[0-9]{4}[A-Z]$'))
    df.loc[mask, 'hcpcs_cpt'] = pd.NA
    df.loc[df['apr_drg'].str.len() > 3, 'apr_drg'] = df['apr_drg'][:3] + '-' + df['apr_drg'][3:]


    df['local_code'] = df['local_code'].apply(fix_decimal_precision)


    hosp_id_mapping = {
    '384089454_centracare-redwood-hospital_standardcharges.csv': '241351',
    '463298651_centracare-paynesville-hospital_standardcharges.csv': '241349',
    '461584944_centracare-monticello-hospital_standardcharges.csv': '241362',
    '411924645_centracare-long-prairie-hospital_standardcharges.csv': '241326',
    '411865315_centracare-melrose-hospital_standardcharges.csv': '241330',
    '452438973_centracare-sauk-centre-hospital_standardcharges.csv': '241368',
    '823166379_centracare-rice-memorial-hospital_standardcharges.csv': '240088',
    '410695596_centracare-st-cloud-hospital_standardcharges.csv': '240036'}

    hosp_id = hosp_id_mapping[file]

    df['hospital_id'] = hosp_id

    out_file = hosp_id + '_' + file.split('_')[1] + '.csv'
    out_folder = '.\\output_files\\'

    df.to_csv(out_folder + out_file, index=False)
