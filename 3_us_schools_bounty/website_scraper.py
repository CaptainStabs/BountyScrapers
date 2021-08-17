import requests
import os
import pandas as pd
import googlesearch as google
import csv
import time
import sys
from utils.interrupt_handler import GracefulInterruptHandler
from _secrets import notify_url

full_auto = False

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
    "elementaryschools"
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
    with open("HIFLD_Schools.csv", "r", encoding="utf-8") as input_source:
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

                if not row["website"]:
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

                found = False
                num_tries = 0

                if no_error:
                    while not found:
                        print("         [*] Starting search loop...")
                        try:
                            for results in google.search(
                                school_name,
                                tld="com",
                                lang="en",
                                num=10,
                                start=0,
                                stop=None,
                                pause=2.0,
                            ):
                                if any(ignored_domains in results for ignored_domain in ignored_domains):
                                        print(f"            [*] Haven't found it yet. URL: {url}")
                                        found = False
                                        if num_tries == 10:
                                            print("         [*] Couldn't find it.")
                                            break
                                        else:
                                            num_tries += 1
                                            continue
                                else:
                                    print(f"         [*] Found it! URL: {results}")
                                    found = True
                                    break


                        except Exception as e:
                            print(e)
                            message_data = "Your code crashed. Error: \n" + str(e)
                            response = requests.post(
                                notify_url, data=message_data
                            )
                            break

                    # Outside while loop
                    if not full_auto:
                        user_choice = input(f"   [!] Does this url look correct? y/n URL: {results}")

                        if user_choice.lower() == "y":
                            write_to_file(results, row, file_out)

                        elif user_choice.lower() == "n":
                            print("   [*] Skipping")
                            continue

                    else:
                        write_to_file(results, row, file_out)
