import pandas as pd
import numpy as np
import os
from tqdm import tqdm


folder = '.\\input_files\\'

for file in tqdm(os.listdir(folder)):
    print('\n', file)

    mapping = {
        'CDM Price': 'gross',
        'Discounted Self Pay/Cash Price': 'cash',
        'Inpatient De-Identified Minimum Negoticated Rate': 'min',
        'Inpatient De-Identified Maximum Negoticated Rate': 'max',
        'Outpatient De-Identified Minimum Negoticated Rate': 'min',
        'Outpatient De-Identified Maximum Negoticated Rate': 'max',
        'Median Charges': 'gross',
        'Median Price': 'gross',
        'Median Charges': 'gross',
        
    }



    df = pd.read_csv(folder + file, dtype=str, encoding='ansi', skiprows=3)

    # # Splitting the df


    # Initialize an empty list to hold the separate DataFrames
    df_list = []

    # Initialize a counter to keep track of the start of each DataFrame
    start_row = 0

    # Loop through the rows in the DataFrame
    for i, row in df.iterrows():

        # Check if the row is completely null
        if row.isnull().all():
            # If so, create a new DataFrame from the previous null row to this one
            new_df = df.iloc[start_row:i]
            
            if len(df_list) > 0 and len(new_df) > 0:
                new_df.columns = new_df.iloc[0]
                new_df = new_df.iloc[1:]
            
            if len(new_df) > 0:
                # Add the new DataFrame to the list
                df_list.append(new_df)

            # Update the start row to the current row + 1
            start_row = i + 1

    dfs = []
    # Assign each DataFrame in the list to a separate variable
    for i, df in enumerate(df_list):
        globals()[f"df_{i+1}"] = df
        dfs.append(df)

    num_df = len(df_list)


    # - `df_2` is the Per Diem Rate df
    # - `df_3` is DRG
    # - `df_4` is APRDRG
    # 


    # # df_1 Stuff


    df_1.rename(columns={
        'EAP Code (Internal Use)': 'local_code',
        'CPT/HCPCS Code': 'code',
        'Procedure Description (Charge)': 'description',
        'Raw 11 Digit NDC or Primary Ext Id': 'ndc',
        'Raw 11 Digit NDC or Primary Ext Id ': 'ndc',
        'Revenue Code': 'rev_code'
    }, inplace=True)


    cols = df_1.columns.tolist()
    # print(cols)
    id_vars = cols[:5]
    value_vars = cols[5:]

    df_1 = pd.melt(df_1, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')


    df_1['payer_category'] = df_1['payer_name'].map(mapping).fillna('payer')


    df_1.loc[df_1['payer_name'].str.lower().str.contains('inpatient'), 'setting'] = 'inpatient'


    df_1['setting'] = np.where(
        df_1['payer_name'].str.lower().str.contains('inpatient'), 'inpatient',
        np.where(
            df_1['payer_name'].str.lower().str.contains('outpatient'), 'outpatient', pd.NA)
    )


    df_1['rev_code'] = df_1['rev_code'].str.zfill(4)


    df_1.dropna(subset='standard_charge', inplace=True)


    # df_1.loc[(~df_1['code'].isna()) & (df_1['code'].str.match(r'^(?:[A-Z][0-9]{4}|[0-9]{5}|[0-9]{4}[A-Z])$')), 'hcpcs_cpt'] = df_1['code']


    # # Classify each DF


    apr_df = False
    drg_df = False
    op_df = False
    op_df1 = False
    per_diem_df = False


    for i, df in enumerate(dfs):
        # if not i:
        #     print(df.columns.tolist())
        if i:
            # Have to remove nan columns
            df.columns = [str(col) if not pd.isna(col) else '' for col in df.columns]
            # print(df.columns.tolist())
            if '' in df.columns:
                df = df.drop([''], axis=1)
            first_col = df.columns[0]
            if first_col == 'DRG Type':
                drg_df = df
            elif first_col == 'APR -DRG':
                apr_df = df
            elif first_col == 'Per Diem Rate':
                per_diem_df = df
            elif first_col == 'OP Type':
                if type(op_df) == bool:
                    op_df = df
                else:
                    op_df1 = df


    # # Per diem df Stuff


    # Have to use type here because dataframes don't have a truth value
    if type(per_diem_df) != bool:
        per_diem_df['contracting_method'] = 'per diem'
        per_diem_df['description'] = 'per diem rate'

        cols = per_diem_df.columns.tolist()
        id_vars = ['description', 'contracting_method']
        value_vars = cols[1:-2]
        per_diem_df = pd.melt(per_diem_df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')
        
        per_diem_df.dropna(subset='standard_charge', inplace=True)

        per_diem_df['payer_category'] = per_diem_df['payer_name'].map(mapping).fillna('payer')


    # # apr-drg df


    # Have to use type here because dataframes don't have a truth value
    if type(apr_df) != bool:
        apr_df.rename(columns={
            'APR -DRG': 'line_type',
            'APRDRG & Severity': 'apr_drg',
            'APR Description': 'description',
        }, inplace=True)

        apr_df.loc[apr_df['apr_drg'].str.len() == 2, 'apr_drg'] = apr_df['apr_drg'].str.zfill(4)
        apr_df['apr_drg'] = apr_df['apr_drg'].str[:3] + '-' + apr_df['apr_drg'].str[-1]

        cols = apr_df.columns.tolist()
        id_vars = cols[:3]
        value_vars = cols[3:]
        
        apr_df = pd.melt(apr_df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')

        apr_df['payer_category'] = apr_df['payer_name'].map(mapping).fillna('payer')
        apr_df.dropna(subset='standard_charge', inplace=True)

        


    # # drg df


    if type(drg_df) != bool:
        drg_df.rename(columns={
            'DRG Type': 'line_type',
            'DRG Code': 'ms_drg',
            'DRG Description': 'description'
        }, inplace=True)

        drg_df['ms_drg'] = drg_df['ms_drg'].str.zfill(3)


        cols = drg_df.columns.tolist()
        id_vars = cols[:3]
        value_vars = cols[3:]
        drg_df = pd.melt(drg_df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')
        drg_df['payer_category'] = drg_df['payer_name'].map(mapping).fillna('payer')
        drg_df.dropna(subset='standard_charge', inplace=True)
        


    # # OP type df


    if type(op_df) != bool:
        op_df.rename(columns={
            'OP Type': 'line_type',
            'OP Code': 'code',
            'OP Description': 'description'
        }, inplace=True)

        cols = op_df.columns.tolist()
        id_vars = cols[:3]
        value_vars = cols[3:]

        op_df = pd.melt(op_df, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')
        op_df['payer_category'] = op_df['payer_name'].map(mapping).fillna('payer')
        
        op_df.loc[op_df['line_type'] == 'APC', 'apc'] = op_df['code'].str.zfill(4)
        op_df.dropna(subset='standard_charge', inplace=True)


    # # OP 1 df


    if type(op_df1) != bool:
        op_df1.rename(columns={
            'OP Type': 'line_type',
            'OP Code': 'code',
            'OP Description': 'description'
        }, inplace=True)

        cols = op_df1.columns.tolist()
        id_vars = cols[:3]
        value_vars = cols[3:]

        op_df1 = pd.melt(op_df1, id_vars=id_vars, value_vars=value_vars, var_name='payer_name', value_name='standard_charge')
        op_df1['payer_category'] = op_df1['payer_name'].map(mapping).fillna('payer')

        op_df1.loc[op_df1['line_type'] == 'EAPG', 'eapg'] = op_df1['code']
        op_df1.dropna(subset='standard_charge', inplace=True)



    # # All dfs


    dfs = [df_1, apr_df, drg_df, op_df, op_df1, per_diem_df]
    dfs = [x for x in dfs if type(x) != bool]


    df = pd.concat(dfs)


    # df['setting'] = np.where(
    #     df['payer_name'].str.lower().str.contains('inpatient'), 'inpatient',
    #     np.where(
    #         df['payer_name'].str.lower().str.contains('outpatient'), 'outpatient', pd.NA)
    # )


    # df['setting'] = np.where(
    #     df['payer_name'].str.lower().str.endswith('IP'), 'inpatient',
    #     np.where(
    #         df['payer_name'].str.lower().str.endswith('OP'), 'outpatient', pd.NA)
    # )

    conditions = [    df['payer_name'].str.lower().str.contains('inpatient'),
    df['payer_name'].str.lower().str.contains('outpatient'),
    df['payer_name'].str.lower().str.contains(' ip | ip$'),
    df['payer_name'].str.lower().str.match(r' op | op$')
    ]

    choices = ['inpatient', 'outpatient', 'inpatient', 'outpatient']

    df['setting'] = np.select(conditions, choices, default=pd.NA)



    df['standard_charge'] = df['standard_charge'].str.replace('$', '', regex=False).str.replace(',', '')


    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    # I do it this way so that I can catch any contracting methods
    df.loc[df['standard_charge'].str.match('#VALUE!|#DIV/0!|#REF!| N/A|N/A|-'), 'standard_charge'] = pd.NA
    df['standard_charge'] = pd.to_numeric(df['standard_charge'])

    df.loc[df['payer_name'].str.contains('IP & OP'), 'setting'] = 'both'

    



    ccn = {
        "documents_standard-charges_41-0695604_Essentia-Health-St.-Marys-Childrens-Hospital_standardcharges.csv": "240002",
        "documents_standard-charges_41-0695602_Essentia-Health-St.-Josephs-Medical-Center_standardcharges.csv": "240075",
        "documents_standard-charges_46-0909870_Essentia-Health-Virginia_standardcharges.csv": "240084",
        "documents_standard-charges_41-1620386_Essentia-Health-St.Marys-Detroit-Lakes_standardcharges.csv": "240101",
        "documents_standard-charges_47-5153885_Essentia-Health-Sandstone_standardcharges.csv": "241309",
        "documents_standard-charges_41-0841441_Essentia-Health-Northern-Pines_standardcharges.csv": "241340",
        "documents_standard-charges_84-5099016_Essentia-Health-Moose-Lake_standardcharges.csv": "241350",
        "documents_standard-charges_41-0706143_Essentia-Health-Fosston_standardcharges.csv": "241357",
        "documents_standard-charges_41-0844574_Essentia-Health-Deer-River_standardcharges.csv": "241360",
        "documents_standard-charges_26-1175213_Essentia-Health-Fargo_standardcharges.csv": "350070",
        "documents_standard-charges_41-1811073_Essentia-Health-St.-Marys-Hospital-Superior_standardcharges.csv": "521329",
        "documents_standard-charges_20-0479568_Essentia-Health-Ada_standardcharges.csv": "241313",
        "documents_standard-charges_41-1878730_Essentia-Health-Duluth_standardcharges.csv": "240019",
        "documents_standard-charges_41-0706143_Essentia-Health-Holy-Trinity-Hospital_standardcharges.csv": "241321"
    }

    id = ccn[file]
    df['hospital_id'] = id

    name = file.split('Essentia-Health-')[-1]
    id



    output_name = id + '_' + name
    df.to_csv('.\\output_files\\' + output_name, index=False)


