import os
import pandas as pd
from tqdm import tqdm

folder = './input_files/'

# file = 'sentara-albemarle-medical-center_standardcharges.xlsx'

var_name = 'payer_name'
value_name = 'standard_charge'

rename_dict = {
        'CDM': 'local_code',
        'CDM DESCRIPTION': 'description',
        'HCPCS': 'hcpcs_cpt',
        'Revenue Code': 'rev_code',
        'CPT/HCPCS': 'hcpcs_cpt',
        'HCPCS': 'hcpcs_cpt',
        'MS-DRG': 'ms_drg',
    }

for file in tqdm(os.listdir(folder)):
    print('\n', file)
    xls = pd.ExcelFile(folder + file)

    sheets = xls.sheet_names
    sheets.remove('Tab Summary')
    sheets.remove('Discounted Cash Price')

    # # Gross Charges

    gc_df = pd.read_excel(xls, 'Gross Charges', dtype=str, skiprows=4)

    gc_df.rename(columns={
        'CDM': 'local_code',
        'CDM Description': 'description',
        'Revenue Code': 'rev_code',
        
    }, inplace=True)

    cols = gc_df.columns.tolist()
    id_vars = cols[:4]
    value_vars = cols[4:]

    gc_df = pd.melt(gc_df, id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)

    payer_mapping = {
        'Unit Price': 'gross',
        'Discount Cash Price': 'cash'
    }

    gc_df['rate_category'] = gc_df['payer_name'].map(payer_mapping)

    sheets.remove('Gross Charges')


    # # Pharmacy & Supply

    try:
        pharm_sheet = 'Pharmacy & Supply Charges'
        psc = pd.read_excel(xls, pharm_sheet, dtype=str, skiprows=4)
    except ValueError:
        pharm_sheet = 'Pharmacy & Suppy Charges'
        psc = pd.read_excel(xls, pharm_sheet, dtype=str, skiprows=4)


    psc.rename(columns={
        'CDM': 'local_code',
        'CDM DESCRIPTION': 'description',
        'HCPCS': 'hcpcs_cpt',
        'Revenue Code': 'rev_code'
    }, inplace=True)

    cols = psc.columns.tolist()
    id_vars = cols[:4]
    value_vars = cols[4:]

    psc = pd.melt(psc, id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)

    psc['rate_category'] = psc['payer_name'].map(payer_mapping)

    sheets.remove(pharm_sheet)


    # # Inpatient Minimum

    ipmin = pd.read_excel(xls, 'Inpatient Minimum', dtype=str, skiprows=4)

    ipmin.rename(columns={
        'MS-DRG': 'ms_drg',
        'Description': 'description',
    }, inplace=True)

    cols = ipmin.columns.tolist()
    id_vars = cols[:2]
    value_vars = cols[2:]

    ipmin = pd.melt(ipmin, id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)

    ipmin['rate_category'] = 'min'
    ipmin['setting'] = 'inpatient'

    sheets.remove('Inpatient Minimum')


    # # Inpatient Maximum

    ipmax = pd.read_excel(xls, 'Inpatient Maximum', dtype=str, skiprows=4)

    ipmax.rename(columns={
        'MS-DRG': 'ms_drg',
        'Description': 'description',
    }, inplace=True)

    cols = ipmax.columns.tolist()
    id_vars = cols[:2]
    value_vars = cols[2:]

    ipmax = pd.melt(ipmax, id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)

    ipmax['rate_category'] = 'max'
    ipmax['setting'] = 'inpatient'

    sheets.remove('Inpatient Maximum')


    # # Outpatient Minimum

    opmin = pd.read_excel(xls, 'Outpatient Minimum', dtype=str, skiprows=4)

    opmin.rename(columns={
        'APC': 'apc',
        'Description': 'description',
    }, inplace=True)

    cols = opmin.columns.tolist()
    id_vars = cols[:2]
    value_vars = cols[2:]

    opmin = pd.melt(opmin, id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)

    opmin['rate_category'] = 'min'
    opmin['setting'] = 'outpatient'

    mask = opmin['apc'].str.contains('N')
    opmin.loc[mask, 'code'] = opmin['apc']
    opmin.loc[mask, 'apc'] = pd.NA

    sheets.remove('Outpatient Minimum')


    # # Outpatient Maximum

    opmax = pd.read_excel(xls, 'Outpatient Maximum', dtype=str, skiprows=4)

    opmax.rename(columns={
        'APC': 'apc',
        'Description': 'description',
    }, inplace=True)

    cols = opmax.columns.tolist()
    id_vars = cols[:2]
    value_vars = cols[2:]

    opmax = pd.melt(opmax, id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)

    opmax['rate_category'] = 'max'
    opmax['setting'] = 'outpatient'

    mask = opmax['apc'].str.contains('N')
    opmax.loc[mask, 'code'] = opmax['apc']
    opmax.loc[mask, 'apc'] = pd.NA

    sheets.remove('Outpatient Maximum')


    # # Inpatient Payers

    ip_sheets = [x for x in sheets if x.startswith('IP')]

    ip_dfs = []

    for sheet in ip_sheets:
        df = pd.read_excel(xls, sheet, dtype=str)
        
        payer = df.iloc[2, 1]
        df.columns = df.loc[5]
        df = df.loc[6:]
        
        df.rename(columns={
        'MS-DRG': 'ms_drg',
        'Description': 'description',
        'Payer Specific Negotiated Charge': 'standard_charge'
        }, inplace=True)

        df['payer_name'] = payer
        df['rate_category'] = 'negotiated'

        ip_dfs.append(df)

    ip_df = pd.concat(ip_dfs, ignore_index=True)

    ip_df['setting'] = 'inpatient'


    # # Outpatient Payers

    op_sheets = [x for x in sheets if x.startswith('OP')]

    op_dfs = []

    for sheet in op_sheets:
        df = pd.read_excel(xls, sheet, dtype=str)
        
        payer = df.iloc[2, 1]
        df.columns = df.loc[5]
        df = df.loc[6:]

        df.rename(columns={
            'APC': 'apc',
            'Description': 'description',
            'Payer Specific Negotiated Charge': 'standard_charge'
        }, inplace=True)

        df['payer_name'] = payer
        df['rate_category'] = 'negotiated'

        mask = df['apc'].str.startswith('N')
        df.loc[mask, 'code'] = df['apc']
        df.loc[mask, 'apc'] = pd.NA

        op_dfs.append(df)

    op_df = pd.concat(op_dfs, ignore_index=True)

    op_df['setting'] = 'outpatient'

    dfs = [gc_df, psc, ipmin, ipmax, opmin, opmax, ip_df, op_df]

    df = pd.concat(dfs)

    id_map = {
        'sentara-albemarle-medical-center_standardcharges.xlsx': '340109',
        'sentara-careplex-hospital_standardcharges.xlsx': '490093',
        'sentara-halifax-regional-hospital_standardcharges.xlsx': '490013',
        'sentara-leigh-hospital_standardcharges.xlsx': '490046',
        'sentara-martha-jefferson-hospital_standardcharges.xlsx': '490077',
        'sentara-norfolk-general-hospital_standardcharges.xlsx': '490007',
        'sentara-northern-virginia-medical-center_standardcharges.xlsx': '490113',
        'sentara-obici-hospital_standardcharges.xlsx': '490044',
        '273208969_sentara-princess-anne-hospital_standardcharges.xlsx': '490119',
        'sentara-rmh-medical-center_standardcharges.xlsx': '490004',
        'sentara-virginia-beach-general-hospital_standardcharges.xlsx': '490057'
    }

    hosp_id = id_map[file]
    df['hospital_id'] = hosp_id

    df.to_csv('./output_files/' + hosp_id + file.split('_')[1] + '.csv', index=False)
