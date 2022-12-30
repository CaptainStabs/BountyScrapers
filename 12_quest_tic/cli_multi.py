import multiprocessing
import pandas as pd
from mrfutils import import_csv_to_set, json_mrf_to_csv
from multiprocessing import Pool, Manager
import sys
import traceback as tb
import argparse
from tqdm import tqdm



def master_function(url, out):
    id = multiprocessing.current_process()._identity[0] + 1
    try:
        json_mrf_to_csv(loc=str(url), url=str(url), npi_filter=import_csv_to_set("quest/npis.csv"), code_filter= import_csv_to_set("quest/codes.csv"), out_dir=out, pos=id)

    except KeyboardInterrupt:
        raise KeyboardInterrupt
    
    except:
        print(url, "\n", id)
        tb.print_exc()


def apply_parallel(df, func, out):
    with multiprocessing.Pool(processes=6) as pool:
        try:
            tqdm(pool.istarmap(func, [(row["url"], out) for _, row in df.iterrows()]), desc="Main Process", position=0)
            pool.close()
        except KeyboardInterrupt:
            print("Quitting")
            pool.terminate()
            sys.exit()
        
        except:
            pool.terminate()
            tb.print_exc()

        finally:
            pool.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default="_input_csvs/first_100.csv")
    parser.add_argument('-o', '--out', default = 'first_100')
    args = parser.parse_args()
    out = args.out

    try:
        df = pd.read_csv(args.input)
        df = df.sort_values(by=["size"])
        results = apply_parallel(df, master_function, out)
    except KeyboardInterrupt:
        print("Quitting")
        sys.exit()