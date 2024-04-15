from frictionless import validate, Schema
import os

# Define the schema
schema = Schema('rate.schema.yaml')

# Iterate over CSV files in a folder
folder_path = '.\\input_files\\'
for file_path in os.listdir(folder_path):
    if file_path.endswith('.csv'):
        # Validate the file against the schema
        report = validate(f'{folder_path}/{file_path}', schema=schema)
        print(report)
        # Check for errors
        if report.valid:
            print(f'{file_path} is valid')
        else:
            print(f'{file_path} is invalid:')
            for error in report.flatten().errors:
                print(f'- {error.message}')
