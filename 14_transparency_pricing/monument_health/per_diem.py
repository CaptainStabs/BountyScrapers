from tqdm import tqdm
import pandas as pd


folder = './input_files/'

files = ['46-0360899_CusterHospital_StandardCharges.xlsx', '46-0360899_LeadDeadwoodHospital_StandardCharges.xlsx', '46-0360899_SturgisHospital_StandardCharges.xlsx']

for file in tqdm(files):
    df = pd.read_excel(folder + file, dtype=str, skiprows=1)


    df.drop(columns=['Location', 'Charge'], inplace=True)


    df.rename(columns={
        'Code Type': 'line_type',
        'Code': 'code',
        'Description': 'description',
        'Patient Type': 'setting'
    }, inplace=True)


    df['setting'] = df['setting'].str.lower()


    cols = df.columns.tolist()
    id_vars = cols[:4]
    val_vars = cols[4:]

    df = pd.melt(df, id_vars=id_vars, value_vars=val_vars, var_name='payer_name', value_name='standard_charge')

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

    df.to_csv(output_folder + hosp_id + '_' + file.split('_')[1] + '_' + 'per_diem' + '.csv', index=False)



