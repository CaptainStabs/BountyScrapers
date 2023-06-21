import pandas as pd
import os
from tqdm import tqdm



folder = '.\\input_files\\'

for file in tqdm(os.listdir(folder)):
    print('\n', file)
    if file == '221487576_raritan-bay-medical-center_standardcharges.xlsx':
        df = pd.read_excel(folder + file, dtype=str, skiprows=4)
    else:
        df = pd.read_excel(folder + file, dtype=str, skiprows=3)

    df.rename(columns=lambda x: x.strip().replace('\n', ' '), inplace=True)
    df.rename(columns={
        'Service Area': 'setting',
        'Service_x000D_ Area': 'setting',
        'Payor': 'payer_name',
        'MSDRG': 'ms_drg',
        'MSDRG Name': 'description',
        'Px Code': 'local_code',
        'Px Description': 'description1',
        'Primary/Bundled CPT Code': 'hcpcs_cpt',
        'CPT/HCPCS Code': 'alt_hcpcs_cpt',
        'Revenue Code': 'rev_code'
    }, inplace=True)


    df.drop('Location', axis=1, inplace=True)


    df.loc[df['local_code'] == 'See MSDRG', 'local_code'] = df['ms_drg']
    df.loc[df['description1'] == 'See MSDRG Name', 'description1'] = pd.NA
    df.loc[(~df['description1'].isna()) &  (df['description'].isna()), 'description'] = df['description1']


    df.drop('description1', axis=1, inplace=True)

    df['setting'] = df['setting'].str.lower().str.strip()
    df.loc[df['setting'] == 'all', 'setting'] = 'both'


    df['ms_drg'] = df['ms_drg'].str.zfill(3)


    df_payer = df.loc[(~df['payer_name'].isna())].copy()


    df_payer.drop(['Gross Charge', 'Discounted Cash Price', 'De-Identified Minimum', 'De-Identified Maximum'], axis=1, inplace=True)


    df_payer.rename(columns={'Payor Specific Negotiated Charge': 'standard_charge'}, inplace=True)


    df_payer.dropna(subset=['standard_charge'], inplace=True)


    df_payer['payer_category'] = 'payer'


    df.drop(['payer_name', 'Payor Specific Negotiated Charge'], axis=1, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:7]
    value_vars = cols[7:]


    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    mapping = {
    'Gross Charge': 'gross',
    'Discounted Cash Price': 'cash',
    'De-Identified Minimum': 'min',
    'De-Identified Maximum': 'max'    
    }

    df['payer_category'] = df['payer_name'].map(mapping)

    df = pd.concat([df, df_payer])

    df['rev_code'] = df['rev_code'].str.zfill(4)

    df.reset_index(inplace=True, drop=True)
    mask = df['alt_hcpcs_cpt'].str.len() > 5
    df.loc[mask, 'code'] = df['alt_hcpcs_cpt']
    df.loc[mask, 'alt_hcpcs_cpt'] = pd.NA

    mask = df['hcpcs_cpt'].str.len() > 5
    df.loc[mask, 'code'] = df['hcpcs_cpt']
    df.loc[mask, 'hcpcs_cpt'] = pd.NA

    df['hcpcs_cpt'] = df['hcpcs_cpt'].str.upper()
    df['alt_hcpcs_cpt'] = df['alt_hcpcs_cpt'].str.upper()

    mask = ~df['hcpcs_cpt'].astype(str).str.match(r'^[A-Z][0-9]{4}$|^[0-9]{5}$|^[0-9]{4}[A-Z]$')
    df.loc[mask, 'code'] = df['hcpcs_cpt']
    df.loc[mask, 'hcpcs_cpt'] = pd.NA

    df['description'] = df['description'].str.strip()


    df.drop(df[df['standard_charge'].str.strip() == '$-'].index, inplace=True)

    mapping = {'221487576_bayshore-medical-center_standardcharges.xlsx': '310112',
    '221487576_hackensack-university-medical-center_standardcharges.xlsx': '310001',
    '221487576_jersey-shore-university-medical-center_standardcharges.xlsx': '310073',
    '221487576_jfk-University-medical-center_standardcharges.xlsx': '310108',
    '221487576_ocean-medical-center_standardcharges.xlsx': '310052',
    '221487576_palisades-medical-center_standardcharges.xlsx': '310003',
    '221487576_raritan-bay-medical-center_standardcharges.xlsx': '310039',
    '221487576_riverview-medical-center_standardcharges.xlsx': '310034',
    '221487576_southern-ocean-medical-center_standardcharges.xlsx': '310113'}

    hospital_id = mapping[file]

    df['hospital_id'] = hospital_id

    out_folder = '.\\output_files\\'
    file = hospital_id + file.split('_')[1] + '.csv'

    df.dropna(subset='standard_charge', inplace=True)

    df.to_csv(out_folder + file, index=False)


