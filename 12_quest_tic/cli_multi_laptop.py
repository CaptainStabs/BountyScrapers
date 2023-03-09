import multiprocessing
import pandas as pd
from mrfutils import json_mrf_to_csv
from _utils.mrf.helpers import import_csv_to_set
from multiprocessing import Pool, Manager
import sys
import traceback as tb
import argparse
from tqdm import tqdm

from _utils import istarmap
from _utils.send_mail import send_mail
from _utils.make_pr import make_pr

import os


# define the master function that will be applied in parallel
def work(url, out):
    try:
        id = multiprocessing.current_process()._identity[0]
        out = out + str(id) + "\\"

        if not os.path.exists(out):
            os.makedirs(out)
         # call the json_mrf_to_csv function with the given arguments

        tries = 0
        while tries < 2:
            try:
                json_mrf_to_csv(url=str(url), npi_filter=import_csv_to_set("./quest/npis.csv"), code_filter= import_csv_to_set("./quest/codes.csv"), out_dir=out)
                tries = 6
            except EOFError:
                print(f"\n!!!EOFError: {url}")
                print(f"\nRetrying, try: {tries}")
                tries += 1
            except Exception as e:
                print(f"\n{e}: {url}")
                print(f"\nRetrying, try: {tries}")
                tries += 1
     
    except:
        print(url, "\n", id)
        tb.print_exc()  # print the traceback for the exception
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
    # parser.add_argument('-o', '--out', default = 'test_100')
    parser.add_argument('-mp', '--make_pr', default=False)
    parser.add_argument('-he', '--head', default=100, type=int)
    parser.add_argument('-b', '--branch')
    parser.add_argument('-cm', '--commit_message')
    parser.add_argument('-p', '--processes', default=10, type=int)
    
    # Parse the arguments
    args = parser.parse_args()
    print(args.branch, args.commit_message)

    out = os.path.join("output", args.branch)
    out = out + "\\"
    
    try:
        # Read the input csv file into a pandas dataframe
        df = pd.read_csv(args.input)
        # sort the dataframe by the 'size' column
        if "size" in df.columns:
            df = df.sort_values(by=["size"])

        # df = df.iloc[1498:]
        df = df.head(args.head)
        # apply the work function in parallel using apply_parallel
        results = apply_parallel(df, work, out, args.processes)
        if args.make_pr:
            out = os.path.join("C:\\Users\\adria\\github\\BountyScrapers\\12_quest_tic\\", out)
            os.system(f'cd C:\\Users\\adria\\_Bounty\\quest-v3\\ & import_folders_push.bat {out} "{args.commit_message}" {args.branch} {args.processes}')
            make_pr(title=args.commit_message, branch=args.branch)
            send_mail(f"Finished {args.branch}", "Finished")
        else:
            send_mail("Finsihed", "Finished")
            
    except KeyboardInterrupt:
        print("Quitting")
        sys.exit()