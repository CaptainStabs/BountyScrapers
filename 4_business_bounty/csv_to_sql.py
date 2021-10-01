import csv
from tqdm import tqdm

# General settings
filename = "C:\\Users\\adria\\github\\BountyScrapers\\4_business_bounty\\RI\\~rhode_island-merge-result-naics_deleted.csv"
table_name = "businesses"

# SQL Update Settings
pk = ["name", "business_type", "state_registered"]
updated_columns = [""]

output_filename = str(filename).strip(".csv") + "_sql.sql"
print(output_filename)

def csv_to_insert(filename, table_name):
    # Count lines in file for tqdm total
    with open(filename, "r") as input_csv:
        line_count = 0
        # Count lines in file
        for line in input_csv.readlines():
            line_count += 1

        # Seek back to 0 to allow csv to read full file
        input_csv.seek(0)

        csv_reader = csv.reader(input_csv, delimiter=",", quotechar='"')

        with open(output_filename, "a", encoding="utf8") as output_file:
            for index, row in tqdm(enumerate(csv_reader), total=line_count):

                # Get the header and parse to fields
                if index == 0:
                    fields = ",".join(row)
                    # print(fields)

                # Every other line
                else:
                    values = str(row).strip("[]")
                    query_statement = f"INSERT INTO {table_name}({fields}) VALUES ({values});\n"
                    output_file.write(query_statement)

def csv_to_update(filename, pk, updated_columns):
    with open(filename, "r") as input_csv:
        line_count = 0
        # Count lines in file
        for line in input_csv.readlines():
            line_count += 1

        # Seek back to 0 to allow csv to read full file
        input_csv.seek(0)

        csv_reader = csv.reader(input_csv, delimiter=",", quotechar='"')

        with open(output_filename, "a", encoding="utf8") as output_file:
            for index, row in tqdm(enumerate(csv_reader), total=line_count):

                # Get the header and parse to fields
                if index == 0:
                    fields = ",".join(row)
                    # print(fields)

                # Every other line
                else:
                    values = str(row).strip("[]")
                    query_statement = f"UPDATE {table_name} SET col1 = 'x',col2 = 'x',col3 = 'x',col4 = 'x' WHERE pk1 = 'x from csv' AND pk2 = 'x from csv' AND pk3 = 'x from csv';);\n"
                    output_file.write(query_statement)
