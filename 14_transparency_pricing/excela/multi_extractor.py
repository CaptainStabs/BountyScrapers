import pandas as pd
import os


ccns = {
    '250965375': '390217',
    '250965414': '390219',
    '250965612': '390145'
}


def payer_category(payer):
    payers = {
        'GROSS CHARGES': 'gross',
        'DISCOUNTED CASH PRICE': 'cash',
        'De-Identified Minimum Negotiated Price': 'min',
        'De-Identified Maximum Negotiated Price': 'max'
    }

    try:
        return payers[payer]
    except KeyError:
        return 'payer'

def plan_type(payer):
    com = 'Commercial Contracts'
    med = 'Medicare Managed Care Contracts'
    # Medical Assistance does not need to be included because they all have it
    payers = {
        'Aetna (PEBTF)': com,
        "Highmark Children's Health Insurance Program (CHIP)": com,
        'Highmark ACA Products': com,
        'Highmark - Laurel Surgical': com,
        'UPMC ACA (Exchange)': com,
        'AmeriHealth Caritas': med,
        'VA CCN': med,
    }

    if 'Commercial' in payer:
        return com
    elif 'Medicare' in payer:
        return med
    elif 'Medical Assistance' in payer:
        return 'Medical Assistance Managed Care Contracts'

    else:
        try:
            return payers[payer]
        except KeyError:
            return pd.NA

def plan_name(payer):
    payers = {
        'Aetna (PEBTF)': 'Pennsylvania Employees Benefit Trust Fund (PEBTF)',
        # 'Highmark ACA Products': 'Affordable Care Act (ACA)',
        'Highmark Medicare Advantage Community Blue': 'Community Blue Medicare',
        'Highmark Medicare Advantage Security Blue': 'Security Blue HMO-POS',
        'Highmark Medicare Advantage Freedom Blue': 'Freedom Blue PPO',
        "Highmark Children's Health Insurance Program (CHIP)": 'Highmark Healthy Kids (CHIP)',
    }

    try:
        return payers[payer]
    except KeyError:
        return pd.NA
    
def group_characters(modifier):
    if pd.isna(modifier):
        return None
    else:
        return ' '.join([modifier[i:i+2] for i in range(0, len(modifier), 2)])


folder = '.\\input_files\\'

for file in os.listdir(folder):
    df = pd.read_excel(folder + file, header=2, dtype={'SERVICE CODE': str})

    df.rename(columns={
        'SERVICE CODE': 'internal_code',
        'SERVICE CODE DESC': 'description',
        'CPT/HCPCS CODE': 'code_orig',
    }, inplace=True)


    cols = df.columns.tolist()
    col_index = cols.index('GROSS CHARGES')
    id_vars = cols[:col_index]
    value_vars = cols[col_index:]

    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='payer_orig', value_name='rate')


    df['payer_category'] = df['payer_orig'].apply(payer_category)
    df['plan_name'] = df['payer_orig'].apply(plan_name)

    df['payer_orig'] = df['payer_orig'].str.strip()

    df['code'] = df['code_orig']
    df['payer_name'] = df['payer_orig']

    # Set code_prefix to 'hcpcs_cpt' if code is not na
    df.loc[df['code'].notna(), 'code_prefix'] = 'hcpcs_cpt'
    df.loc[df['plan_name'].notna(), 'plan_orig'] = df['payer_name']
    df['plan_orig'] = df['plan_orig'].fillna('na')

    df['code'] = df['code'].fillna('na')
    df['code_prefix'] = df['code_prefix'].fillna('none')
    df['modifier'] = df['code'].apply(lambda x: str(x)[5:] if len(str(x)) > 5 else pd.NA)
    df['modifier'] = df['modifier'].apply(group_characters)
    df['modifier'] = df['modifier'].fillna('na')


    # This is nulling the entire code column for some reason
    # df['code'] = df['code'].str[:5]

    df['code'] = df['code'].apply(lambda x: str(x)[:5] if len(str(x)) > 5 else x)


    df['rate'] = df['rate'].astype(str)
    df = df[(df['rate'] != 'Follows Medicare Logic; Payment Varies By Case') & (df['rate'] != '0')]
    df['rate'] = df['rate'].str.replace(',', '').str.replace('$', '', regex=False)
    df['rate'] = df['rate'].str.strip()
    df['rate_desc'] = df['rate'].apply(lambda x: " ".join(str(x).split()[1:]) if " " in str(x) else " ".join(str(x).split('/')[1:]) if "/" in str(x) else pd.NA)
    df['rate'] = df['rate'].apply(lambda x: str(x).split()[0].split('/')[0] if " " in x or "/" in x else x)
    df['rate'] = df['rate'].astype(float)
    df.dropna(subset=['rate'], inplace=True)


    


    ein = file.split("_")[0]
    ein = ein[:2] + "-" + ein[2:]

    df['hospital_ein'] = ein
    df['hospital_ccn'] = ccns[file.split("_")[0]]
    df['file_last_updated'] = '2022-12-20'
    df['filename'] = file
    df['url'] = "https://www.excelahealth.org/documents/content/" + file

    df.to_csv(".\\output_files\\" + file.split("_")[0] + '.csv', index=False)

