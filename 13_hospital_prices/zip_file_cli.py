import os
import sys
import zipfile
import pandas as pd
from mrfutils.flatteners import in_network_file_to_csv
from mrfutils.helpers import import_csv_to_set
import sys
import traceback as tb
import argparse
from tqdm import tqdm

from _utils import istarmap
from _utils.send_mail import send_mail
from _utils.make_pr import make_pr

import os

import logging
logging.basicConfig()
log = logging.getLogger('flatteners')
log.setLevel(logging.WARNING)

def main(args, filename, zip_file):
    # filename is file inside zip_file
    in_network_file_to_csv(url=args.url, out_dir=args.out, file=filename, zip_file=zip_file, code_filter=import_csv_to_set(".\\codes\\70_shoppables.csv"), npi_filter=import_csv_to_set(".\\codes\\npis.csv"))


if __name__ == '__main__':
    # create an argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url')
    parser.add_argument('-f', '--file')
    parser.add_argument('-o', '--out')
    
    # Parse the arguments
    args = parser.parse_args()
    
    with zipfile.ZipFile(args.file) as z:    
        for filename in tqdm(z.namelist()):
            try:
                    
            except:
                tb.print_exc()
                pass
