import pandas as pd
import requests


def url_check(url):
    try:
        r = requests.get(url)

        if r.status_code == 200:
            return url
        else:
            return pd.NA
    except:
        raise
        return pd.NA

df = df.read_csv("extracted_data.csv")

df["source_2"] = df["source_2"].apply(lambda x: url_check[x])

df.to_csv("extracted_data2.csv", index=False)
