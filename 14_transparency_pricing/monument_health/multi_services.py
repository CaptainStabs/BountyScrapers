import pandas as pd
from tqdm import tqdm


folder = './input_files/'

files = ['46-0319070_RapidCityHospital_StandardCharges.xlsx', '46-0360899_SpearfishHospital_StandardCharges.xlsx']


for file in tqdm(files):
    df = pd.read_excel(folder + file, dtype=str, sheet_name='Bundled Services', skiprows=1)


    df.drop(columns=['Location', 'Charge'], inplace=True)


    df.rename(columns={
        'Code Type': 'line_type',
        'Code': 'code',
        'Description': 'description'
    }, inplace=True)


    df.loc[~df['Blue Cross Blue Shield Wellmark\nBlue Cross Blue Shield Federal'].isna()]


    def split_column_by_newline(df):
        for column_name in df.columns:
            if '\n' in column_name:
                new_column_names = column_name.split('\n')
                df[new_column_names[0]] = df[column_name]
                df[new_column_names[1]] = df[column_name]
                df.drop(column_name, axis=1, inplace=True)
                
    # Apply the function to split columns with '\n'
    split_column_by_newline(df)


    cols = df.columns.tolist()
    id_vars = cols[:4]
    val_vars = cols[4:]

    df = pd.melt(df, id_vars=id_vars, value_vars=val_vars, var_name='payer_name', value_name='standard_charge')


    payer_mapping = {
        'De-Identified Minimum Negotiated Charge': 'min',
        'De-Identified Maximum Negotiated Charge': 'max',
    }

    df['rate_category'] = df['payer_name'].map(payer_mapping).fillna('negotiated')


    df.loc[df['line_type'].str.upper().str.contains('PER DIEM'), 'contracting_method'] = 'per diem'


    df.loc[df['line_type'] == 'MS-DRG', 'ms_drg'] = df['code']
    df.loc[df['line_type'] == 'MS DRG-PER DIEM', 'ms_drg'] = df['code']
    df.loc[df['line_type'] == 'APR-DRG', 'apr_drg'] = df['code']
    df.loc[df['line_type'] == '	APR-DRG Per Diem', 'apr_drg'] = df['code']
    df.loc[df['line_type'] == 'EAPG', 'eapg'] = df['code']
    df.loc[df['line_type'] == 'APC', 'apc'] = df['code']



    df.loc[df['Patient Type'].str.contains('Inpatient'), 'setting'] = 'inpatient'
    df.loc[df['Patient Type'].str.contains('Outpatient'), 'setting'] = 'outpatient'


    id_mapping = {
    '46-0360899_SpearfishHospital_StandardCharges.xlsx': '430048',
    '46-0319070_RapidCityHospital_StandardCharges.xlsx': '430077',
    '46-0360899_LeadDeadwoodHospital_StandardCharges.xlsx': '431320',
    '46-0360899_SturgisHospital_StandardCharges.xlsx': '431321',
    '46-0360899_CusterHospital_StandardCharges.xlsx': '431323'
    }

    hosp_id = id_mapping[file]

    df['hospital_id'] = hosp_id

    output_folder = '.\\output_files\\'

    df.to_csv(output_folder + hosp_id + '_' + file.split('_')[1] + '_' + 'bundled_services' + '.csv', index=False)



