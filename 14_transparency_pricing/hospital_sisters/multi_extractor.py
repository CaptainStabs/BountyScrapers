import os
import pandas as pd
from tqdm import tqdm


folder = './input_files/'

# file = '370663568_ST-JOSEPH-S-HOSPITAL-HIGHLAND_STANDARDCHARGES.txt'

for file in tqdm(os.listdir(folder)):
    df = pd.read_csv(folder + file, dtype=str, skiprows=1, encoding='ansi')


    df.drop('Site', axis=1, inplace=True)


    df.rename(columns=lambda x: x.strip(), inplace=True)


    df.rename(columns={
        'Svc_Cd': 'local_code',
        'HCPC/Cpt_Cd': 'code',
        'CDM_Svc_Descr': 'description',
        'Rev_Cd': 'rev_code',
        'Quantity/Units': 'drug_quantity', 
    }, inplace=True)


    df['drug_quantity'] = df['drug_quantity'].str.strip()
    df.loc[df['drug_quantity'] == '1', 'drug_quantity'] = pd.NA


    cols = df.columns.tolist()
    id_vars = cols[:5]
    val_vars = cols[5:]

    df = pd.melt(df, id_vars=id_vars, value_vars=val_vars, var_name='payer_name', value_name='standard_charge')


    df['code'] = df['code'].str.strip()


    mask = ~df['code'].isna()


    df.loc[mask & df['code'].str.match(r'^\d{3}$'), 'ms_drg'] = df['code']


    df['temp_code'] = df['code'].str.upper()
    df.loc[mask & df['temp_code'].str.match(r'^[A-Z][0-9]{4}$|^[0-9]{5}$|^[0-9]{4}[A-Z]$'), 'hcpcs_cpt'] = df['code']

    df['hcpcs_cpt'] = df['hcpcs_cpt'].str.upper()


    payer_map = {
        'Hospital_Cdm_Chg': 'gross',
        'Self_Pay_Chg': 'cash',
        'Minimum_Negotiated_Chg': 'min',
        'Maximum_Negotiated_Chg': 'max',
    } 

    df['rate_category'] = df['payer_name'].map(payer_map).fillna('negotiated')


    df['standard_charge'] = df['standard_charge'].str.replace('$', '').str.replace(',', '')


    df.loc[df['code'] == '1967', 'hcpcs_cpt'] = '01967'


    df.loc[df['code'].str.len() == 4, 'hcpcs_cpt'] = df['code'].str.zfill(5)
    df.loc[~df['rev_code'].isna(), 'rev_code'] = df['rev_code'].str.zfill(4)


    df.drop('temp_code', axis=1, inplace=True)

    # df_obj = df.select_dtypes(['object'])
    # df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    df['standard_charge'] = df['standard_charge'].str.strip()

    df.loc[df['standard_charge'].str.lower().str.contains('inpatient'), 'setting'] = 'inpatient'
    df.loc[df['standard_charge'].str.lower().str.contains('outpatient'), 'setting'] = 'outpatient'
    
    # Remove rows where standard_charge has no value
    df.loc[df['standard_charge'].str.match('^Inpatient Medicare$|^Inpatient Medicaid$'), 'standard_charge'] = pd.NA
    df.loc[df['standard_charge'] == 'N/A', 'standard_charge'] = pd.NA
    df.dropna(subset='standard_charge', inplace=True)
    
    df.loc[df['standard_charge'].str.contains(r'Medicare|Medicaid'), 'standard_charge_percent'] = df['standard_charge'].str.extract(r'\+(\d{1,3})\%', expand=False)

    df['standard_charge_percent'] = df['standard_charge_percent'].astype(float)

    df.loc[~df['standard_charge_percent'].isna(), 'standard_charge_percent'] = df['standard_charge_percent'] + 100

    mask = df['standard_charge'].str.contains('Medicare|Medicaid')

    df.loc[mask, 'additional_generic_notes'] = df['standard_charge']
    df.loc[mask, 'standard_charge'] = pd.NA



    hosp_map = {
        '370512290_GOOD-SHEPHERD-HOSPITAL_STANDARDCHAGES.txt': '140019',
        '370661233_ST-ANTHONY-S-MEMORIAL-HOSPITAL_STANDARDCHARGES.txt': '140032',
        '370661238_ST-JOHN-S-HOSPITAL_STANDARDCHARGES.txt': '140053',
        '370792770_HOLY-FAMILY-HOSPITAL_STANDARDCHARGES.txt': '140137',
        '371208459_ST-JOSEPH-S-HOSPITAL-BREESE_STANDARDCHARGES.txt': '140145',
        '370661244_ST-MARY-S-HOSPITAL-DECATUR_STANDARDCHARGES.txt': '140166',
        '370663567_ST-ELIZABETH-S-HOSPITAL_STANDARDCHARGES.txt': '140187',
        '370663568_ST-JOSEPH-S-HOSPITAL-HIGHLAND_STANDARDCHARGES.txt': '141336',
        '370661236_ST-FRANCIS-HOSPITAL_STANDARDCHARGES.txt': '141350',
        '390807060_SACRED-HEART-HOSPITAL_STANDARDCHARGES.txt': '520013',
        '390810545_ST-JOSEPH-S-CHIPPEWA-FALLS_STANDARDCHARGES.txt': '520017',
        '390808480_ST-NICHOLAS-HOSPITAL_STANDARDCHARGES.txt': '520044',
        '390817529_ST-VINCENT-HOSPITAL_STANDARDCHARGES.txt': '520075',
        '390818682_ST-MARY-S-HOSPITAL_STANDARDCHARGES.txt': '520097',
        '390848401_ST-CLARE-MEMORIAL-HOSPITAL_STANDARDCHARGES.txt': '521310'
    }

    hosp_id = hosp_map[file]

    df['hospital_id'] = hosp_id

    output_folder = './output_files/'

    df.to_csv(output_folder + hosp_id + '_' + file.split('_')[1] + '.csv', index=False)


