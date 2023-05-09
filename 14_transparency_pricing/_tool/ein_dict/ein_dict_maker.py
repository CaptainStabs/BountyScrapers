import pandas as pd
import argparse
import json

def ein_dict(file):
    df = pd.read_csv(file, dtype=str)
    ein_ccn_dict = dict(zip(df['file_name'], df['id']))
    print(json.dumps(ein_ccn_dict, indent=4))

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, nargs='?', help='input file', const='hospital.csv', default='hospital.csv')
    args = parser.parse_args()
    ein_dict(args.file)

if __name__ == '__main__':
    cli()