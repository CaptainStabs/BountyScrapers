import requests
import os
import pandas as pd
import googlesearch as google
import csv
import time
import sys


ignored_domains = [
    "facebook",
    "twitter",
    "linkedin",
    "instagram",
    "youtube",
    "tiktok",
    "pinterest",
    "reddit",
    "wicz",
    "krtv",
    "foxnews",
    "wsbtv",
    "cnbc",
    "cbs",
    "nytimes",
]
print("   [*] Opening Source File...")
with open("HIFLD_Schools.csv", "r", encoding="utf-8") as input_source:
    print("      [*] Reading csv")
    df = pd.read_csv(input_source)
    df_columns = list(df.columns)
    data_columns = ",".join(map(str, df_columns))

    print("         [*] Opening output file...")
    with open("websites_added.csv", "a", encoding="utf-8") as file_out:
        print("            [*] Starting loop")
        for index, row in df.iterrows():
            try:
                school_name = row["name"]
                no_error = True
            except KeyError:
                print(f"            [!] Error on index: {index}")
                no_error = False
                pass

            found = False

            if no_error:
                while not found:
                    print("         [*] Starting search loop...")
                    try:
                        
