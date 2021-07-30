import csv
import os
import json
import doltcli as dolt
import requests
import googlesearch as google
from urllib.parse import urlparse


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
    'Sec-Fetch-Dest': 'empty'
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

def check_if_exists():
    print("   [*] Starting loop")
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
                        for index, row in enumerate(read_csv):
                            if index == 2:
                                restaurant_name = row["restaurant_name"]
                                branch_name1 = "add_" + row["restaurant_name"].replace(" ", "").replace("'", "").replace("&", "").replace("%20", "_").lower()
                                branch_name2 = "add_" + row["restaurant_name"].replace(" ", "-").replace("'", "").replace("&", "").replace("--", "-").replace("%20", "_").lower()
                                branch_name3 = "add_" + row["restaurant_name"].replace(" ","-").replace("'", "").replace("&", "").replace("--","-").replace("%20","_").rstrip(".").lower()
                                break

                        print("\n      [*] Finding branch's name...")
                        try:
                            print("         [*] Checking out branch: " + branch_name1)
                            db.checkout(branch=branch_name1)
                            branch_name = branch_name1
                            success = True
                        except:
                            print("         [!] That didn't work, trying with: " + branch_name2)
                            # success = False
                            pass
                            try:
                                db.checkout(branch=branch_name2)
                                branch_name = branch_name2
                                success = True
                            except:
                                # success = False
                                print("         [!] That didn't work, trying with: " + branch_name3)
                                pass
                                try:
                                    db.checkout(branch=branch_name3)
                                    branch_name = branch_name3
                                    success = True
                                except:
                                    print(f"         [!] That also didn't work. Rest Name: {restaurant_name}")
                                    print("          [*] Last automated try... Searching google...")
                                    search_query = "toasttab " + restaurant_name
                                    # success = False
                                    for results in google.search(search_query, tld="com", lang="en", num=5, start=0, stop=5, pause=0.3):
                                        # print(results)
                                        if "toasttab" in results:
                                            print("          [*] Might've found one! ")
                                            parsed_url = urlparse(results)
                                            url_path = parsed_url.path
                                            potential_branch = url_path.split("/")[1]
                                            print("            [*] Potenial branch: " + str(potential_branch))
                                            try:
                                                db.checkout(branch="add_" + potential_branch)
                                                branch_name = "add_" + potential_branch
                                                success = True
                                                break
                                            except:
                                                print(f"               [!] Wasn't {potential_branch}, trying again...")
                                                pass

                                    # if not success:
                                    #     if not full_auto:
                                    #         branch_name4 = input("         [?] Type the branchname: ")
                                    #         db.checkout(branch=branch_name4)
                                    #         branch_name = branch_name4
                                    #         success=True
                                    #     else:
                                    # success=False
                                                with open("csv_fails.txt", "a") as output:
                                                    output.write(file + ", " + branch_name + ", branch failure" + "\n")
                                                pass

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
                                    dolt_url = "https://www.dolthub.com/graphql"
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
                                    response = requests.request("POST", dolt_url, headers=dolt_headers, data=payload)
                                    if response.status_code == 200:
                                        print("      [*] Success!")
                                        f.close()
                                        os.rename(root + file, root + "verified_submitted/" + file)

                                    else:
                                        print("      [!] Couldn't open a PR")
                                        print("      [!] That's not right. Response code: " + str(response.status_code))
                                        with open("csv_fails.txt", "a") as output:
                                            output.write(file + ", " + branch_name + ", PR failure" + "\n")
                                    print("      [*] Response: " + response)
                                except:
                                    print("      [!] Something went wrong!")
                                    print(response.text)
                                    with open("csv_fails.txt", "a") as output:
                                        output.write(file + ", " + branch_name + ", other failure" + "\n")
                                    pass

                            else:  # If a pr already exists for that file
                                print("      [*] There is already a PR for this file, moving it out" )
                                f.close()
                                os.rename(root + file, root + "verified_submitted/" + file)


                    #
                    # print(read_csv)
                    # input()

# get_open_prs(payload, headers, url)
check_if_exists()
