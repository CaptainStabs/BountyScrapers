import csv
import os
import json
import doltcli as dolt
import requests
import googlesearch as google
from urllib.parse import urlparse
from _cookie import dolt_cookie
import re
from utils.interrupt_handler import GracefulInterruptHandler

dir = ("./submited/")  # Where the save directory should be
full_auto = True  # Default False


db = dolt.Dolt("menus")  # Select the dolt database

url = "https://www.dolthub.com/graphql"
dolt_username = "captainstabs"

###  Payload for getting open PRs from dolt
payload = json.dumps({
    "operationName": "PullsForRepo",
    "variables": {
        "query": f"{dolt_username}",
        "ownerName": "dolthub",
        "repoName": "menus"
    },
    "query": "query PullsForRepo($ownerName: String!, $repoName: String!, $pageToken: String, $filterByState: PullState, $query: String) {\n  pulls(\n    ownerName: $ownerName\n    repoName: $repoName\n    pageToken: $pageToken\n    filterByState: $filterByState\n    query: $query\n  ) {\n    ...PullListForPullList\n    __typename\n  }\n}\n\nfragment PullListForPullList on PullList {\n  list {\n    ...PullForPullList\n    __typename\n  }\n  nextPageToken\n  __typename\n}\n\nfragment PullForPullList on Pull {\n  _id\n  pullId\n  creatorName\n  title\n  fromBranchName\n  __typename\n}\n"
})

###  Headers for Dolt
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
    'Cookie': f'{dolt_cookie}'
}

'''
Get the open pull requests from dolt, and save them in `open_prs.txt` to be read
'''
def get_open_prs(payload, headers, url):
    is_nextpagetoken = True
    from_branch_name = []
    response = requests.request("POST", url, headers=headers, data=payload)  # Get inital page
    first = True

    print("while loop start")
    while is_nextpagetoken:  # There is no nextPageToken on the last "page"
        if not first:        # To deliver the nextPageToken payload instead of default starter payload
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
            is_nextpagetoken = False  #  Breaks while loop
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

    ###  Once there is no nextPageToken, this will write
    with open("open_prs.txt", "w") as output:
        output.write(str(from_branch_name))
    print(from_branch_name)
        # print(json.dumps(parsed, indent=4))

