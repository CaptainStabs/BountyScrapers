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

    with GracefulInterruptHandler() as h:
        for root, dirs, files in os.walk(dir):
            if "verified_submitted" or "not_submitted" not in root:  # These are the "safe" folders
                for file in files:
                    if h.interrupted:
                        print("   [!] Interrupted, exiting.")
                        break

                    branch_name = "last_bounty"
                    db.checkout(branch=branch_name)
                    if ".csv" in file:                               # We only want the CSVs
                        with open(root + file, 'r') as f:
                            read_csv = csv.DictReader(f)
                            print("\n" + file)
                            success = True

                            if success:  # No point in wasting time on broken files
                                # response = requests.request("POST", url, headers=headers, data=payload)  # Don't need this anymore, used to check if the branch existed in  a PR

                                try:
                                    print("            [*] Trying to write to db...")
                                    filename = file.replace("_"," ").lower()
                                    dolt.write_file(dolt=db, table="menu_items", file_handle=open(root + file, "r"), import_mode="create", commit=True, commit_message=f"Add {filename}", do_continue=True, do_gc=False)
                                    success2 = True
                                        # dolt.write_file(dolt=db, table="menu_items", file_handle=open(filename, "r"), import_mode="create", do_continue=True)
                                except Exception as error:
                                        print(error)
                                        print("               [!] Write failure")
                                        if "dolt add" in str(error):
                                            print("         [!] Data was already added to database, skipping.")
                                            success2 = True
                                        else:
                                            success2 = False
                                            print("          [!] Other error, idk")
                                            with open("csv_fails.txt", "a") as output:  # Log the failure
                                                output.write(file + ", " + file + ", write failure" + "\n")
                                        pass

                                if success2:
                                    print("      [*] Finished push, moving" )
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



                                # """Being the early stages that dolt is in, these are primarily workarounds.
                                # Due to the (mostly) autonomous nature of this script, I don't want any errors interefering with it's progress.
                                # """
                                # print("            [*] Trying to push to remote")
                                # try:
                                #     db.push(remote="origin", set_upstream=True, refspec=branch_name)
                                #     success2 = True
                                #
                                # except Exception as error:
                                #     print("         [!] " + str(error))
                                #     print("               [!] Push failed")
                                #     with open("csv_fails.txt", "a") as output:  # Log the failure for manual review
                                #         output.write(file + ", " + file + ", push failure" + "\n")
                                #     sucess2 = False
                                #     pass
                                #
                                # if success2:  # If a pr already exists for that file
                                #     print("      [*] Finished push, moving" )
                                #     f.close()  # Close to prevent in use error
                                #
                                #     try:
                                #         print("      [*] Moving file...")
                                #         os.rename(root + file, root + "verified_submitted/" + file)  # move the file
                                #     except FileExistsError:
                                #         print("      [!] File already exists! Removing current one.")
                                #         with open("removed.txt", "a") as f:
                                #             f.write(file + ", pr existed, file existed\n")
                                #         os.remove(root + file)
                                #         pass


                        #
                        # print(read_csv)
                        # input()

# get_open_prs(payload, headers, url)
check_if_exists(headers=headers)
