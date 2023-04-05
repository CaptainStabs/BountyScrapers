import multiprocessing
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


#  python cli_multi.py -i input_csvs\UHC_payers_sorted.csv -mp True -o UHC_4 -he 300 -cm "300 UHC files"
# define the master function that will be applied in parallel
def work(url, out):
    try:
        id = multiprocessing.current_process()._identity[0]
        out = "\\".join(["output", out, str(id)]) + "\\"

        if not os.path.exists(out):
            os.makedirs(out)
         # call the json_mrf_to_csv function with the given arguments

        # tries = 0
        # while tries < 2:
        #     try:
        #         in_network_file_to_csv(url=str(url), out_dir=out, code_filter=import_csv_to_set(".\\codes\\70_shoppables.csv"), npi_filter=import_csv_to_set(".\\codes\\npis.csv"))
        #         tries = 6
        #     except EOFError:
        #         print(f"\n!!!EOFError: {url}")
        #         print(f"\nRetrying, try: {tries}")
        #         tries += 1
        #     except Exception as e:
        #         tb.print_exc()
        #         print(f"\n{e}: {url}")
        #         print(f"\nRetrying, try: {tries}")
        #         tries += 1
        
        try:
            in_network_file_to_csv(url=str(url), out_dir=out, code_filter=import_csv_to_set(".\\codes\\70_shoppables.csv"), npi_filter=import_csv_to_set(".\\codes\\npis.csv"))
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
    parser.add_argument('-i', '--input', default="_input_csvs/first_100.csv")
    parser.add_argument('-o', '--out', default = 'test_100')
    parser.add_argument('-mp', '--make_pr', default=False)
    parser.add_argument('-he', '--head', default=100, type=int)
    parser.add_argument('-b', '--branch') # If left null out will be used as branch name
    parser.add_argument('-cm', '--commit_message')
    parser.add_argument('-p', '--processes', default=10, type=int)
    
    # Parse the arguments
    args = parser.parse_args()
    print(args.branch, args.commit_message)

    if args.make_pr and not args.branch:
        args.branch = args.out

    
    try:
        # Read the input csv file into a pandas dataframe
        df = pd.read_csv(args.input)
        # sort the dataframe by the 'size' column
        if "size" in df.columns:
            df = df.sort_values(by=["size"])

        # df = df.iloc[1498:]
        df = df.head(args.head)
        # apply the work function in parallel using apply_parallel
        results = apply_parallel(df, work, args.out, args.processes)
        if args.make_pr:
            out = os.path.join("C:\\Users\\adria\\github\\BountyScrapers\\13_hospital_prices\\output\\", args.out)
            os.system(f'cd /D F:\\_Bounty\\hospital-prices-allpayers\\ & import_folders_push.bat {out} "{args.commit_message}" {args.branch} {args.processes}')
            make_pr(title=args.commit_message, branch=args.branch)
            send_mail(f"Finished {args.branch}", "Finished")
        else:
            send_mail("Finsihed", "Finished")
            
    except KeyboardInterrupt:
        print("Quitting")
        sys.exit()