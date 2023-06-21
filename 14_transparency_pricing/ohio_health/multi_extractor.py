import pandas as pd
from tqdm import tqdm
import os



folder = '.\\input_files\\'
# file = '38-4105653_berger_standardcharges.xlsx'


for file in tqdm(os.listdir(folder)):
    df = pd.read_excel(folder + file, dtype=str, skiprows=3)

    df.rename(columns={
        'Procedure Description': 'description',
        'Patient Class (Inpatient/Outpatient)': 'setting',
        'Code': 'code',
        'Quantity': 'drug_quantity',
        'Rev Code': 'rev_code',
        'Derived Negotiated Rate Estimate Min': 'Commercial - Derived Negotiated Rate Estimate Min',
        'Derived Negotiated Rate Estimate Max': 'Commercial - Derived Negotiated Rate Estimate Max',
        'Derived Negotiated Rate Estimate Min.1': 'Managed Medicaid - Derived Negotiated Rate Estimate Min',
        'Derived Negotiated Rate Estimate Max.1': 'Managed Medicaid - Derived Negotiated Rate Estimate Max',
        'Derived Negotiated Rate Estimate Min.2': 'Managed Medicare - Derived Negotiated Rate Estimate Min',
        'Derived Negotiated Rate Estimate Max.2': 'Managed Medicare - Derived Negotiated Rate Estimate Max'
    }, inplace=True)


    cols = df.columns.tolist()

    id_vars = cols[:5]
    val_vars = cols[5:]

    df = pd.melt(df, id_vars=id_vars, value_vars=val_vars, var_name='payer_name', value_name='standard_charge')


    val_vars


    df.dropna(subset=['standard_charge'], inplace=True)


    df['setting'] = df['setting'].str.lower()
    df['code'] = df['code'].str.strip()


    df.loc[(~df['code'].isna()) & (df['code'].str.contains('MS-DRG')), 'ms_drg'] = df['code'].str.extract(r'MS-DRG V39 \(FY2022\) (\d+)', expand=False)
    df.loc[(~df['code'].isna()) & (df['code'].str.match('HCPCS|CPT®')), 'hcpcs_cpt'] = df['code'].str.replace('HCPCS |CPT® ', '', regex=True)
    df.loc[(~df['code'].isna()) & (df['code'].str.contains('Custom')), 'local_code'] = df['code'].str.replace('Custom ', '')


    df['hcpcs_cpt'] = df['hcpcs_cpt'].str.strip()
    df.loc[(df['hcpcs_cpt'].str.len() == 8) | (df['hcpcs_cpt'] == 'CUSTOM') | (df['hcpcs_cpt'].str.len() != 5), 'hcpcs_cpt'] = pd.NA


    df.loc[(~df['rev_code'].isna()), 'rev_code'] = df['rev_code'].str.extract(r'(\d{4})', expand=False)


    df.loc[(df['drug_quantity'] == "1") | (df['drug_quantity'] == '(blank)'), 'drug_quantity'] = pd.NA


    df.drop_duplicates(subset='setting')


    df.loc[(~df['setting'].isna()) & (df['setting'].str.match(r'pharmacy|supplies')), 'setting'] = pd.NA


    df.loc[df['setting'] == 'professional', ['setting', 'billing_class']] = (pd.NA, 'professional')
    df.loc[df['setting'] == 'erx', ['setting', 'line_type']] = (pd.NA, 'erx')
    df.loc[df['setting'] == 'sup', ['setting', 'line_type']] = (pd.NA, 'sup')

    df['hcpcs_cpt'] = df['hcpcs_cpt'].str.upper()


    mapping = {
        'Commercial - Derived Negotiated Rate Estimate Min': 'min',
        'Commercial - Derived Negotiated Rate Estimate Max': 'max',
        'Managed Medicaid - Derived Negotiated Rate Estimate Min': 'min',
        'Managed Medicaid - Derived Negotiated Rate Estimate Max': 'max',
        'Managed Medicare - Derived Negotiated Rate Estimate Min': 'min',
        'Managed Medicare - Derived Negotiated Rate Estimate Max': 'max',
        'Discounted Cash Price (Uninsured Discount 35%)': 'cash',
        'Gross Charge': 'gross',
    }

    df['payer_category'] = df['payer_name'].map(mapping)


    id_mapping = {'38-4105653_berger_standardcharges.xlsx': '360170',
    '31-4394942_doctors_standardcharges.xlsx': '360152',
    '31-4394942_dublin_standardcharges.xlsx': '360348',
    '31-4379436_grady_standardcharges.xlsx': '360210',
    '31-4394942_grant_standardcharges.xlsx': '360017',
    '31-4440479_hardin_standardcharges.xlsx': '361315',
    '31-1070877_marion_standardcharges.xlsx': '360011',
    '31-4394942_grove-city_standardcharges.xlsx': '360372',
    '34-0714456_mansfield_standardcharges.xlsx': '360118',
    '31-4446959_obleness_standardcharges.xlsx': '360014',
    '34-0714456_shelby_standardcharges.xlsx': '361324',
    '31-4394942_riverside_standardcharges.xlsx': '360006'}

    hosp_id =  id_mapping[file]
    df['hospital_id'] = hosp_id


    output_folder = ".\\output_files\\"

    file = hosp_id + '_' + file.split('_')[1] + '.csv'

    df.to_csv(output_folder + file, index=False)


