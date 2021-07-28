from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urlparse
import os
import jmespath
import re
import doltcli as dolt
from doltcli import DoltHubContext
# from doltclie import write_file
import csv
import pandas as pd
from tabulate import tabulate

# webpage = input("Enter URL: ")
# https://www.toasttab.com/hearth-pizza-tavern/v3/
webpage = "https://www.toasttab.com/thbtowson/v3"

def toast_tab_scraper(webpage, skip_existing=False, pull_master=True, local_branches=True):
    will_skip = False
    url = "https://ws.toasttab.com/consumer-app-bff/v1/graphql" #  API endpoint

    ### use python's requests module to fetch the webpage as plain html
    html_page = requests.get(webpage).text

    ### use BeautifulSoup4 (bs4) to parse the returned html_page using BeautifulSoup4's html parser (html.parser)
    soup = BeautifulSoup(html_page, "html.parser")

    # for script in soup.find_all("script")[2]:
        # try:
        #     variable_dict = json.loads(script)["window.OO_GLOBALS"]
        #     print(variable_dict)
        # except json.decoder.JSONDecodeError:
        #     pass
        # print(script)
        # variable_dict = json.loads(script)["window.OO_GLOBALS"]
        # script = script.replace("window.OO_GLOBALS =", "")

    parsed = urlparse(webpage) # Parse url
    web_path = parsed.path # Extract info from parse
    web_path_split = web_path.split("/")
    short_url = web_path_split[1]
    print("   [*] Short URL: " + short_url)

    ### Dolt stuff
    print("   [*] Dolt stuff: ")
    print("      [*] Selecting Menus...")
    db = dolt.Dolt("menus")
    print("      [*] Switching to Master...")
    db.checkout(branch="master")
    print("      [*] Pulling remote")
    if pull_master:
        db.pull(remote="dolt-origin")
    branch_name = "add_" + short_url.replace("%20", "_").replace(" ", "_")
    print("      [*] Created and checked out branch " + branch_name)

    dolt_url = "https://www.dolthub.com/graphql"
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
        'Cookie': '__hssc=234007937.7.1627339712817; __hssrc=1; __hstc=234007937.8c2dbc8618061048c739d393b08463d5.1622138431678.1627327973246.1627339712817.97; _ga=GA1.2.1181270506.1617050482; _gat_gtag_UA_130584753_2=1; _gid=GA1.2.2133862710.1627078097; amplitude_id_fef1e872c952688acd962d30aa545b9edolthub.com=eyJkZXZpY2VJZCI6IjAzMjc5ZDFkLWY4MzQtNDhjNS04MTMyLWQ1NTI2MzUwMDZiNlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTYyNzMyNDU5ODc1NSwibGFzdEV2ZW50VGltZSI6MTYyNzMyNDY0NDY3MiwiZXZlbnRJZCI6NCwiaWRlbnRpZnlJZCI6MSwic2VxdWVuY2VOdW1iZXIiOjV9; hubspotutk=8c2dbc8618061048c739d393b08463d5; G_ENABLED_IDPS=google; __stripe_mid=4b66cabc-51a2-47a3-8c23-b35a4fcb222f48f55d; __stripe_sid=03c3c926-44c6-4f20-b32f-5b450897d93de0727d; dolthubToken=ldst.v1.6h4rmj56ot1sfhcf3htm9n8im3hb2gfckshkh1aiug0kn45t8j60'
    }

    if not local_branches:
        dolt_payload =  json.dumps({"operationName":"BranchSelectorForRepo","variables":{"ownerName":"captainstabs","repoName":"menus"},"query":"query BranchSelectorForRepo($ownerName: String!, $repoName: String!, $pageToken: String) {\n  branchNames(ownerName: $ownerName, repoName: $repoName, pageToken: $pageToken) {\n    list {\n      ...BranchForBranchSelector\n      __typename\n    }\n    nextPageToken\n    __typename\n  }\n}\n\nfragment BranchForBranchSelector on Branch {\n  branchName\n  repoName\n  ownerName\n  __typename\n}\n"})
        response = requests.request("POST", dolt_url, headers=dolt_headers, data=dolt_payload)
        if branch_name in response.text:
            will_skip = True
            print("      [!] Found remote branch matching proposed branch, skipping!")
    if not will_skip:
        try:
            db.checkout(branch=branch_name, checkout_branch=True)
        except Exception as error:
            print("      [!] Branch probably already exists, but I can't tell due to non-existant exceptions")
            print("        " + str(error))
            db.checkout(branch=branch_name)
            if skip_existing:
                print("      [!] Skipping!")
                will_skip = True
            pass


    if not will_skip and skip_existing:
            print("   [*] Finding third script")
            scripts = soup.find_all("script")[2]
            # print("Scripts: " + str(scripts))

            ###  Regex? never heard of it
            script = str(scripts).replace("window.OO_GLOBALS =", "").replace("<script>", "").replace("</script>", "").replace(";", "")
            # print("Script: " + script)
            data = json.loads(script)
            restaurant_guid = data["restaurantGuid"]
            print("   [*] Restaurant's guid: " + restaurant_guid)


            payload = json.dumps([
                {
                    "operationName": "RESTAURANT_INFO",
                    "variables": {
                        "restaurantGuid": f"{restaurant_guid}"
                    },
                    "query": "query RESTAURANT_INFO($restaurantGuid: ID!) {\n  restaurantV2(guid: $restaurantGuid) {\n    ... on Restaurant {\n      guid\n      whiteLabelName\n      location {\n        city\n        state\n }\n  }\n    ... on GeneralError {\n      code\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"
                }
            ])
            headers = {
                'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                'apollographql-client-name': 'takeout-web',
                'DNT': '1',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                'toast-customer-access': '',
                'content-type': 'application/json',
                'accept': '*/*',
                'apollographql-client-version': '542',
                'Toast-Restaurant-External-ID': f'{restaurant_guid}',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            parsed = json.loads(response.text)

            restaurant_info = parsed[0]["data"]["restaurantV2"]
            city = restaurant_info["location"]["city"].upper()
            state = restaurant_info["location"]["state"].upper()

            restaurant_name = restaurant_info["whiteLabelName"]
            identifier = f"{city}, {state}"

            print("\n   [*] Restaurant Info: ")
            print("      [*] Restaurant Name: " + restaurant_name)
            print("      [*] Identifier: " + identifier)

            menu_payload = json.dumps({
                "operationName": "MENUS",
                "variables": {
                    "input": {
                        "shortUrl": f"{short_url}", # no idea why this doesn't matter
                        "restaurantGuid": f"{restaurant_guid}",
                        "menuApi": "DO"
                    }
                },
                "query": "query MENUS($input: MenusInput!) {\n  menusV3(input: $input) {\n    ... on MenusResponse {\n      menus {\n        id\n        name\n        groups {\n          guid\n          name\n          items {\n            description\n            guid\n            name\n            outOfStock\n            price\n            calories\n            itemGroupGuid\n            unitOfMeasure\n            usesFractionalQuantity\n            masterId\n            __typename\n          }}}}... on GeneralError {\n      code\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"
            })
            menu_response = requests.request("POST", url, headers=headers, data=menu_payload)


            # print(menu_response.text)
            # menu_parsed = json.loads(menu_response.text)
            # with open("testokiboru.json", "w") as output:
            #     output.write(json.dumps(menu_parsed, indent=4))

            columns = ["name", "restaurant_name", "identifier", "calories", "price_usd"]
            # menu_parsed = json.loads(menu_response.text)
            # menus = menu_parsed["data"]["menusV3"]["menus"] # menusV3
            # menu = json.dumps(menu_parsed, indent=4)
            # print(menu)
            expression = jmespath.compile('data.menusV3.menus[][name, groups[].[name, items[*][name,price,calories]]]')
            #expression = jmespath.compile('length(data)')
            data = json.loads(menu_response.text)
            searched = expression.search(data)
            #print(data)
            # print(json.dumps(searched, indent=4))

            print("   [*] Beginning loop... Number of menus: " + str(len(searched)))
            print("      [*] Menus: ")

            filename = restaurant_name.replace(" ", "_").replace("/", "_") + ".csv"

            ### searched[0] # this is second list, containing menus
            nutrition_facts= {}
            nutrition_list = []
            with open("./submitted/" + filename, "a") as output:
                writer = csv.DictWriter(output, fieldnames=columns)
                if not os.path.isfile(filename) or os.stat(filename).st_size == 0:
                    writer.writeheader()
                for i in range(len(searched)):  # Loop over array (top-level)
                    menu_name = searched[i][0]  # This works
                    print("         [*] " + str(menu_name))
                    print("RERESRESRSE " + str(i) )
                    menu = searched[i][1]
                    # print(json.dumps(menu, indent=4))
                    for j in range(len(menu)):
                        sub_menu_category = menu[j][0]
                        print("            [*] "+ sub_menu_category)
                        category_items = menu[j][1]
                        for item_list in category_items:
                            # print(sub_menu[item_list])
                            # items_list = category_items[item_list]
                            # print(json.dumps(items_list, indent=4))
                            try:
                                nutrition_facts["name"] =  item_list[0].replace('\\"', " inch ").replace('"', " inch ").upper()
                                nutrition_facts["restaurant_name"] = restaurant_name.upper()
                                nutrition_facts["identifier"] = identifier.upper()
                                nutrition_facts["calories"] = str(item_list[2]).replace("None", "")
                                nutrition_facts["price_usd"] = "{:.2f}".format(item_list[1])

                                writer.writerow(nutrition_facts)
                                nutrition_list.append(nutrition_facts)


                            except TypeError as exception:
                                print(exception)
                                print("   [!!!!] UH OH")
                                pass



                        #

            # print(tabulate(df, headers='keys', tablefmt='psql'))
            # choice = input("   [!!!] Automatically (attempt) to load data? Y/N: ")
            # if choice.lower() == "y":
            try:
                dolt.write_file(dolt=db, table="menu_items", file_handle=open(filename, "r"), import_mode="create", commit=True, commit_message="Add data", do_continue=True)
                    # dolt.write_file(dolt=db, table="menu_items", file_handle=open(filename, "r"), import_mode="create", do_continue=True)
                db.push(remote="origin", set_upstream=True, refspec=branch_name)

                ### Open a PR
                branch_name2 = branch_name.replace("_"," ").replace("-", " ") + " " + identifier
                # dolt_url = "https://www.dolthub.com/graphql"
                payload = json.dumps({
                    "operationName": "CreatePullRequestWithForks",
                    "variables": {
                        "title": f"{branch_name2}",
                        "description": "",
                        "fromBranchName": f"{branch_name}",
                        "toBranchName": "master",
                        "fromBranchOwnerName": "captainstabs",
                        "fromBranchRepoName": "menus",
                        "toBranchOwnerName": "dolthub",
                        "toBranchRepoName": "menus",
                        "parentOwnerName": "dolthub",
                        "parentRepoName": "menus"
                    },
                    "query": "mutation CreatePullRequestWithForks($title: String!, $description: String!, $fromBranchName: String!, $toBranchName: String!, $fromBranchRepoName: String!, $fromBranchOwnerName: String!, $toBranchRepoName: String!, $toBranchOwnerName: String!, $parentRepoName: String!, $parentOwnerName: String!) {\n  createPullWithForks(\n    title: $title\n    description: $description\n    fromBranchName: $fromBranchName\n    toBranchName: $toBranchName\n    fromBranchOwnerName: $fromBranchOwnerName\n    fromBranchRepoName: $fromBranchRepoName\n    toBranchOwnerName: $toBranchOwnerName\n    toBranchRepoName: $toBranchRepoName\n    parentRepoName: $parentRepoName\n    parentOwnerName: $parentOwnerName\n  ) {\n    _id\n    pullId\n    __typename\n  }\n}\n"
                })

                print("   [!] Opening PR")
                response = requests.request("POST", dolt_url, headers=dolt_headers, data=payload)
                print("      [*] Response: " + response)
                # menu_parsed = json.loads(searched)
                # print(json.dumps(menu_parsed, indent=4))
            except:
                with open("fails.txt", "a") as f:
                    f.write(branch_name)
                print("    [!] No Bueno")
                pass
toast_tab_scraper(webpage, skip_existing=True, pull_master=False,  local_branches=False)
