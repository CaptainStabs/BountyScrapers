from idxutils import gen_in_network_links, JSONOpen
from tqdm import tqdm
import pandas as pd
import requests
import csv
import aiofiles
import multiprocessing
import sys
import traceback as tb
from _utils import istarmap



# for i, file in tqdm(enumerate(gen_in_network_links(rates_file)), total=len(df)

def get_network_files(url):
    files = [f for files in gen_in_network_links(url)]
    return files

def get_file_size(session, url):
    return session.head(url).headers.get("Content-Length")

def worker(url, session):
    files = get_network_files(url)
    for file in files:
        size = get_file_size(session, file)
        yield file, size


def apply_parallel(df, func, writer, session):
    try:
        with multiprocessing.Pool(processes=10) as pool:
            for _ in tqdm(pool.istarmap(func, [(row["url"], session) for _, row in df.iterrows()]),desc="Main Process", position=0, total=len(df)):
                print(_)
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
    session = requests.Session()
    with open("uhc_rates.csv", "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["url", "size"])
        df = pd.read_csv("UHC_indexes.csv")

        try:
            results = apply_parallel(df, worker, writer, session)
        except KeyboardInterrupt:
            print("Quitting")
            sys.exit()