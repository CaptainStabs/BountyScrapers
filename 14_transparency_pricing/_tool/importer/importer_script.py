import os
from tqdm import tqdm
import argparse

def importer():
    folder = os.getcwd()
    folder = os.path.join(folder, 'output_files')

    for file in os.listdir(folder):
        print(file)
        path = os.path.join(folder, file)
        os.system(f'cd /D F:\\_Bounty\\transparency-in-pricing\\ & dolt table import -u rate "{path}"')

def cli():
    importer()

if __name__ == "__main__":
    cli()