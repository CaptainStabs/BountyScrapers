import multiprocessing
import pandas as pd
from mrfutils.flatteners import toc_file_to_csv
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
log = logging.getLogger('mrfutils')
log.setLevel(logging.WARNING)


#  python cli_multi.py -i input_csvs\UHC_payers_sorted.csv -mp True -he 300 -b UHC_4 -o UHC_4 -cm "300 UHC files"
# define the master function that will be applied in parallel
def work(url, out):
    try:
        id = multiprocessing.current_process()._identity[0]
        out = "\\".join([out, str(id)]) + "\\"
        url = "https://storage.googleapis.com/cms-humana-price-transparency-prd/prod/february/inn/" + url.strip("\n")
        # url = "https://developers.humana.com/Resource/DownloadPCTFile?fileType=innetwork&fileName=" + url.strip("\n")
        if not os.path.exists(out):
            os.makedirs(out)
        
        try:
            toc_file_to_csv(url=str(url), out_dir=out)
        except EOFError:
            print(f"\n!!!EOFError: {url}")
        except Exception as e:
            tb.print_exc()
            print(f"\n{e}: {url}")
     
    except:
        tb.print_exc()  # print the traceback for the exception
        print("CRASH URL:", url, "\n", "ID:", id)
        pass


# define the apply_parallel function that applies the master function in parallel
def apply_parallel(df, func, out, processes):
    try:
        # create a pool with 10 processes
        with multiprocessing.Pool(processes=processes) as pool:
            # apply the work function in parallel using the pool and tqdm to display progress
            # loop is for istarmap
            for _ in tqdm(pool.istarmap(func, [(row["url"], out) for _, row in df.iterrows()]), desc="Main Process", position=0, total=len(df)):
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
    parser.add_argument('-i', '--input', default=".\\humana_tools\\files.txt")
    parser.add_argument('-o', '--out', default = 'F:\\_Bounty\\humana_toc')
    parser.add_argument('-p', '--processes', default=10, type=int)
    
    # Parse the arguments
    args = parser.parse_args()
    try:
        # Read the input csv file into a pandas dataframe
        df = pd.read_csv(args.input)
        # sort the dataframe by the 'size' column
        # apply the work function in parallel using apply_parallel
        results = apply_parallel(df, work, args.out, args.processes)
        send_mail("Finsihed", "Finished")
            
    except KeyboardInterrupt:
        print("Quitting")
        sys.exit()