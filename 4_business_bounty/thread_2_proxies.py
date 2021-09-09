from alabama_function_search import alabama_scraper_proxy
from multiprocessing import Pool

def run_parallel():
    one_start = 14776
    two_start = 194671
    three_start = 383882
    four_start = 574507
    five_start = 742313

    list_ranges = [[one_start, 189199, "alabama1.csv", 1], [two_start, 378399,"alabama2.csv", 2], [three_start, 567599, "alabama3.csv", 3], [four_start, 736799, "alabama4.csv", 4], [five_start, 945999, "alabama5.csv", 5]]
    pool = Pool(processes=len(list_ranges))
    pool.map(alabama_scraper_proxy, list_ranges)
    # alabama_scraper()

if __name__ == "__main__":
    run_parallel()
