from alabama_function_search import alabama_scraper_proxy
from multiprocessing import Pool

def run_parallel():
    list_ranges = [[7630, 189199, "alabama1.csv", 1], [189199, 378399,"alabama2.csv", 2], [378399, 567599, "alabama3.csv", 3], [567599, 736799, "alabama4.csv", 4], [736799, 945999, "alabama5.csv", 5]]
    pool = Pool(processes=len(list_ranges))
    pool.map(alabama_scraper_proxy, list_ranges)
    # alabama_scraper()

if __name__ == "__main__":
    run_parallel()
