import os
import pandas as pd
from tqdm import tqdm

folder = '.\\input_files\\'

for file in tqdm(os.listdir(folder)):

    df = pd.read_csv(folder + file, dtype=str, skiprows=1)


    df.drop(columns='Facility Name', inplace=True)


    df.rename(columns={
        'Charge Description': 'description',
        'CPT/HCPCS': 'code'
        }, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:2]
    value_vars = cols[2:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    df.dropna(subset='standard_charge', inplace=True)


    mapping = {
        'Charge': 'gross',
        'De-Identified Minimum Negotiated Charge': 'min',
        'De-Identified Maximum Negotiated Charge': 'max',
        'Discounted Cash Price': 'cash'
    }

    df['payer_category'] = df['payer_name'].map(mapping).fillna('payer')


    df['standard_charge'] = df['standard_charge'].str.replace('$', '').str.replace(',', '')


    df.loc[(~df['code'].isna()) & (df['code'].str.match(r'^(?:[A-Z][0-9]{4}|[0-9]{5}|[0-9]{4}[A-Z])$')), 'hcpcs_cpt'] = df['code']
    df.loc[(~df['code'].isna()) & (df['code'].str.match(r'MS(\d{3})')), 'ms_drg'] = df['code'].str.extract(r'MS(\d+)', expand=False)


    ccns = {
        "561484844_wayneunchealthcare_standardcharges.csv": "340010",
        "562084959_pardeeunchealthcare_standardcharges.csv": "340017",
        "566000674_unclenoirhealthcare_standardcharges.csv": "340027",
        "560554202_caldwellunchealth_standardcharges.csv": "340041",
        "560530233_UNCHealthSoutheastern_standardcharges.csv": "340050",
        "823745228_uncrockinghamhealthcare_standardcharges.csv": "340060",
        "561118388_uncmedicalcenter_standardcharges.csv": "340061",
        "463176429_johnstonhealth_standardcharges.csv": "340090",
        "561509260_uncrexhealthcare_standardcharges.csv": "340114",
        "237027004_nashunchealthcare_standardcharges.csv": "340147",
        "560611546_chathamhospital_standardcharges.csv": "341311"
    }

    id = ccns[file]
    ein = file.split('_')[0]
    df['hospital_id'] = id
    output_name = '.\\output_files\\' + ein + '_' + id + '.csv'
    df.to_csv(output_name, index=False)


