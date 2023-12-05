import pandas as pd
import json
import os
from tqdm import tqdm


folder = '.\\input_files\\'
# file = '37-0960170-northwestern-memorial-hospital-standard-charges.json'

for file in tqdm(os.listdir(folder)):
    with open(folder + file, 'r', encoding='utf-8-sig') as f:
        jd = json.load(f)
        jd = jd[list(jd.keys())[0]]


    df = pd.DataFrame(jd, dtype=str)


    df.rename(columns={
        'Billing_Code': 'code',
        'Service_Description': 'description',
        'Revenue_Code': 'rev_code',
    }, inplace=True)


    df.loc[~df['rev_code'].isna(),'rev_code'] = df['rev_code'].str.split('.').str[0].str.zfill(4)


    cols = df.columns.tolist()
    id_vars = cols[:3]
    val_vars = cols[3:]

    df = pd.melt(df, id_vars=id_vars, value_vars=val_vars, var_name='payer_name', value_name='standard_charge')

    df['code'] = df['code'].str.strip()
    df.loc[df['code'].str.startswith('CPT®'), 'hcpcs_cpt'] = df['code'].str.split('CPT® ').str[1]
    df.loc[df['code'].str.startswith('HCPCS'), 'hcpcs_cpt'] = df['code'].str.split('HCPCS ').str[1]
    # df.loc[df['code'].str.startswith('MS-DRG V40 (FY 2023)'), 'ms_drg'] = df['code'].str.split('MS-DRG V40 (FY 2023) ').str[1]
    df['ms_drg'] = df['code'].str.extract(r'MS-DRG V40 \(FY 2023\) (.*)')


    mask = df['code'].str.match(r'CPT® HB\d{5}')
    df.loc[mask, 'billing_class'] = 'facility'
    df.loc[mask, 'hcpcs_cpt'] = df['code'].str.replace('CPT® HB', '')
    # df.loc[mask, 'modifiers'] = 'HB'

    payer_mapping = {
        'Gross_Charge': 'gross',
        'Deidentified_Minimum_Negotiated_Charge': 'min',
        'Deidentified_Maximum_Negotiated_Charge': 'max',
        'Discounted_Cash_Price': 'cash'
    }

    df['payer_category'] = df['payer_name'].map(payer_mapping).fillna('payer')

    df.dropna(subset='standard_charge', inplace=True)


    id_mapping = {
    '36-2513909-northwestern-medicine-central-dupage-hospital-standard-charges.json': '140242',
    '36-3484281-northwestern-medicine-delnor-hospital-standard-charges.json': '140211',
    '23-7087041-northwestern-medicine-kishwaukee-hospital-standard-charges.json': '140286',
    '36-2179779-northwestern-medicine-lake-forest-hospital-standard-charges.json': '140130',
    '36-2338884-northwestern-medicine-mchenry-hospital-standard-charges.json': '140116',
    '36-2169179-northwestern-medicine-palos-hospital-standard-charges.json': '140062',
    '36-4244337-northwestern-medicine-valley-west-hospital-standard-charges.json': '141340',
    '36-2338884-northwestern-medicine-woodstock-hospital-standard-charges.json': '140176',
    '37-0960170-northwestern-memorial-hospital-standard-charges.json': '140281',
    '36-2680776-marianjoy-rehabilitation-hospital-standard-charges.json': '143027'}

    hosp_id = id_mapping[file]
    df['hospital_id'] = hosp_id

    # Modifiers
    mask = df['hcpcs_cpt'].str.len() == 7
    df.loc[mask, 'modifiers'] = df.loc[mask, 'hcpcs_cpt'].str[-2:]

    # Remove last two characters from 'hcpcs_cpt'
    df.loc[mask, 'hcpcs_cpt'] = df.loc[mask, 'hcpcs_cpt'].str[:-2]

    mask = ~df['hcpcs_cpt'].isna() & df['hcpcs_cpt'].str.match(r'^[A-Z][0-9]{4}$|^[0-9]{5}$|^[0-9]{4}[A-Z]$')

    df.loc[~mask, ['hcpcs_cpt', 'modifiers']] = (pd.NA, pd.NA)

    output_folder = '.\\output_files\\'
    output_file = file.split('-standard-charges')[0]
    output_file = '-'.join(output_file.split('-')[2:])
    output_file = hosp_id + '_' + output_file + '.csv'

    df.to_csv(output_folder + output_file, index=False)
