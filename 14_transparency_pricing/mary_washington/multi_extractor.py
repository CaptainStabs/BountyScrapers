import pandas as pd
import os

def payer_category(x):
    payers = {
        'Charge': 'gross',
        'Self Pay Price': 'cash',
        'Min Negotiated Rate': 'min',
        'Max Negotiated Rate': 'max',
    }

    try:
        return payers[x]
    except KeyError:
        return 'payer'


folder = '.\\input_files\\'

for file in os.listdir(folder):
    df = pd.read_excel(folder + file)


    df.rename(columns={
        'Code': 'code',
        'Desc.': 'description'
    }, inplace=True)


    cols = df.columns.tolist()
    id_vars = ['code', 'description']
    value_vars = cols[3:]
    value_vars.append('Charge')

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer', value_name= 'standard_charge')


    df.dropna(subset=['standard_charge'], inplace=True)


    df.loc[df['code'].str.len() == 5, 'hcpcs_cpt'] = df['code']


    df['payer_category'] = df['payer'].apply(payer_category)


    ccn = {
        '540519577': '490022',
        '134316364': '490140'
    }

    ein = file.split('_')[0]
    df['hospital_id'] = ccn[ein]


    df.to_csv(file.split('_')[0] + '.csv', index=False)


