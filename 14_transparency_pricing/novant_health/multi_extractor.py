import pandas as pd
import os
from tqdm import tqdm

folder = '.\\input_files\\'
# file = '56-0554230_novanthealthcharlotteorthopedichospital_standardcharges.csv'


for file in tqdm(os.listdir(folder)):
    try:
        df = pd.read_csv(folder + file, dtype=str)
    except UnicodeDecodeError:
        df = pd.read_csv(folder + file, dtype=str, encoding='ansi')


    df.rename(columns={
        'Code': 'code',
        'Code Description': 'description',
        'CPT DRG': 'cpt_drg',
        'Charge Detail': 'contracting_method'
    }, inplace=True)


    cols = df.columns.tolist()
    id_vars = cols[:4]
    val_vars = cols[4:]

    df = pd.melt(df, id_vars=id_vars, value_vars=val_vars, var_name='payer_name', value_name='standard_charge')


    df.dropna(subset='standard_charge', inplace=True)


    df['cpt_drg'] = df['cpt_drg'].str.upper()

    df.loc[df['cpt_drg'].str.len() == 5, 'hcpcs_cpt'] = df['cpt_drg']
    df.loc[df['cpt_drg'].str.len() == 3, 'ms_drg'] = df['cpt_drg']

    df.loc[df['hcpcs_cpt'] == '(BLAN', 'hcpcs_cpt'] = pd.NA


    df.loc[df['code'].str.startswith('NDC'), 'ndc'] = df['code'].str.replace('NDC', '')


    df.drop(columns='cpt_drg', inplace=True)


    mask = ~df['contracting_method'].str.lower().isin(['standard charge', 'per diem', 'case rate'])
    df.loc[mask, 'additional_payer_specific_notes'] = df['contracting_method']
    df.loc[mask, 'contracting_method'] = 'other' # nulls methods not in the mask, after they have been copied to notes

    df.loc[df['contracting_method'] == 'Standard Charge', 'contracting_method'] = pd.NA
    df['contracting_method'] = df['contracting_method'].str.lower()


    df['payer_name'] = df['payer_name'].str.strip()


    payer_mapping = {
        'Gross Charge': 'gross',
        'De-identified minimum negotiated charge': 'min',
        'De-identified maximum negotiated charge': 'max',
        'Discounted cash price': 'cash'
    }

    df['payer_category'] = df['payer_name'].map(payer_mapping).fillna('payer')


    df.loc[df['description'].str.match(r'SUP\d{6}'), 'line_type'] = 'sup'

    # Strip all objects
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    df.loc[df['standard_charge'].str.contains('\$|,', regex=True), 'standard_charge'] = df['standard_charge'].str.replace('\$|,', '', regex=True)
    df.loc[df['standard_charge'] == '-', 'standard_charge'] = pd.NA

    df.dropna(subset='standard_charge', inplace=True)


    id_mapping = {
    '20-4278130_novanthealthbrunswickmedicalcenter_standardcharges.csv': '340158',
    '56-0554230_novanthealthcharlotteorthopedichospital_standardcharges.csv': '340153',
    '56-0928089_novanthealthforsythmedicalcenter_standardcharges.csv': '340014',
    '56-0554230_novanthealthhuntersvillemedicalcenter_standardcharges.csv': '340183',
    '56-1376368_novanthealthmatthewsmedicalcenter_standardcharges.csv': '340171',
    '56-1340424_novanthealthmedicalparkhospital_standardcharges.csv': '340148',
    '26-0599536_novanthealthminthillmedicalcenter_standardcharges.csv': '340190',
    '56-0887181_novanthealthnewhanorverregionalmedicalcenter_standardcharges.csv': '340141',
    '56-0653348_novanthealthpendermemorialhospital_standardcharges.csv': '341307',
    '56-0554230_novanthealthpresbyterianmedicalcenter_standardcharges.csv': '340053',
    '56-0547479_novanthealthrowanmedicalcenter_standardcharges.csv': '340015',
    '56-0636250_novanthealththomasvillemedicalcenter_standardcharges.csv': '340085'}

    hosp_id = id_mapping[file]
    df['hospital_id'] = hosp_id

    output_folder = '.\\output_files\\'

    file = hosp_id + '_' + file.split('_')[1] + '.csv'
    df.to_csv(output_folder + file, index=False)


