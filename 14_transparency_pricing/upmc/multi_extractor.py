import pandas as pd
import numpy as np
import os
from tqdm import tqdm


folder = '.\\input_files\\'

file = '160743226_upmc-chautauqua_standardcharges.csv'

for file in tqdm(os.listdir(folder)):
        
    df = pd.read_csv(folder + file, dtype=str)


    df.rename(columns={
        'Description': 'description',
        'CPT/DRG': 'code',
        'NDC': 'ndc'
    }, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:4]
    value_vars = cols[4:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    df.loc[(df['code'].str.len() < 3) | (df['code'].str.len() == 3), 'ms_drg'] = df['code'].str.zfill(3)
    df.loc[df['code'].str.len() == 5, 'hcpcs_cpt'] = df['code']



    df['setting'] = np.where(df['payer_name'].str.startswith('IP ') | df['payer_name'].str.endswith(' IP'), 'inpatient', np.where(df['payer_name'].str.startswith('OP ') | df['payer_name'].str.endswith(' OP'), 'outpatient', 1))


    df.drop('Hospital', axis=1, inplace=True)


    df['payer_name'] = df['payer_name'].str.strip()


    mapping = {
        'IP Price': 'gross',
        'OP Price': 'gross',
        'Gross Charges IP': 'gross',
        'Gross Charges OP': 'gross',
        'Discounted Cash Price IP': 'cash',
        'Discounted Cash Price OP': 'cash',
        'Min Rate': 'min',
        'Max Rate': 'max',
        'IP Cash Price': 'cash',
        'OP Cash Price': 'cash',

    }

    df['payer_category'] = df['payer_name'].map(mapping).fillna('payer')


    df['standard_charge'] = df['standard_charge'].str.strip()
    df['standard_charge'] = df['standard_charge'].str.replace('\$|,', '')


    df.dropna(subset='standard_charge', inplace=True)


    ccns = {
    '160743226': '330239',
    '250965423': '390002',
    '250965406': '390016',
    '250965429': '390028',
    '240795508': '390045',
    '820880337': '390058',
    '251778644': '390067',
    '820844453': '390068',
    '821600494': '390071',
    '231352155': '390073',
    '250489010': '390091',
    '820912090': '390101',
    '232875070': '390102',
    '250965451': '390107',
    '250965420': '390114',
    '231396795': '390117',
    '250965480': '390164',
    '250523970': '390178',
    '231360851': '390233',
    '274814831': '390328',
    '250402510': '393302',
    '250965387': '399817'
    }

    ein = file.split('_')[0]

    id = ccns[ein]

    df['hospital_id'] = id

    df.to_csv('.\\output_files\\' + id + '.csv', index=False)