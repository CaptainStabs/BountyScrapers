from alabama_function_search import alabama_scraper_proxy
from multiprocessing import Pool
import pandas as pd

def run_parallel():
    id_list = []
    for i in range(1,6): # Open alabama(x).csv
        df = pd.read_csv(f"alabama{i}.csv")
        df_columns = list(df.columns)
        data_columns = ",".join(map(str, df_columns))

        # Get the last row from df
        last_row = df.tail(1)
        # Access the corp_id
        last_id = last_row["corp_id"].values[0]
        id_list.append(last_id)

    # Could just put these directly into the list_ranges but im lazy
    one_start = id_list[0]
    two_start = id_list[1]
    three_start = id_list[2]
    four_start = id_list[3]
    five_start = id_list[4]

    list_ranges = [[one_start, 189199, "alabama1.csv", 1], [two_start, 378399,"alabama2.csv", 2], [three_start, 567599, "alabama3.csv", 3], [four_start, 736799, "alabama4.csv", 4], [five_start, 945999, "alabama5.csv", 5]]
    pool = Pool(processes=len(list_ranges))
    pool.map(alabama_scraper_proxy, list_ranges)
    # alabama_scraper()

if __name__ == "__main__":
    run_parallel()
