import pandas as pd
import requests
from tqdm import tqdm

tqdm.pandas()


def url_check(url):
    try:
        r = requests.head(url)

        if r.status_code == 302:
            return url
        else:
            return pd.NA

    except KeyboardInterrupt:
        import sys; sys.exit()

    except:
        # raise
        return pd.NA

df = pd.read_csv("extracted_data1.csv")

s = requests.Session()
df["source_2"] = df["source_2"].progress_apply(lambda x: url_check(x))

df.to_csv("extracted_data2.csv", index=False)
