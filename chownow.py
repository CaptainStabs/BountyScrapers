import requests
import csv
import json
import doltcli as dolt
import os
import time
import re
from _cookie import dolt_cookie


# db = dolt.Dolt("menus")
# db.checkout(branch="master")

"""ChowNow request headers"""
query_headers = {
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'Accept': 'application/json version=3.0;',
    'DNT': '1',
    'X-CN-App-Info': 'Marketplace-Web/2.0.0',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Content-Type': 'application/json; charset=UTF-8',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'#,
    # 'Cookie': '__cf_bm=5f0d216f7036bab638b4bf50c1785131cbaa32f9-1627664529-1800-ASpeyAz6m6jOA6fJGzBVczvlvJYj5Op1MX2tkI/em5kt0BOVCIoTwUIG+RtzBLXzCRWhuVhY6FkC9FGR2HllOUS2NKgZXyJowlB/7rCFoviv; __cfruid=09aaef67db4c3eae06bde07c79cecfeef0ff5dc2-1627664611'
}

dolt_headers = {
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'accept': '*/*',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'content-type': 'application/json',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Cookie': f'{dolt_cookie}'
}

columns = ["name", "restaurant_name", "identifier", "calories", "price_usd"]

"""Open file
Due to the way that chownow's API requests cities (by coordinates),
we need to be able to loop through cities
"""
print("   [*] Opening list of cities...")
with open("us_cities.csv", "r") as location_file:
    location_list = csv.reader(location_file)
    next(location_list)  # Skip header

    first = True

    for row in location_list:
        last = False
        city = row[3]
        state_code = row[1]
        lat = row[5]
        lon = row[6]
        print(f"      [*] Current City, State: {city}, {state_code}")
        print(lat, lon)

        if first:  # This needs to be differentiated as the first as we don't have a next page yet
            first_query_url = f"https://api.chownow.com/api/restaurant/?u_lat={lat}&u_lon={lon}"
            first_query_response = requests.request("GET", first_query_url, headers=query_headers)

            try:
                parsed_response = json.loads(first_query_response.text)

            except json.decoder.JSONDecodeError as e:
                print("      [!] Error: " + str(e))
                print(first_query_response.text)

        else:  # (Not first)
            next_page_url = "https://api.chownow.com/" + parsed_response["next"]
            next_page_response = requests.request("GET", next_page_url, headers=query_headers)
            parsed_response = json.loads(next_page_response.text)


        """Sleep times are due to the script being too fast
        when it doesn't handle the db checkout/write/push stuff. (Got rate limitted by cloudflare)
        """
        if parsed_response["total"] == 0:
            print("      [*] No results, skipping")
            time.sleep(0.9)
            # print(first_query_response.text)
            continue  # Get the next row from location_list

        else:
            restaurant_list = parsed_response["restaurants"]

            if not parsed_response["next"]:
                print("      [*] End of City results...")
                last = True  # Forces the loop to progress at the end

            for restaurant_dict in restaurant_list:
                nutrition_facts = {}  # Prepare output dict

                ### Access the information from the response
                # restaurant_dict = restaurant_list[lists]  # Restaurants is a list of dicts
                restaurant_city = restaurant_dict["address"]["city"]  # This should match the city belonging to the coords, but just to be sure
                restaurant_state = restaurant_dict["address"]["state"]
                company_id = restaurant_dict["restaurant_company_id"]
                restaurant_name = restaurant_dict["short_name"]
                location_id = restaurant_dict["id"]

                identifier = restaurant_city + ", " + restaurant_state  # For PK in db
                print(f"      [?] City, state: {identifier}, Company_id: {company_id}, location_id: {location_id}, restaurant_name: {restaurant_name}")

                menu_query = f"https://api.chownow.com/api/restaurant/{company_id}/menu/"
                menu_response = requests.request("GET", menu_query, headers=query_headers)
                time.sleep(0.9)

                try:
                    menu_parsed = json.loads(menu_response.text)

                except json.decoder.JSONDecodeError as e:
                    print("      [!] Error: " + str(e))
                    print(first_query_response.text)

                try:  # Should probably be protected by a variable defined by a succusful parsed but whatever
                    menu_categories = menu_parsed["menu_categories"]

                except KeyError:  # For whatever reason, the api uses company_id sometimes, and just id for others
                    menu_query = f"https://api.chownow.com/api/restaurant/{location_id}/menu/"
                    menu_response = requests.request("GET", menu_query, headers=query_headers)
                    menu_parsed = json.loads(menu_response.text)
                    time.sleep(0.8)
                    pass

                    try:  # Try accessing menu_categories again
                        menu_categories = menu_parsed["menu_categories"]

                    except KeyError:  # Other times it requires a time stamp to be appended. format is YYMMDDHHMM
                        menu_query = f"https://api.chownow.com/api/restaurant/{location_id}/menu/" + time.strftime('%Y%m%d') + str(1700)
                        menu_response = requests.request("GET", menu_query, headers=query_headers)
                        menu_parsed = json.loads(menu_response.text)
                        pass

                        try:  # Sometimes the timestamp is different than usual, so I just skip those
                            menu_categories = menu_parsed["menu_categories"]
                        except KeyError:
                            print("      [!] I give up, skipping")
                            continue
                            pass



                    # print(json.dumps(menu_parsed, indent=4))
                    # with open("menu_parsed.txt", "a") as f:
                    #     f.write(json.dumps(menu_parsed, indent=4))
                    #     input()
                    # with open("first_query.txt", "a") as f:
                    #     f.write(json.dumps(parsed_response, indent=4))
                    #     input()

                # filename = "add_" + restaurant_name.replace(" ", "_").replace("'","").replace("\n","").replace("&","and").replace("--","-").replace("_|_", "").replace(".", "-").replace("?","").lower() + ".csv"
                branch_name = "add_" + re.sub("[^0-9a-zA-Z]+", "-", restaurant_name).lower()  # Strip out nono-alphanumeric characters
                filename = branch_name + ".csv"
                # print(json.dumps(menu_parsed, indent=4))


                ### Prepare Dolt
                # db.checkout(branch="master")
                # try:
                #     db.checkout(branch=branch_name, checkout_branch=True)
                # except Exception as error:
                #     print("      [!] Branch probably already exists, but I can't tell due to non-existant exceptions")
                #     print("        " + str(error))
                #     db.checkout(branch=branch_name)
                # print("      [*] Opening file")

                # Write results to file
                file_path = "./submited/" + filename.replace("/", "-").replace("_|_", "")
                with open(file_path, "a") as output:
                    writer = csv.DictWriter(output, fieldnames=columns)

                    # Check if the file exists, or if the file is empty
                    # If it's empty, we need to add the header
                    if not os.path.isfile(file_path) or os.stat(file_path).st_size == 0:
                        writer.writeheader()
                        file_is_new = True

                    else:
                        file_is_new = False

                    if file_is_new:
                        print("      [*] File is new")
                        for category_dict in menu_categories:
                            category_items = category_dict["items"]
                            # print(category_items)

                            for items in category_items:
                                failed = False
                                # print(json.dumps(items, indent=4))
                                try:
                                    try:
                                        print("      [*] There is a size! Size: " + str(items["size"]).upper())
                                        nutrition_facts["name"] = items["name"].replace('\\"', " inch ").replace('"', " inch ").upper() + " - " + str(items["size"]).upper()

                                    except KeyError as error:  # Means that the API is dumb and inconsisitent
                                        print("      [!] ERROR with size: " + str(error))
                                        nutrition_facts["name"] = items["name"].replace('\\"', " inch ").replace('"', " inch ").upper()
                                        pass

                                    nutrition_facts["restaurant_name"] = restaurant_name.upper()
                                    nutrition_facts["identifier"] = "CHOWNOW, " + identifier.upper()

                                    try:
                                        nutrition_facts["price_usd"] =  "{:.2f}".format(items["price"])
                                    except KeyError as e:
                                        failed = True  # I don't want to write a bad row
                                        # print("      [!] " + str(e))
                                        print("      [!] Couldn't find a price")
                                        pass

                                    if not failed:  # Tries to prevent writing bad rows
                                        writer.writerow(nutrition_facts)

                                except KeyError as e1:  # Related to first try in this chunk, doesn't happen afaik
                                        failed = True
                                        print("      [!] " + str(e1))
                                        print("      [!] One of the other three columns failed")
                                        pass

                                ### Dolt stuff
                                # try:
                                #     print("      [*] Trying to write to db")
                                #     dolt.write_file(dolt=db, table="menu_items", file_handle=open("./submited/" + filename, "r"), import_mode="create", commit=True, commit_message="Add data", do_continue=True)
                                #         # dolt.write_file(dolt=db, table="menu_items", file_handle=open(filename, "r"), import_mode="create", do_continue=True)
                                #     print("      [*] Trying to push")
                                #     db.push(remote="origin", set_upstream=True, refspec=branch_name)
                                #     failure = False
                                # except Exception as e:
                                #     print("     [!] Couldn't write/push. Error: " + str(e))
                                #     failure = True
                                # if not failure:
                                #     try:
                                #         ### Open a PR
                                #         branch_name2 = branch_name.replace("_"," ").replace("-", " ") + " " + identifier
                                #         dolt_url = "https://www.dolthub.com/graphql"
                                #         payload = json.dumps({
                                #             "operationName": "CreatePullRequestWithForks",
                                #             "variables": {
                                #                 "title": f"{branch_name2}",
                                #                 "description": "",
                                #                 "fromBranchName": f"{branch_name}",
                                #                 "toBranchName": "master",
                                #                 "fromBranchOwnerName": "captainstabs",
                                #                 "fromBranchRepoName": "menus",
                                #                 "toBranchOwnerName": "dolthub",
                                #                 "toBranchRepoName": "menus",
                                #                 "parentOwnerName": "dolthub",
                                #                 "parentRepoName": "menus"
                                #             },
                                #             "query": "mutation CreatePullRequestWithForks($title: String!, $description: String!, $fromBranchName: String!, $toBranchName: String!, $fromBranchRepoName: String!, $fromBranchOwnerName: String!, $toBranchRepoName: String!, $toBranchOwnerName: String!, $parentRepoName: String!, $parentOwnerName: String!) {\n  createPullWithForks(\n    title: $title\n    description: $description\n    fromBranchName: $fromBranchName\n    toBranchName: $toBranchName\n    fromBranchOwnerName: $fromBranchOwnerName\n    fromBranchRepoName: $fromBranchRepoName\n    toBranchOwnerName: $toBranchOwnerName\n    toBranchRepoName: $toBranchRepoName\n    parentRepoName: $parentRepoName\n    parentOwnerName: $parentOwnerName\n  ) {\n    _id\n    pullId\n    __typename\n  }\n}\n"
                                #         })
                                #
                                #         print("   [!] Opening PR")
                                #         response = requests.request("POST", dolt_url, headers=dolt_headers, data=payload)
                                #         print(response.text)
                                #         # input()
                                #         print("      [*] Response: " + response)
                                #         # menu_parsed = json.loads(searched)
                                #         # print(json.dumps(menu_parsed, indent=4))
                                #     except:
                                #         with open("fails.txt", "a") as f:
                                #             f.write(branch_name + ", " + restaurant_name + "\n")
                                #         print("    [!] No Bueno")
                                #         continue
                                #         pass

            if last:
                """Reset for next location"""
                first = True
                continue  # End iterating over restaurant_dict
                time.sleep(2)

                # print(json.dumps(parsed_response["restaurants"], indent=4))
                    # break
