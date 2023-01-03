import multiprocessing
import pandas as pd
from official_mrfutils import import_csv_to_set, json_mrf_to_csv
from multiprocessing import Pool, Manager
import sys
import traceback as tb
import argparse
from tqdm import tqdm
from _utils import istarmap



def master_function(url, out):
    out = "output\\payers\\"
    id = multiprocessing.current_process()._identity[0] + 1
    try:
        json_mrf_to_csv(loc=str(url), url=str(url), npi_filter=import_csv_to_set("C:\\Users\\adria\\github\\data-analysis\\transparency-in-coverage\\python\\processors\\quest\\npis.csv"), code_filter= import_csv_to_set("C:\\Users\\adria\\github\\data-analysis\\transparency-in-coverage\\python\\processors\\quest\\codes.csv"), out_dir=out)

    except:
        print(url, "\n", id)
        tb.print_exc()


def apply_parallel(file, func, out):
    with open(file, "r") as f:
        f.seek(100000)
        try:
            with multiprocessing.Pool(processes=1) as pool:
                for _ in tqdm(pool.istarmap(func, [row for row in f]), desc="Main Process", position=0, total=61996706-100000):
                    pass
                pool.close()
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default="_input_csvs/first_100.csv")
    parser.add_argument('-o', '--out', default = 'test_100')
    args = parser.parse_args()
    out = args.out

    try:
        file = "F:\\_Bounty\\deduped_payers.txt"
        # df = df.sort_values(by=["size"])
        results = apply_parallel(file, master_function, out)
    except KeyboardInterrupt:
        print("Quitting")
        sys.exit()