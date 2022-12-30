import multiprocessing
import pandas as pd
from mrfutils_v2 import import_csv_to_set, json_mrf_to_csv
from multiprocessing import Pool, Manager
import sys
import traceback as tb
import argparse
from tqdm import tqdm
from _utils import istarmap

# def master_function(url, out, lock):
#     id = multiprocessing.current_process()._identity[0]
#     out = "./output/" + out
#     try:
#         json_mrf_to_csv(loc=str(url), url=str(url), npi_filter=import_csv_to_set("quest/npis.csv"), code_filter= import_csv_to_set("quest/codes.csv"), out_dir=out, pos=id, lock=lock)

#     except KeyboardInterrupt:
#         raise KeyboardInterrupt
    
#     except:
#         print(url, "\n", id)
#         tb.print_exc()

def master_function(url, out, lock):
    id = multiprocessing.current_process()._identity[0]
    out = "./output/" + out
    try:
        json_mrf_to_csv(loc=str(url), url=str(url), npi_filter=import_csv_to_set("quest/npis.csv"), code_filter= import_csv_to_set("quest/codes.csv"), out_dir=out, pos=id, lock=lock)

    except:
        print(url, "\n", id)
        tb.print_exc()

def apply_parallel(df, func, out):
    lock = Manager().Lock()
    # with multiprocessing.Pool(processes=6) as pool:
    try:
        pool = multiprocessing.Pool(processes=6)
        for _ in tqdm(pool.istarmap(func, [(row["url"], out, lock) for _, row in df.iterrows()]), desc="Main Process", position=0, total=len(df.index)):
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
        sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default="_input_csvs/first_100.csv")
    parser.add_argument('-o', '--out', default = 'test_100')
    args = parser.parse_args()
    out = args.out


    df = pd.read_csv(args.input)
    df = df.sort_values(by=["size"])
    apply_parallel(df, master_function, out)
