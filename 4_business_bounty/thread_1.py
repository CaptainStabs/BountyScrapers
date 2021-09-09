from alabama_function_search import alabama_scraper
from multiprocessing import Pool

def run_parallel():
    one_start = 9205
    two_start = 190678
    three_start = 379998
    four_start = 569073
    five_start = 738402

    list_ranges = [[one_start, 189199, "alabama1.csv", 1], [two_start, 378399,"alabama2.csv", 2], [three_start, 567599, "alabama3.csv", 3], [four_start, 736799, "alabama4.csv", 4], [five_start, 945999, "alabama5.csv", 5]]
    try:
        pool = Pool(processes=len(list_ranges))
        pool.map(alabama_scraper, list_ranges)

    except KeyboardInterrupt:
        print("Quitting")
        pool.terminate()
        sys.exit(1)
    # alabama_scraper()

if __name__ == "__main__":
        run_parallel()
