import os
import pandas as pd

# Define the schema
schema = {
    'hospital_id': 'object',
    'row_id': 'uint64',
    'line_type': 'object',
    'description': 'object',
    'rev_code': 'object',
    'local_code': 'object',
    'code': 'object',
    'ms_drg': 'object',
    'apr_drg': 'object',
    'eapg': 'object',
    'hcpcs_cpt': 'object',
    'modifiers': 'object',
    'thru': 'object',
    'apc': 'object',
    'icd': 'object',
    'ndc': 'object',
    'drug_hcpcs_multiplier': 'Int64',
    'drug_quantity': 'object',
    'drug_unit_of_measurement': 'object',
    'drug_type_of_measurement': pd.CategoricalDtype(categories=['gr', 'mg', 'ml', 'un']),
    'billing_class': pd.CategoricalDtype(categories=['professional', 'facility']),
    'setting': pd.CategoricalDtype(categories=['inpatient', 'outpatient', 'both']),
    'payer_category': pd.CategoricalDtype(categories=['gross', 'cash', 'min', 'max', 'payer']),
    'payer_name': 'object',
    'plan_name': 'object',
    'standard_charge': 'float64',
    'standard_charge_percent': 'float64',
    'contracting_method': pd.CategoricalDtype(categories=['capitation', 'case rate', 'fee schedule', 'percent of total billed charge', 'per diem', 'other']),
    'additional_generic_notes': 'object',
    'additional_payer_specific_notes': 'object'
}


# Define the validation rules
validation_rules = {
    'payer_category': {
        'condition': lambda x: not (x == 'payer' and ('gross' in column_name or column_name in ['price', 'charge'])) if pd.notna(x) else False,
        'message': 'Invalid value for payer_category'
    },
    'standard_charge': {
        'condition': lambda x: pd.to_numeric(x, errors='coerce').notnull().all(),
        'message': 'Invalid value for standard_charge'
    }
}

# Define the folder path
folder_path = './input_files/'

# Iterate over the CSV files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(os.path.join(folder_path, file_name), dtype=schema)

        # Validate the DataFrame according to the rules
        for column_name, rule in validation_rules.items():
            try:
                if not df[column_name].apply(rule['condition']).all():
                    print(f'Validation error in {file_name}: {rule["message"]} for column {column_name}')
            except KeyError:
                print(f'Validation error in {file_name}: {rule["message"]} for missing column {column_name}')
            except Exception as e:
                print(f'Validation error in {file_name}: {str(e)} for column {column_name}')