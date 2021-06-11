import requests
import os
import pandas as pd
import googlesearch as google
import csv
import time
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
    "whitepages",
    "police1",
    "claimspages",
]
with open("duplicates_csved.csv", "r", encoding="utf-8") as input_source:
    df = pd.read_csv(input_source)
    # access the dataframe columns
    df_columns = list(df.columns)
    # join the returned list to format as csv header
    data_columns = ",".join(map(str, df_columns))

    with open("agencies_updated_urls.csv", "a", encoding="utf-8") as cleaned_output:
        for index, row in df.iterrows():
            # print("inside loop")
            try:
                department_name = str(row["name"]) + " " + str(row["state_iso"])
                no_error = True
            except KeyError:
                print("        [!] Error on index: " + str(index))
                no_error = False
                pass

            found = False
            # prevent NameError from ocurring if the `department_name` was not extracted for some reason.
            if no_error:
                num_tries = 0
                not_found = False
                while not found:
                    print("    [*] Searching...")
                    # iterate through the results returned by search (search loop)
                    try:
                        for results in google.search(
                            department_name,
                            tld="com",
                            lang="en",
                            num=10,
                            start=0,
                            stop=5,
                            pause=2.0,
                        ):
                            if any(
                                ignored_domain in results
                                for ignored_domain in ignored_domains
                            ):
                                print(
                                    "      [*] Haven't found it yet. URL: "
                                    + results
                                )
                                found = False
                                num_tries += 1
                                continue
                            else:
                                print("      [*] Found it! URL: " + results)
                                found = True
                                break

                            # if found, break the search loop
                            if found:
                                break
                            if num_tries >= 3:
                                not_found = True
                                print("      [*] Couldn't find it.")
                    except Exception as e:
                        print(e)
                        message_data = "Your code crashed. Error: " + str(e)
                        response = requests.post(
                            "https://notify.run/3GXNtgh04xOuLknE", data=message_data
                        )
                        break

                # print("      " + results)
                print("                   Name: " + str(row["name"]) + "\n")
                print("      [*] Writing results")
                # Access the homepage_url from row and set it to results
                # in case black formatting broke it, non-formatted is:  f'\"{results}\"'
                if found:
                    row["homepage_url"] = f'{results}'
                elif not_found:
                    print("Couldn't find it...")
                    row["homepage_url"] = f''

                # Convert the dataframe series to a list
                row_list = pd.Series.tolist(row)
                # print(row_list)

                # join the list to make it csv compatible
                row_list = ",".join(map(str, row_list))

                # print(row_list.strip("nan"))

                cleaned_output.write(f"{row_list} \n")
                print("        [*] Done writing!")
