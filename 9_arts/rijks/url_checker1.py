# import pandas as pd
import csv
import requests
import os
from tqdm import tqdm


def url_check(url, s):
    try:
        r = s.head(url)
        if r.status_code == 302:
            return url
        else:
            return
    except KeyboardInterrupt:
        import sys; sys.exit()
    except:
        raise
        return

# df = df.read_csv("extracted_data.csv")
#
# df["source_2"] = df["source_2"].apply(lambda x: url_check[x])

filename = "extracted_data2.csv"
s = requests.Session()
with open("extracted_data1.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    cols = reader.fieldnames
    with open(filename, "a", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=cols)

        if os.stat(filename).st_size == 0:
            writer.writeheader()

        for row in tqdm(reader, total=198931):
            row["source_2"] = url_check(row["source_2"], s)
            writer.writerow(row)
