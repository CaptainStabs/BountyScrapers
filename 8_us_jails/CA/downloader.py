import csv
import sys
from tqdm import tqdm
import argparse

def csv_to_insert(filename, table_name):
    output_filename = str(filename).strip(".csv") + "_sql.sql"
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
                if not index:
                    fields = ",".join(row)
                    continue
                    # print(fields)

                # Every other line
                else:
                    values = str(row).strip("[]")
                    query_statement = f"INSERT INTO {table_name}({fields}) VALUES ({values});\n"
                    output_file.write(query_statement)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert CSV to SQL inserts')
    parser.add_argument('--f', type=str, help='Path to CSV, output will be same location')
    parser.add_argument('--tn', type=str, help='Table name')
    args = parser.parse_args()
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    csv_to_insert(args.f, args.tn)
