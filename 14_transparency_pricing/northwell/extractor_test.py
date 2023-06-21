import json
import pandas as pd
import os
from tqdm import tqdm
# import heartrate; heartrate.trace(browser=True, daemon=True)


def extractor():
    folder = 'F:\\_Bounty\\northwell\\input_files\\'

    for file in tqdm(os.listdir(folder)):
        print('\n' + file)
        with open(folder + file, 'r') as f:
            jf = json.load(f)

        try:
            cols = jf['Headers']
            data = jf['Data']
            df = pd.DataFrame(columns=cols, data=data)
            normal_file = True
        except TypeError:
            df = pd.DataFrame(jf)
            normal_file = False
        del jf


        df.rename(columns={
            'Identification_Description': 'description',
            'Identifier_Description': 'description',
            'Identifier_Code': 'local_code',
            'Billing_Code': 'code'
        }, inplace=True)


        df.drop('Site', axis=1, inplace=True)


        df['local_code'] = df['local_code'].replace("", pd.NA)
        df['code'] = df['code'].replace("", pd.NA)
        df['description'] = df['description'].str.strip()

        cols = df.columns.tolist()
        id_vars = cols[:3]
        value_vars = cols[3:]

        df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')

        if not normal_file:
            df['standard_charge'] = df['standard_charge'].replace('-', pd.NA)
            df['local_code'] = df['local_code'].replace('-', pd.NA)
            df['code'] = df['code'].replace('-', pd.NA)
            df['code'] = df['code']. replace('NULL', pd.NA)
        df['standard_charge'] = df['standard_charge'].replace('', pd.NA)
        df['standard_charge'] = df['standard_charge'].replace('N/A', pd.NA)
        df['standard_charge'] = df['standard_charge'].str.replace(',', '')

        df.dropna(subset='standard_charge', inplace=True)


        mapping = {
            'Charge': 'gross',
            'De-identified Maximum': 'max',
            'De-identified Minimum': 'min',
            'Discounted Cash Price': 'cash',   
        }

        df['payer_category'] = df['payer_name'].map(mapping).fillna('payer')

        # df.loc[~df['code'].isna()]


        df.loc[(~df['code'].isna()) & (df['code'].str.contains('APR DRG')), 'apr_drg_temp'] = df['code']
        df.loc[~df['apr_drg_temp'].isna(), 'apr_drg_temp'] = df['apr_drg_temp'].str.replace('APR DRG ', '')
        df.loc[~df['apr_drg_temp'].isna(), 'apr_drg'] = df['apr_drg_temp'].str[:3] + '-' + df['apr_drg_temp'].str[-1]
        df.drop('apr_drg_temp', axis=1, inplace=True)

        df['temp_code'] = df['code']
        df['temp_code'] = df['temp_code'].str.upper()
        df.loc[(~df['temp_code'].isna()) & (df['temp_code'].str.match(r'^(?:[A-Z][0-9]{4}|[0-9]{5}|[0-9]{4}[A-Z])$')), 'hcpcs_cpt'] = df['code']

        df.loc[(~df['temp_code'].isna()) & (df['temp_code'].str.contains('MSDRG')), 'ms_drg'] = df['code'].str.extract(r'MSDRG(\d+)', expand=False)

        df.drop('temp_code', axis=1, inplace=True)

        # Create a dictionary mapping of standard_charge values to replacement values
        charge_map = {
            'POC': ('other', 'POC', pd.NA),
            'NSP': ('other', 'NSP', pd.NA),
            'Packaged': ('other', 'Packaged', pd.NA),
            'APG - Bundling': ('other', 'APG - Bundling', pd.NA)
        }

        # Replace standard_charge values based on the dictionary mapping
        for charge, values in charge_map.items():
            df.loc[df['standard_charge'] == charge, ['contracting_method', 'additional_payer_specific_notes', 'standard_charge']] = values

        # Replace standard_charge values that contain ' PD'
        df.loc[df['standard_charge'].str.contains(' PD', na=False), ['contracting_method', 'additional_payer_specific_notes']] = ['other', 'PD']
        df.loc[df['standard_charge'].str.lower() == 'case rate', ['contracting_method', 'standard_charge']] = ['case rate', pd.NA]
        df.loc[df['standard_charge'].str.lower() == 'per diem', ['contracting_method', 'standard_charge']] = ['per diem', pd.NA]

        df['standard_charge'] = df['standard_charge'].str.replace(' PD', '')
        df['standard_charge'] = df['standard_charge'].str.replace('$', '', regex=False)
        df['hcpcs_cpt'] = df['hcpcs_cpt'].str.upper()


        ccn = {'11-1667761_South Shore University Hospital_StandardCharges.json': '330043',
        '11-1630914_Huntington Hospital_StandardCharges.json': '330045',
        '11-1562701_North Shore University Hospital_StandardCharges.json': '330106',
        '11-1661359_Peconic Bay Medical Center_StandardCharges.json': '330107',
        '13-1624070_Lenox Hill Hospital_StandardCharges.json': '330119',
        '11-2868878_Staten Island University Hospital_StandardCharges.json': '330160',
        '13-1740118_Northern Westchester Hospital_StandardCharges.json': '330162',
        '11-1633487_Glen Cove Hospital_StandardCharges.json': '330181',
        '11-1639818_Mather Memorial Hospital_StandardCharges.json': '330185',
        '11-2241326_Long Island Jewish Hospital_StandardCharges.json': '330195',
        '13-1725076_Phelps Memorial Hospital Center_StandardCharges.json': '330261',
        '11-3241243_Plainview Hospital_StandardCharges.json': '330331',
        '11-2241326_Long Island Jewish Forest Hills_StandardCharges.json': '330353',
        '11-2241326_Long Island Jewish Valley Stream_StandardCharges.json': '330372',
        '11-1562701_Syosset Hospital_StandardCharges.json': '330398'}


        id = ccn[file]

        df['hospital_id'] = id

        tqdm.write('Writing to file...')
        output_name = file.split('_')[0] + '_' + id + '.csv'
        # df.to_csv('F:\\_Bounty\\northwell\\output_files\\' + output_name, index=False)


extractor()