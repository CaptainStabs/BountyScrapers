import pandas as pd
import os


def test(df):
    checked_urls = []
    for x in df:
        if x == "cdm3" or x == "hpg1":
            x = pd.NA
        checked_urls.append(x)
        print(checked_urls)
    return checked_urls


df = pd.read_csv("non-null copy.csv")
cdu, ciu, hpg = "cdm_url", "cdm_indirect_url", "homepage"
df[[cdu, hpg, ciu]] = df[[cdu, hpg, ciu]].apply(test)
print(df)

