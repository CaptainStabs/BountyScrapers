import requests
import os
import pandas as pd
import googlesearch as google
import csv
import time
import sys

# sys.setrecursionlimit(10)


# Copy the csv file and rename the copy to `agencies2`
# filename = "agencies.csv"


def main():
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

    # if os.path.isfile("agenciesv1.csv"):
    #     os.rename("agenciesv1.csv", "agencies.csv")

    was_error = False

    # already scraped agencies files
    with open("agencies2.csv", "r", encoding='utf-8') as output_source:
        data_columns2 = output_source.readlines()[0]
        # print(data_columns2)
        output_source.seek(0)
        last_agency = output_source.readlines()[-1]
        last_agency_list = last_agency.split(",")

        print(last_agency)
        # origin data file
        with open("agencies.csv", "r", encoding="utf-8") as input_source:
            content = input_source.readlines()
            # index = [x for x in range(len(content)) if last_agency in content[x].lower()]
            for num, line in enumerate(content, 1):
                line_list = line.split(",")
                # print(line_list[0])
                # print(last_agency_list[0] + " \n")
                if last_agency_list[0] in line_list[0]:
                    try:
                        index = num
                    except NameError:
                        print("No duplicates found")
                        was_error = True
                        pass
                    break
            if not was_error:
                input_source.seek(1)
                with open("agenciesv1.csv", "a", encoding="utf-8") as output:
                    output.write(data_columns2)
                    for i, line in enumerate(content):
                        if i >= index:
                            output.write(line)

        os.remove("agencies.csv")
        os.rename("agenciesv1.csv", "agencies.csv")

    print("  [*] Opening the table and reading...")
    with open("agencies.csv", "r", encoding="utf-8") as filename:
        df = pd.read_csv(filename)
        # access the dataframe columns
        df_columns = list(df.columns)
        # join the returned list to format as csv header
        data_columns = ",".join(map(str, df_columns))
        # print("    [?] Columns: " + str(data_columns))

    print("    [*] Starting loop")
    with open("agencies2.csv", "a", encoding="utf-8") as output:
        # if the file is empty, add the columns
        if os.stat("agencies2.csv").st_size == 0:
            print("      [*] File was empty, adding header")
            print(data_columns)
            output.write(data_columns + "\n")

        print("      [*] Opening agencies.csv")
        with open("agenciesv1.csv", "w") as output2:
            # print("outside loop")
            for index, row in df.iterrows():
                # print("inside loop")
                try:
                    department_name = row["name"].rstrip()
                    no_error = True
                except KeyError:
                    print("        [!] Error on index: " + str(index))
                    no_error = False
                    pass

                found = False
                # prevent NameError from ocurring if the `department_name` was not extracted for some reason.
                if no_error:
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
                                stop=None,
                                pause=2.0,
                            ):
                                # for i in range(len(ignored_domains)):
                                # Iterate through the ignored_domains table to filter out unwanted results
                                # if ignored_domains[i] not in results:
                                #     print("      [*] Found it! URL: " + results)
                                #     found = True
                                #     break
                                # else:
                                #     print("      [*] Haven't found it yet. URL: " + results)
                                #     found = False
                                #     continue

                                # Iterate through the ignored_domains table to filter out unwanted results
                                if any(
                                    ignored_domain in results
                                    for ignored_domain in ignored_domains
                                ):
                                    print(
                                        "      [*] Haven't found it yet. URL: "
                                        + results
                                    )
                                    found = False
                                    continue
                                else:
                                    print("      [*] Found it! URL: " + results)
                                    found = True
                                    break

                                # if found, break the search loop
                                if found:
                                    break
                        except Exception as e:
                            print(e)
                            message_data = "Your code crashed. Error: " + str(e)
                            response = requests.post(
                                "https://notify.run/3GXNtgh04xOuLknE", data=message_data
                            )
                            break

                    # print("      " + results)
                    print("                   Name: " + row["name"] + "\n")
                    print("      [*] Writing results")

                    # ﻿id, name, agency_type, state_iso, city, zip, county_fips, lat, lng, date_insert, data_policy, country, homepage_url
                    type_list = ["university", "school"]
                    for i in range(len(type_list)):
                        if type_list[i] in row["name"].lower():
                            if "nan" in str(row["agency_type"]):
                                row["agency_type"] = str(5)

                    # Access the homepage_url from row and set it to results
                    # in case black formatting broke it, non-formatted is:  f'\"{results}\"'
                    row["homepage_url"] = f'"{results}"'

                    # Convert the dataframe series to a list
                    row_list = pd.Series.tolist(row)
                    # print(row_list)

                    # join the list to make it csv compatible
                    row_list = ",".join(map(str, row_list))

                    # print(row_list.strip("nan"))

                    output.write(f"{row_list} \n")
                    print("        [*] Done writing!")

                    # input()
                    print("   [*] Sleeping")
                    time.sleep(0.05)
    os.remove("agenciesv1.csv")


script_ouput = main()
print(script_ouput)
