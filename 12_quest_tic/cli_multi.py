import multiprocessing
import pandas as pd
from mrfutils import json_mrf_to_csv
from _mrf_stuff.helpers import import_csv_to_set
from multiprocessing import Pool, Manager
import sys
import traceback as tb
import argparse
from tqdm import tqdm
from _utils import istarmap
from _utils import send_mail

import os


# define the master function that will be applied in parallel
def work(url, out):
    try:
        id = multiprocessing.current_process()._identity[0]
        out = out + str(id) + "\\"

        if not os.path.exists(out):
            os.makedirs(out)
         # call the json_mrf_to_csv function with the given arguments
        json_mrf_to_csv(url=str(url), npi_filter=import_csv_to_set("./quest/npis.csv"), code_filter= import_csv_to_set("./quest/codes.csv"), out_dir=out)
     
    except:
        print(url, "\n", id)
        tb.print_exc()  # print the traceback for the exception
        pass


# define the apply_parallel function that applies the master function in parallel
def apply_parallel(df, func, out):
    try:
        # create a pool with 10 processes
        with multiprocessing.Pool(processes=10) as pool:
            # apply the work function in parallel using the pool and tqdm to display progress
            # loop is for istarmap
            for _ in tqdm(pool.istarmap(func, [(row["url"], out) for _, row in df.iterrows()]), desc="Main Process", position=0, total=len(df)):
                pass
            pool.close()
            send_mail("Finished", "Finished")

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
    # Parse the arguments
    args = parser.parse_args()
    
    try:
        # Read the input csv file into a pandas dataframe
        df = pd.read_csv(args.input)
        # sort the dataframe by the 'size' column
        if "size" in df.columns:
            df = df.sort_values(by=["size"])

        df = df.iloc[500:]
        df = df.head(500)
        # apply the work function in parallel using apply_parallel
        results = apply_parallel(df, work, args.out)
    except KeyboardInterrupt:
        print("Quitting")
        sys.exit()