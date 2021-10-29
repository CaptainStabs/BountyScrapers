from min_finder_function import find_min
from multiprocessing import Pool
import pandas as pd
import sys

def run_parallel():
    id_list = []

    # Could just put these directly into the list_ranges but im lazy
    one_start = 0
    two_start = 300000000
    three_start = 600000000
    four_start = 900211911
    five_start = 1200000000

    # Five found : 1200005665

    list_ranges = [[one_start, 300000000, 1], [two_start,  600000000, 2], [three_start, 900000000, 3], [four_start, 1200000000, 4]]#, [five_start, 1500000000, 5]]
    try:
        pool = Pool(processes=len(list_ranges))
        pool.map(find_min, list_ranges)

    except KeyboardInterrupt:
        print("Quitting")
        pool.terminate()
        sys.exit(1)
    # alabama_scraper()

if __name__ == "__main__":
        run_parallel()
