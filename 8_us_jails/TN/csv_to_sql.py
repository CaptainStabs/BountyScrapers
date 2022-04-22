import csv
from tqdm import tqdm

# General settings
filename = "extracted_data.csv"
table_name = "inmate_population_snapshots"

# SQL Update Settings
pk = ["name", "business_type", "state_registered"]
updated_columns = ["street_registered",	"city_registered",	"zip5_registered",	"state_physical",	"street_physical",	"city_physical",	"zip5_physical",	"filing_number"]
fieldnames = ["name",	"business_type",	"state_registered",	"street_registered",	"city_registered",	"zip5_registered",	"state_physical",	"street_physical",	"city_physical",	"zip5_physical",	"filing_number"]#,	"public",	"naics_2017",	"ein",	"sic4",	"parent",	"website", "duns"]

output_filename = str(filename).strip(".csv") + "_sql.sql"
print(output_filename)

def csv_to_insert(filename, table_name):
    # Count lines in file for tqdm total
    with open(filename, "r", encoding="utf-8") as input_csv:
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

def csv_to_update(filename, table_name, pk, updated_columns, fieldnames):
    with open(filename, "r", encoding="utf-8") as input_csv:
        line_count = 0
        # Count lines in file
        for line in input_csv.readlines():
            line_count += 1

        # Seek back to 0 to allow csv to read full file
        input_csv.seek(0)

        csv_reader = csv.DictReader(input_csv, fieldnames=fieldnames)

        with open(output_filename, "a", encoding="utf8") as output_file:
            for index, row in tqdm(enumerate(csv_reader), total=line_count):

                # Get the header and parse to fields
                # print(row)
                if index == 0:
                    fields = ",".join(row)
                    # print(fields)

                # Every other line
                else:

                    values = str(row).strip("[]")
                    set_statement_list = []
                    for i in range(len(updated_columns)):
                        column_to_update = updated_columns[i]
                        set_statement_list.append(f"{column_to_update} = '{row[column_to_update]}'")

                    set_statements = ",".join(set_statement_list)
                    query_statement = f"UPDATE {table_name} SET " + str(set_statements) + f" WHERE {pk[0]} = '{row['name']}' and {pk[1]} = '{row['business_type']}' and {pk[2]} = '{row['state_registered']}';\n"
                    output_file.write(query_statement)

# csv_to_update(filename, table_name, pk, updated_columns, fieldnames)
csv_to_insert(filename, table_name)
