import pandas as pd
import numpy as np
import os
from tqdm import tqdm

main_folder = 'G:\\transparency-in-pricing'
folder = main_folder + '\\input_files\\'

# file = '481281376_texas-health-center-for-diagnostics-and-surgery-plano_standardcharges.csv'

for file in tqdm(os.listdir(folder)):

    df = pd.read_csv(folder + file, dtype=str, skiprows=2, encoding='ansi')


    df.rename(columns={
        'GenlDescr': 'description',
        'Package Type': 'contracting_method',
        'Code Type': 'line_type',
        'RevCode': 'rev_code',
        'Code': 'code',
        'NDC': 'ndc',
        'Charge Quantity': 'drug_quantity'
    }, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:7]
    value_vars = cols[7:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    df.dropna(subset='standard_charge', inplace=True)


    df.loc[df['code'].str.match(r'^[A-Z][0-9]{4}$|^[0-9]{5}$|^[0-9]{4}[A-Z]$'), 'hcpcs_cpt'] = df['code']


    df.loc[~df['rev_code'].isna(), 'rev_code'] = df['rev_code'].str.zfill(4)


    df.loc[df['line_type'] == 'DRG', 'ms_drg'] = df['code']
    df.loc[~df['ms_drg'].isna(), 'ms_drg'] = df['ms_drg'].str.zfill(3)


    df.loc[df['line_type'] == 'APR DRG', 'apr_drg'] = df['code']
    df.loc[~df['apr_drg'].isna(), 'apr_drg'] = df['apr_drg'].str.zfill(4)

    df['apr_drg'] = df['apr_drg'].str[:3] + '-' + df['apr_drg'].str[-1]


    df.loc[df['code'].str.match('NOCPT|No CPT'), 'code'] = pd.NA


    df['contracting_method'] = df['contracting_method'].str.lower()
    df['line_type'] = df['line_type'].str.lower()


    payer_mapping = {
        'Price': 'gross',
        'Min IP TR': 'min',
        'Max IP TR': 'max',
        'Min IP': 'min',
        'Max IP': 'max',
        'Min OP': 'min',
        'Max OP': 'max',
        'Self Pay IP': 'cash',
        'Self Pay OP': 'cash'
    }

    df['rate_category'] = df['payer_name'].map(payer_mapping).fillna('negotiated')

    df['standard_charge'] = df['standard_charge'].str.replace(',', '')


    df['setting'] = np.where(df['payer_name'].str.contains(' IP'), 'inpatient', np.where(df['payer_name'].str.contains(' OP'), 'outpatient', 1))

    df_obj = df.select_dtypes(['object'])  # Select only object columns
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())


    id_mapping ={
        '750972805_texas-health-arlington-memorial-hospital_standardcharges.csv': '450064',
        '481281376_texas-health-center-for-diagnostics-and-surgery-plano_standardcharges.csv': '450891',
        '756001743_texas-health-harris-methodist-hospital-fort-worth_standardcharges.csv': '450135',
        '451502252_texas-health-harris-methodist-hospital-alliance_standardcharges.csv': '670085',
        '751748586_texas-health-harris-methodist-hospital-azle_standardcharges.csv': '450419',
        '751977850_texas-health-harris-methodist-hospital-cleburne_standardcharges.csv': '450148',
        '020555370_texas-health-harris-methodist-hospital-southlake_standardcharges.csv': '450888',
        '752678857_texas-health-harris-methodist-hospital-southwest-fort-worth_standardcharges.csv': '450779',
        '751752253_texas-health-harris-methodist-hospital-stephenville_standardcharges.csv': '450351',
        '203003947_texas-health-heart-and-vascular-hospital-arlington_standardcharges.csv': '670071',
        '831954982_texas-health-hospital-frisco_standardcharges.csv': '670260',
        '260684968_texas-health-presbyterian-hospital-flower-mound_standardcharges.csv': '670068',
        '752771437_texas-health-presbyterian-hospital-kaufman_standardcharges.csv': '450292',
        '202848116_texas-health-hospital-rockwall_standardcharges.csv': '670044',
        '751047527_texas-health-presbyterian-hospital-dallas_standardcharges.csv': '450462',
        '751438726_texas-health-harris-methodist-hospital-hurst-euless-bedford_standardcharges.csv': '450639',
        '752770738_texas-health-presbyterian-hospital-plano_standardcharges.csv': '450771',
        '432008974_texas-health-presbyterian-hospital-denton_standardcharges.csv': '450743'
    }

    hosp_id = id_mapping[file]

    df['hospital_id'] = hosp_id

    output_file = hosp_id + '_' + file.split('_')[1].replace('texas-health-', '') + '.csv'

    df.to_csv(main_folder + '\\output_files\\' + output_file, index=False)





