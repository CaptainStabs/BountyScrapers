import csv
import os
import pandas as pd

columns = ["name", "city", "state", "website"]

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
    "yelp",
    "sacbee",
    "ed-data",
    "high-schools",
    "publiccharters",
    "publicschoolreview",
    "elementaryschools",
    "greatschools",
    "thearcofil",
    "usnews",
    "guardianangelstaffing",
    "wikipedia",
    "mapquest",
    "maps.google",
    "countyoffice",
    "nces.ed.gov",
    "schooldigger",
    "niche",
    "patch",
    "point2homes",
    "zillow"
]

with open("websites_added_short.csv", "r", encoding="utf-8") as input_source:
    df = pd.read_csv(input_source)
    df_columns = list(df.columns)
    data_columns = ",".join(map(str, df_columns))

    with open("cleaned_websites.csv", "a", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=columns)
        if os.stat("cleaned_websites.csv").st_size == 0:
            writer.writeheader()

        with open("dirty_websites.csv", "a", encoding="utf-8") as output2:
            writer2 = csv.DictWriter(output2, fieldnames=columns)
            if os.stat("dirty_websites.csv").st_size == 0:
                writer2.writeheader()


            for index, row in df.iterrows():
                if any(ignored_domain in row["website"] for ignored_domain in ignored_domains):
                    print("dirty")
                    output_dict = {}
                    output_dict["name"] = row["name"]
                    output_dict["city"] = row["city"]
                    output_dict["state"] = row["state"]
                    output_dict["website"] = ""
                    writer2.writerow(output_dict)

                else:
                    # print("clean")
                    output_dict = {}
                    output_dict["name"] = row["name"]
                    output_dict["city"] = row["city"]
                    output_dict["state"] = row["state"]
                    output_dict["website"] = row["website"]

                    writer.writerow(output_dict)
