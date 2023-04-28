import pandas as pd
import polars as pl
import os

input_files = '.\\input_files\\'


for file in os.listdir(input_files):

    df = pd.read_csv(input_files + file, dtype=str)


    df.columns = df.columns.str.strip()
    df.rename(columns={
        'Code': 'code',
        'Description': 'description',
        'Type': 'setting',
    }, inplace=True)


    df.drop(columns=['Package/Line_Level', 'Derived contracted rate'], inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:3]
    value_vars = cols[3:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer', value_name='standard_charge')


    df['standard_charge'] = df['standard_charge'].str.strip()
    df.loc[df['standard_charge'] == 'N/A', 'standard_charge'] = pd.NA
    df.dropna(subset=['standard_charge'], inplace=True)

    df['setting'] = df['setting'].str.lower()




    df.loc[df['code'].str.len() == 1, 'ms_drg'] = df['code'].str.zfill(3)
    df.loc[df['code'].str.len() == 3, 'ms_drg'] = df['code']
    df.loc[df['code'].str.len() == 5, 'hcpcs_cpt'] = df['code']


    mapping = {
        'Gross Charge': 'gross',
        'Discounted cash price': 'cash',
        'De-identified min contracted rate': 'min',
        'De-identified max contracted rate': 'max',
    }
    df['payer_category'] = df['payer'].map(mapping).fillna('payer')


    file_locations = {
        'Boston': '223304',
        'Greenville': '423300',
        'Hawaii': '123301',
        'Northern': '053311',
        'Ohio': '363308',
        'Philadelphia': '393309',
        'Spokane': '503302',
        'Chicago': '143302',
        'Louis': '263304',
        'Portland': '383300',
        'Texas': '453311'
    }

    for location, ccn in file_locations.items():
        if location in file:
            id = ccn
            name = location

    df['hospital_id'] = ccn


    df['standard_charge'] = df['standard_charge'].str.replace(',', '', regex=False)


    df['standard_charge'] = pd.to_numeric(df['standard_charge'])


    df['ms_drg'].fillna('', inplace=True)
    df['hcpcs_cpt'].fillna('', inplace=True)
    df['code'].fillna('', inplace=True)


    df = pl.from_pandas(df)
    df.write_csv('.\\output_files\\' + name + '.csv')