"""Check if the branch exists (locally)."""
def check_if_exists(headers):
    print("   [*] Starting loop")
    dolt_url = "https://www.dolthub.com/graphql"

    with open("open_prs.txt", "r") as output:
        list_branches = output.readlines()
        # from_branches = from_branches.replace("[", "").replace("]", "")
        # list_branches = from_branches.split(", ")
        # print(from_branches)
    with GracefulInterruptHandler() as h:
        for root, dirs, files in os.walk(dir):
            if "verified_submitted" or "not_submitted" not in root:  # These are the "safe" folders
                for file in files:
                    if h.interrupted:
                        print("   [!] Interrupted, exiting.")
                        break

                    db.checkout(branch="master")
                    if ".csv" in file:                               # We only want the CSVs
                        with open(root + file, 'r') as f:
                            read_csv = csv.DictReader(f)
                            print("\n" + file)

                            print("      [*] Getting potential branch names from file")
                            for index, row in enumerate(read_csv):
                                # print(index)
                                if index == 1:  # Skip the csv header
                                    restaurant_name = row["restaurant_name"]
                                    # branch_name1 = "add_" + row["restaurant_name"].replace(" ", "").replace("'", "").replace("&", "").replace("%20", "_").lower()
                                    # branch_name2 = "add_" + row["restaurant_name"].replace(" ", "-").replace("'", "").replace("&", "").replace("--", "-").replace("%20", "_").lower()
                                    # branch_name3 = "add_" + row["restaurant_name"].replace(" ","-").replace("'", "").replace("&", "").replace("--","-").replace("%20","_").rstrip(".").lower()
                                    identifier = row["identifier"]
                                    branch_name = "add_" + re.sub("[^0-9a-zA-Z]+", "-", restaurant_name) + "-2".lower()
                                    break

                            print("\n      [*] Finding branch's name...")
                            print("         [*] Checking out branch: " + branch_name)
                            try:
                                db.checkout(branch=branch_name, checkout_branch=True)
                                # success = True

                            except Exception as error:
                                print("      [!] Branch probably already exists, but I can't tell due to non-existant exceptions")
                                print("        " + str(error))
                                db.checkout(branch=branch_name)
                                # success = False
                            # db.checkout(branch=branch_name)
                            # branch_name = branch_name1
                            success = True

                            if success:  # No point in wasting time on broken files
                                print("         [*] That worked! branchname: " + branch_name)
                                # response = requests.request("POST", url, headers=headers, data=payload)  # Don't need this anymore, used to check if the branch existed in  a PR

                                print("      [*] Checking if branch has a PR...")
                                if not any(branch_name in list_branch for list_branch in list_branches):
                                    print("         [*] PR does not exist, attempting to write...")
                                    try:
                                        print("            [*] Trying to write to db...")
                                        dolt.write_file(dolt=db, table="menu_items", file_handle=open(root + file, "r"), import_mode="create", commit=True, commit_message="Add data", do_continue=True, do_gc=False)
                                            # dolt.write_file(dolt=db, table="menu_items", file_handle=open(filename, "r"), import_mode="create", do_continue=True)
                                    except Exception as error:
                                            print(error)
                                            print("               [!] Write failure")
                                            with open("csv_fails.txt", "a") as output:  # Log the failure
                                                output.write(file + ", " + branch_name + ", write failure" + "\n")
                                            pass


                                    """Being the early stages that dolt is in, these are primarily workarounds.
                                    Due to the (mostly) autonomous nature of this script, I don't want any errors interefering with it's progress.
                                    """
                                    print("            [*] Trying to push to remote")
                                    try:
                                        db.push(remote="origin", set_upstream=True, refspec=branch_name)

                                    except:
                                        print("               [!] Push failed")
                                        with open("csv_fails.txt", "a") as output:  # Log the failure for manual review
                                            output.write(file + ", " + branch_name + ", push failure" + "\n")
                                        pass

                                    try:
                                        print("            [*] Trying to create PR...")
                                        pr_name = branch_name.replace("_"," ").replace("-", " ") + " " + identifier
                                        payload = json.dumps({
                                            "operationName": "CreatePullRequestWithForks",
                                            "variables": {
                                                "title": f"{pr_name.lower()}",
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

                                        if response.status_code == 200 and "error" not in response.text:  # Check if dolt returns OK
                                            print("      [*] Success!")
                                            print("         [?] " + str(response.text))
                                            f.close()  # Close to prevent InUse error

                                            try:
                                                os.rename(root + file, root + "verified_submitted/" + file)  # Move the file to the submitted folder

                                            except FileExistsError:
                                                print("Removed")
                                                with open("removed.txt", "a") as f:
                                                    f.write(file + "\n")
                                                os.remove(root + file)
                                                pass

                                        else:
                                            print("      [!] Couldn't open a PR")
                                            print("      [!] That's not right. Response code: " + str(response.status_code))
                                            print(response.text)
                                            with open("csv_fails.txt", "a") as output:
                                                output.write(file + ", " + branch_name + ", PR failure" + "\n")

                                        print("      [*] Response: " + str(response))

                                    except Exception as e:
                                        print("      [!] Something went wrong!")
                                        print("      [!] Error: " + str(e))

                                        response = requests.request("POST", dolt_url, headers=headers, data=payload)
                                        print(response.status_code)

                                        with open("csv_fails.txt", "a") as output:
                                            output.write(file + ", " + branch_name + ", other failure" + "\n")
                                        pass

                                else:  # If a pr already exists for that file
                                    print("      [*] There is already a PR for this file, moving it out" )
                                    f.close()  # Close to prevent in use error
                                    try:
                                        print("      [*] Moving file...")
                                        os.rename(root + file, root + "verified_submitted/" + file)  # move the file
                                    except FileExistsError:
                                        print("      [!] File already exists! Removing current one.")
                                        with open("removed.txt", "a") as f:
                                            f.write(file + ", pr existed, file existed\n")
                                        os.remove(root + file)
                                        pass


                        #
                        # print(read_csv)
                        # input()

# get_open_prs(payload, headers, url)
check_if_exists(headers=headers)
