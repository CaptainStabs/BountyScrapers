import multiprocessing
import pandas as pd
from mrfutils.flatteners import import_csv_to_set, in_network_file_to_csv
import sys
import traceback as tb
import argparse
from tqdm import tqdm
from _utils import istarmap


# define the master function that will be applied in parallel
def work(url, out):
    try:
        print(out)
         # call the json_mrf_to_csv function with the given arguments
        in_network_file_to_csv(url=str(url), out_dir=out, code_filter=import_csv_to_set(".\\codes\\70_shoppables.csv"), npi_filter=import_csv_to_set(".\\codes\\npis.csv"))
    except KeyboardInterrupt:
        raise
    except:
        print(url, "\n", id)
        tb.print_exc()  # print the traceback for the exception


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
        
        # apply the work function in parallel using apply_parallel
        for url in tqdm(df["url"]):
            work(url, args.out)
    except KeyboardInterrupt:
        print("Quitting")
        sys.exit()