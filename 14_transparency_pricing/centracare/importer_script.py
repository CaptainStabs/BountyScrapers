import os
from tqdm import tqdm
import argparse

def importer(hospital, drive):
    folder = os.getcwd()

    drive = drive.lower()
    if drive == 'f':
        db_path = 'F:\\_Bounty\\transparency-in-pricing\\'
    elif drive == 'g':
        db_path = 'G:\\transparency-in-pricing\\'

    confirm = input(f'\nData will be imported to the database at {db_path}, continue? y/n ')
    if confirm.lower() == 'y':
        pass
    else:
        os._exit(1)
    

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
    parser.add_argument('drive', type=str, nargs='?', default= 'f', help="Drive letter of db")
    # parser.add_argument('-f', '--hospital', type=str, required=False, help="Name of hospital csv to import")
    args = parser.parse_args()
    importer(args.hospital, args.drive)

if __name__ == "__main__":
    cli()