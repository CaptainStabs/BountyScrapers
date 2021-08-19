import requests
import os
import pandas as pd
import googlesearch as google
import csv
import time
import sys
from utils.interrupt_handler import GracefulInterruptHandler
import traceback
from _secrets import notify_url

full_auto = True

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
    "countyoffice"
]



def write_to_file(results, row, file_in):
    row["website"] = f'"{results}"'
    row_list = pd.Series.tolist(row)
    row_list = ",".join(map(str, row_list))

    file_in.write(f"{row_list}\n")
    print("   [*] Done writing! Sleeping...")
    time.sleep(0.5)

print("   [*] Opening Source File...")

with GracefulInterruptHandler() as h:
    with open("websites_smaller_HIFLD_Schools.csv", "r", encoding="utf-8") as input_source:
        print("      [*] Reading csv")
        df = pd.read_csv(input_source)
        df_columns = list(df.columns)
        data_columns = ",".join(map(str, df_columns))

        print("         [*] Opening output file...")
        with open("websites_added.csv", "a", encoding="utf-8") as file_out:
            print("            [*] Starting loop")
            for index, row in df.iterrows():
                if h.interrupted:
                    print("      [!] Interrupted, exiting")
                    break

                # check_null = row["website"]
                if pd.isnull(row["website"]):
                    try:
                        school_name = row["name"]
                        no_error = True

                    except KeyError:
                        print(f"            [!] Error on index: {index}")
                        no_error = False
                        pass
                else:
                    no_error = False
                    print("            [*] Website already exists, skipping.")
                    print("               [?] Website: " + str(row["website"]))
                    print(row["website"])

                found = False
                num_tries = 0

                if no_error:
                    while not found:
                        print("         [*] Starting search loop...")
                        query = school_name + " " + row["state"]
                        print("            [?] " + query)
                        try:
                            for results in google.search(
                                query,
                                tld="com",
                                lang="en",
                                num=10,
                                start=0,
                                stop=10,
                                pause=2.0,
                            ):

                                # print(type(results))
                                if any(ignored_domain in results for ignored_domain in ignored_domains):
                                        print(f"            [*] Haven't found it yet. URL: {results}")
                                        found = False
                                        num_tries += 1
                                        continue

                                else:
                                    print(f"         [*] Found it! URL: {results}\n                    Name: {school_name}\n                    City: {row['city']}\n                    State: {row['state']}\n")
                                    found = True
                                    break

                                if num_tries > 10:
                                    print("         [*] Couldn't find it.")
                                    break


                        except Exception as e:
                            import urllib3
                            traceback.print_exc()
                            print("\n\n")
                            print(e)

                            message_data = f"Your code crashed. Error: \n{str(e)}"
                            http = urllib3.PoolManager()
                            response = http.request('POST', notify_url, body=message_data)
                            print(response.read())
                            found = False
                            sys.exit()
                            break

                    # Outside while loop
                    if found:
                        if not full_auto:
                            user_choice = input(f"   [!] Does this url look correct?\n     Name: {school_name}\n     State: {row['state']}\n     City: {row['city']}\n     URL: {results}\n     y/n: ")

                            if user_choice.lower() == "y":
                                write_to_file(results, row, file_out)

                            elif user_choice.lower() == "n":
                                print("   [*] Skipping")
                                continue

                        else:
                            write_to_file(results, row, file_out)
