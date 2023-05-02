import pandas as pd
import polars as pl
import os
from tqdm import tqdm


folder = '.\\input_files\\'

for file in tqdm(os.listdir(folder)):
    try:
        df = pd.read_csv(folder + file, dtype=str, skiprows=4, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(folder + file, dtype=str, skiprows=4, encoding='ansi')


    df.rename(columns={
        'Patient Type': 'setting',
        'DRG': 'ms_drg',
        'APR-DRG': 'apr_drg',
        'Procedure Code': 'local_code',
        'Procedure Name': 'description',
        'NDC': 'ndc',
        'Default Rev Code': 'rev_code',
        'CPT / HCPCS Code': 'hcpcs_cpt',
        'Service Package Type': 'contracting_method',
    }, inplace=True)


    df['setting'] = df['setting'].str.lower()
    df['contracting_method'] = df['contracting_method'].str.lower()


    df.drop(columns='Gross Charge Min/Max', inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:9]
    value_vars = cols[9:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer', value_name='standard_charge')


    df['standard_charge'] = pd.to_numeric(df['standard_charge'], errors='coerce')
    df.dropna(subset=['standard_charge'], inplace=True)


    empty_cols = ['ms_drg', 'apr_drg', 'local_code', 'ndc', 'rev_code', 'hcpcs_cpt']
    df.loc[:, empty_cols] = df[empty_cols].fillna('')


    mapping = {
        'Gross Charge': 'gross',
        'Discounted Cash Price': 'cash',
        'De-Identified Minimum Reimbursement*': 'min',
        'De-Identified Maximum Reimbursement*': 'max',
    }

    df['payer_category'] = df['payer'].map(mapping).fillna('payer')


    ccn = {
            '74-1166904': '450054',
        '75-2586857': '450079',
        '74-1161944': '450101',
        '75-1008430': '450137',
        '75-1844139': '450372',
        '75-1777119': '450563',
        '75-2834135': '450851',
        '82-0551704': '450890',
        '74-1595711': '451374',
        '20-2850920': '452105',
        '41-2101361': '670025',
        '20-3749695': '670043',
        '27-4434451': '670088',
        '46-4007700': '670108',
        '81-3040663': '670136',
        '74-2519752': '450187', 
        '82-4052186': '450885',
        '26-0194016': '450742',
        '75-1037591': '670082',
        '26-3603862': '450893',
        '75-1837454': '450021'
    }

    ein = file.split('_')[0]

    if ein == '20-3749695':
        if 'round-rock' in file:
            id = '670034'
        elif 'lakeway' in file:
            id = '673058'
        elif 'cedar-park' in file:
            id = '670043'

    elif ein == '81-3040663':
        if 'plfugerville' in file:
            id = '670128'
        elif 'buda' in file:
            id = '670131'

        elif 'austin' in file:
            if = '670136'

    else:
        id = ccn[ein]
    df['hospital_id'] = id

    # Schema patches
    df['rev_code'] = df['rev_code'].str.zfill(4)
    df['ms_drg'] = df['ms_drg'].str.zfill(3)
    df.loc[df['rev_code'] == '-000', 'rev_code'] = ''
    df.loc[df['rev_code'] == '0000', 'rev_code'] = ''
    df.loc[df['ms_drg'] == '000', 'ms_drg'] = ''
    df.loc[df['hcpcs_cpt'].str.len() > 5, 'hcpcs_cpt'] = ''

    df = pl.from_pandas(df)
    df.write_csv('.\\output_files\\' + ein + '.csv')
