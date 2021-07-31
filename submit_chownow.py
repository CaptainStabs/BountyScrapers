import csv
import os
import json
import doltcli as dolt
import requests
import googlesearch as google
from urllib.parse import urlparse
import re


dir = ("./submited/")
full_auto = True  # Default False

db = dolt.Dolt("menus")

url = "https://www.dolthub.com/graphql"
dolt_username = "captainstabs"

payload = json.dumps({
    "operationName": "PullsForRepo",
    "variables": {
        "query": f"{dolt_username}",
        "ownerName": "dolthub",
        "repoName": "menus"
    },
    "query": "query PullsForRepo($ownerName: String!, $repoName: String!, $pageToken: String, $filterByState: PullState, $query: String) {\n  pulls(\n    ownerName: $ownerName\n    repoName: $repoName\n    pageToken: $pageToken\n    filterByState: $filterByState\n    query: $query\n  ) {\n    ...PullListForPullList\n    __typename\n  }\n}\n\nfragment PullListForPullList on PullList {\n  list {\n    ...PullForPullList\n    __typename\n  }\n  nextPageToken\n  __typename\n}\n\nfragment PullForPullList on Pull {\n  _id\n  pullId\n  creatorName\n  title\n  fromBranchName\n  __typename\n}\n"
})
headers = {
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

def get_open_prs(payload, headers, url):
    is_nextpagetoken = True
    from_branch_name = []
    response = requests.request("POST", url, headers=headers, data=payload)
    first = True
    print("while loop start")
    while is_nextpagetoken:
        if not first:
            print("not first")
            response = requests.request("POST", url, headers=headers, data=next_payload)
        parsed = json.loads(response.text)
        pulls_list = parsed["data"]["pulls"]["list"]
        print("looping rows")
        for row in pulls_list:
            from_branch_name.append(row["fromBranchName"])
            # print(row["fromBranchName"])
        if parsed["data"]["pulls"]["nextPageToken"]:  # Check if there is still a nextPageToken
            next_page = parsed["data"]["pulls"]["nextPageToken"]

        else:
            is_nextpagetoken = False
            print("no more token")
        first = False
        next_payload = json.dumps({
            "operationName": "PullsForRepo",
            "variables": {
                "query": f"{dolt_username}",
                "ownerName": "dolthub",
                "repoName": "menus",
                "pageToken": f"{next_page}"
            },
            "query": "query PullsForRepo($ownerName: String!, $repoName: String!, $pageToken: String, $filterByState: PullState, $query: String) {\n  pulls(\n    ownerName: $ownerName\n    repoName: $repoName\n    pageToken: $pageToken\n    filterByState: $filterByState\n    query: $query\n  ) {\n    ...PullListForPullList\n    __typename\n  }\n}\n\nfragment PullListForPullList on PullList {\n  list {\n    ...PullForPullList\n    __typename\n  }\n  nextPageToken\n  __typename\n}\n\nfragment PullForPullList on Pull {\n  _id\n  pullId\n  creatorName\n  title\n  fromBranchName\n  __typename\n}\n"
        })
    with open("open_prs.txt", "w") as output:
        output.write(str(from_branch_name))
    print(from_branch_name)
        # print(json.dumps(parsed, indent=4))

def check_if_exists(headers):
    print("   [*] Starting loop")
    dolt_url = "https://www.dolthub.com/graphql"
    with open("open_prs.txt", "r") as output:
        list_branches = output.readlines()
        # from_branches = from_branches.replace("[", "").replace("]", "")
        # list_branches = from_branches.split(", ")
        # print(from_branches)
    for root, dirs, files in os.walk(dir):
        if "verified_submitted" or "not_submitted" not in root:
            for file in files:
                if ".csv" in file:
                    with open(root + file, 'r') as f:
                        read_csv = csv.DictReader(f)
                        print(file)
                        for index, row in enumerate(read_csv):
                            print("      [*] Getting potential branch names from file")
                            print(index)
                            if index == 1:
                                restaurant_name = row["restaurant_name"]
                                # branch_name1 = "add_" + row["restaurant_name"].replace(" ", "").replace("'", "").replace("&", "").replace("%20", "_").lower()
                                # branch_name2 = "add_" + row["restaurant_name"].replace(" ", "-").replace("'", "").replace("&", "").replace("--", "-").replace("%20", "_").lower()
                                # branch_name3 = "add_" + row["restaurant_name"].replace(" ","-").replace("'", "").replace("&", "").replace("--","-").replace("%20","_").rstrip(".").lower()
                                identifier = row["identifier"]
                                branch_name = "add_" + re.sub("[^0-9a-zA-Z]+", "-", restaurant_name).lower()



                        print("\n      [*] Finding branch's name...")
                        print("         [*] Checking out branch: " + branch_name)
                        try:
                            db.checkout(branch=branch_name, checkout_branch=True)
                        except Exception as error:
                            print("      [!] Branch probably already exists, but I can't tell due to non-existant exceptions")
                            print("        " + str(error))
                            db.checkout(branch=branch_name)
                        # db.checkout(branch=branch_name)
                        # branch_name = branch_name1
                        success = True

                        if success:
                            print("         [*] That worked! branchname: " + branch_name)
                            # response = requests.request("POST", url, headers=headers, data=payload)  # Don't need this anymore, used to check if the branch existed in  a PR
                            print("      [*] Checking if branch has a PR...")
                            if not any(branch_name in list_branch for list_branch in list_branches):
                                print("         [*] PR does not exist, attempting to write...")
                                try:
                                    print("            [*] Trying to write to db...")
                                    dolt.write_file(dolt=db, table="menu_items", file_handle=open(root + file, "r"), import_mode="create", commit=True, commit_message="Add data", do_continue=True)
                                        # dolt.write_file(dolt=db, table="menu_items", file_handle=open(filename, "r"), import_mode="create", do_continue=True)
                                except:
                                        print("               [!] Write failure")
                                        with open("csv_fails.txt", "a") as output:
                                            output.write(file + ", " + branch_name + ", write failure" + "\n")
                                        pass
                                print("            [*] Trying to push to remote")

                                try:
                                    db.push(remote="origin", set_upstream=True, refspec=branch_name)
                                except:
                                    print("               [!] Push failed")
                                    with open("csv_fails.txt", "a") as output:
                                        output.write(file + ", " + branch_name + ", push failure" + "\n")
                                    pass

                                try:
                                    print("            [*] Trying to create PR...")
                                    pr_name = branch_name.replace("_"," ").replace("-", " ") + " " + identifier
                                    payload = json.dumps({
                                        "operationName": "CreatePullRequestWithForks",
                                        "variables": {
                                            "title": f"{pr_name}",
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
                                    response = requests.request("POST", dolt_url, headers=headers, data=payload)
                                    if response.status_code == 200:
                                        print("      [*] Success!")
                                        f.close()
                                        try:
                                            os.rename(root + file, root + "verified_submitted/" + file)
                                        except FileExistsError:
                                            print("Removed")
                                            with open("removed.txt", "a") as f:
                                                f.write(file + "\n")
                                            os.remove(root + file)
                                            pass
                                    else:
                                        print("      [!] Couldn't open a PR")
                                        print("      [!] That's not right. Response code: " + str(response.status_code))
                                        with open("csv_fails.txt", "a") as output:
                                            output.write(file + ", " + branch_name + ", PR failure" + "\n")
                                    print("      [*] Response: " + str(response))
                                except Exception as e:
                                    print(e)
                                    print("      [!] Something went wrong!")
                                    response = requests.request("POST", dolt_url, headers=headers, data=payload)
                                    print(response.status_code)
                                    with open("csv_fails.txt", "a") as output:
                                        output.write(file + ", " + branch_name + ", other failure" + "\n")
                                    pass

                            else:  # If a pr already exists for that file
                                print("      [*] There is already a PR for this file, moving it out" )
                                f.close()  # Close to prevent in use error
                                try:
                                    os.rename(root + file, root + "verified_submitted/" + file)  # move the file
                                except FileExistsError:
                                    print("Removed")
                                    with open("removed.txt", "a") as f:
                                        f.write(file + "\n")
                                    os.remove(root + file)
                                    pass


                    #
                    # print(read_csv)
                    # input()

# get_open_prs(payload, headers, url)
check_if_exists(headers=headers)
