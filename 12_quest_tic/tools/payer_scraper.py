import multiprocessing
import pandas as pd
from mrfutils import import_csv_to_set, json_mrf_to_csv
from threading import Thread
import sys
import traceback as tb
import argparse
from tqdm import tqdm
from _utils import istarmap



def master_function(url):
    url =url.strip("\n")
    out = "output\\payers\\"
    id = multiprocessing.current_process()._identity[0] + 1
    url = url.strip().strip("\n")
    try:
        json_mrf_to_csv(loc=str(url), url=str(url), npi_filter=import_csv_to_set("C:\\Users\\adria\\github\\data-analysis\\transparency-in-coverage\\python\\processors\\quest\\npis.csv"), code_filter= import_csv_to_set("C:\\Users\\adria\\github\\data-analysis\\transparency-in-coverage\\python\\processors\\quest\\codes.csv"), out_dir=out)

    except:
        print(url, "\n", id)
        tb.print_exc()
        


def apply_parallel(file, func):
    # f.seek(100000)
    try:
        with multiprocessing.Pool(processes=5) as pool:
            for _ in tqdm(pool.imap(func, file), description="Main Process", position=0, total=61996706-100000):
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
    
    try:
        file = "F:\\_Bounty\\deduped_payers_utf.txt"
        with open(file, 'r', encoding="utf-16") as f:
            results = apply_parallel(f, master_function)
    except KeyboardInterrupt:
        print("Quitting")
        sys.exit()