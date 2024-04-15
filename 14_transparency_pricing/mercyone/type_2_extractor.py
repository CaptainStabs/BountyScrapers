import pandas as pd
import os
from tqdm import tqdm

folder = '.\\input_files\\other_schema\\'

# file = '202552602_Mercy Medical Center Dyersville_standardcharges.xlsx'


for file in tqdm(os.listdir(folder)):
    print(file)
    if file == '420818642_MercyOne Elkader Medical Center_standardcharges.xlsx':
        skip = 2
    else:
        skip = 1

    df = pd.read_excel(folder + file, skiprows=skip, dtype=str)


    df.rename(columns={
        'Code': 'code',
        'Description': 'description',
        'Type': 'setting',
    }, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:3]
    value_vars = cols[3:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    df['code'] = df['code'].str.strip()


    df.loc[(~df['code'].isna()) & (df['code'].str.match(r'^[A-Z][0-9]{4}$|^[0-9]{5}$|^[0-9]{4}[A-Z]$')), 'hcpcs_cpt'] = df['code']
    df.loc[(~df['code'].isna()) & (df['code'].str.len() == 3), 'ms_drg'] = df['code']


    mapping = {
        'Gross charge': 'gross',
        'Discounted cash price': 'cash',
        'De-identified min contracted rate': 'min',
        'De-identified max contracted rate': 'max'
    }

    df['payer_category'] = df['payer_name'].map(mapping).fillna('payer')


    df.loc[(~df['payer_name'].str.contains('De-identified') & (df['payer_name'].str.contains('-'))), 'plan_name'] = df['payer_name'].str.split('-').str[-1]


    df['setting'] = df['setting'].str.lower()


    mapping = {'421470935_mercyone-newton-medical-center_standardcharges.csv': '160032',
        '420758901_MercyOne Cedar Falls Medical Center_standardcharges.xlsx': '160040',
        '311373080_Mercy Medical Center North Iowa_standardcharges.xlsx': '160064',
        '421264647_MercyOne Waterloo Medical Center_standardcharges.xlsx': '160067',
        '421437483_Mercy Medical Center Dubuque_standardcharges.xlsx': '160069',
        '421336618_Mercy Medical Center Clinton_standardcharges.xlsx': '160080',
        '420680448_mercyone-des-moines-medical-center_standardcharges.xlsx': '160083',
        '311407377_Mercy Medical Center Siouxland_standardcharges.xlsx': '160153',
        '421500277_MercyOne Primghar Medical Center_standardcharges.xlsx': '161300',
        '420818642_MercyOne Elkader Medical Center_standardcharges.xlsx': '161319',
        '421178403_MercyOne Oelwein Medical Center_standardcharges.xlsx': '161338',
        '420680308_mercyone-centerville-medical-center_standardcharges.csv': '161377',
        '202552602_Mercy Medical Center Dyersville_standardcharges.xlsx': '161378'}

    hospital_id = mapping[file]
    df['hospital_id'] = hospital_id


    output_folder = '.\\output_files\\other_schema\\'
    df.to_csv(output_folder + hospital_id + "_" + file.split('_')[1].replace(' ', '_') + '.csv', index=False)


