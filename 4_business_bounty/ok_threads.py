from ./OK/functionized_ok_scraper import oklahoma_scraper
from multiprocessing import Pool
import pandas as pd

def run_parallel():

    # Could just put these directly into the list_ranges but im lazy
    one_start = 1900091737
    two_start = 1900029239 #id_list[1]
    three_start = 190005840 #id_list[2]
    four_start = 0 #id_list[3]
    five_start = id_list[4]

    list_ranges = [[one_start, 1900029239, "oklahoma_1.csv", 1], [two_start, 190005840,"oklahoma_2.csv", 2], [three_start, 1900087720, "oklahoma_3.csv", 3], [four_start, 1900058480, "oklahoma_4.csv", 4], [5000000000, "oklahoma_5.csv", 5]]
    try:
        pool = Pool(processes=len(list_ranges))
        pool.map(oklahoma_scraper, list_ranges)

    except KeyboardInterrupt:
        print("Quitting")
        pool.terminate()
        sys.exit(1)
    # alabama_scraper()

if __name__ == "__main__":
        run_parallel()
