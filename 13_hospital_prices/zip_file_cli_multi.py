import os
import sys
import zipfile
import pandas as pd
import multiprocessing
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

def work(url, filename, zip_file, out):
    try:
        id = multiprocessing.current_process()._identity[0]
        out = "\\".join([out, str(id)]) + "\\"
        if not os.path.exists(out):
            os.makedirs(out)
        try:
            # filename is file inside zip_file
            print(filename)
            in_network_file_to_csv(url=url, out_dir=out, file=filename, zip_file=zip_file, code_filter=import_csv_to_set(".\\codes\\70_shoppables.csv"), npi_filter=import_csv_to_set(".\\codes\\npis.csv"))
        except EOFError:
            print("EOFError:", filename)

        except:
            tb.print_exc()
            print("Error:", filename)
        finally:
            pass
    except:
        tb.print_exc()


def apply_parallel(url, zip_file, out, func, processes):
    try:
        # create a pool with 10 processes
        with multiprocessing.Pool(processes=processes) as pool:
            # apply the work function in parallel using the pool and tqdm to display progress
            # loop is for istarmap
            with zipfile.ZipFile(args.file) as z:
                name_list = z.namelist()
                for _ in tqdm(pool.istarmap(func, [(url, filename, zip_file, out) for filename in name_list]), desc="Main Process", position=0, total=len(name_list)):
                    pass
                pool.close()

    # catch sigint to prevent unstoppable crash
    except KeyboardInterrupt:
        print("Quitting")
        pool.terminate() 
        sys.exit()
    
    except Exception:
        pool.terminate()
        tb.print_exc()
        raise

    finally:
        pool.join()

if __name__ == '__main__':
    # create an argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url')
    parser.add_argument('-f', '--file')
    parser.add_argument('-o', '--out')
    parser.add_argument('-p', '--processes', type=int, default=10)
    
    # Parse the arguments
    args = parser.parse_args()
    results = apply_parallel(url=args.url, zip_file=args.file, out=args.out, func=work, processes=args.processes)
