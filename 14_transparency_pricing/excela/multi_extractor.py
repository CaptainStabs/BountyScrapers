
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
    


folder = '.\\input_files\\'

for file in os.listdir(folder):
    df = pd.read_excel(folder + file, header=2, dtype={'SERVICE CODE': str})

    df.rename(columns={
        'SERVICE CODE': 'internal_code',
        'SERVICE CODE DESC': 'desc',
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

    df['code'].fillna('na')
    df['code_prefix'].fillna('na')


    ein = file.split("_")[0]
    ein = ein[:2] + "-" + ein[2:]

    df['hospital_ein'] = ein
    df['hospital_ccn'] = ccns[file.split("_")[0]]
    df['file_last_updated'] = '2022-12-20'
    df['filename'] = file
    df['url'] = "https://www.excelahealth.org/documents/content/" + file

    df.to_csv(".\\output_folder\\" + file.split("_")[0], index=False)
