import requests
import os
import pandas as pd
import csv
import sys

ignored_strings = [
    "http://www.dss.state.la.us/directory/office/",
    "police1",
    "bethalto",
    "bayouvista",
    "boro.dormont",
    "cherokeecounty",
    "christiancountyky",
    "chittendencountysheriff.com",
    "ci.pinckneyville.il.us",
    "cityofdeerwood",
    "cityofdeerwood",
    "cityofmontesano",
    "burleson",
    "co.harrison.ms.us",
    "crescenttownship",
    "daphneal",
    "dcin.ncsbi.gov",
    "duquoin",
    "delawarecounty.iowa.gov",
    "edwardsburg",
    "expositionpark",
    "fice.loyno"

]
with open("agencies_cleaned.csv", "r", encoding="utf-8") as input_source:
    df = pd.read_csv(input_source)
    # access the dataframe columns
    df_columns = list(df.columns)
    # join the returned list to format as csv header
    data_columns = ",".join(map(str, df_columns))

    # with open("agencies_cleaned_deduplicated.csv", "a", encoding="utf-8") as cleaned_output:
    duplicates = df.duplicated(subset=["homepage_url"])
    max_loop = 0

    for index, bool in enumerate(duplicates):
        pos_index = index - 2
        if bool:
            index_url = df.loc[pos_index]["homepage_url"]
            if not any(
                ignored_string in str(index_url) for ignored_string in ignored_strings
            ):
                print(index, index_url)
                max_loop = max_loop + 1
                # print(max_loop)
        if max_loop >= 10:
            break
