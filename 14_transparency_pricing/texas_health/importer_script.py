import os
from tqdm import tqdm
import argparse

def importer(hospital):
    folder = 'G:\\transparency-in-pricing\\'
    
    db_path = 'G:\\transparency-in-pricing\\'   

    if hospital:
        file = os.path.join(folder, hospital)
        os.system(f'cd /D {db_path} & dolt table import -u hospital "{file}"')

    folder = os.path.join(folder, 'output_files')

    for file in os.listdir(folder):
        print('\n', file)
        path = os.path.join(folder, file)
        os.system(f'cd /D {db_path} & dolt table import -u rate "{path}"')

def cli():
    parser = argparse.ArgumentParser(description="Iteratively import data from child folder 'input_files`. Optionally include name of hospital csv to import that as well.")
    parser.add_argument('hospital', type=str, nargs='?', default=False, help="Name of hospital csv to import")
    # parser.add_argument('-f', '--hospital', type=str, required=False, help="Name of hospital csv to import")
    args = parser.parse_args()
    importer(args.hospital)

if __name__ == "__main__":
    cli()