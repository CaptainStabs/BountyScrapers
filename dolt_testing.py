import csv
import os
import json
import doltcli as dolt
import requests
import googlesearch as google
from urllib.parse import urlparse
import re
import time
from _cookie import dolt_cookie


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
    'Cookie': f'{dolt_cookie}'
}

# this function is used for gathering time stats
def function_timer(stats):
    if stats != False:
        return time.perf_counter()

# this function simply calculates and prints the difference between the end and start times
def time_dif(stats, string, start, end):
    if stats != False:
        print(f"{string}: {end - start} seconds")

def get_open_prs(payload, headers, url):
    is_nextpagetoken = True
    pull_id = []
    response = requests.request("POST", url, headers=headers, data=payload)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=4))
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
            pull_id.append(row["pullId"])
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
    ###  Once there is no nextPageToken, this will write
    with open("pull_ids.txt", "w") as output:
        output.write(str(pull_id))
    print(pull_id)

def remove_pulls(start_id, end_id):
    print(f"   [*] Removing pulls in the range {start_id}-{end_id}")
    with open("pull_ids.txt", "r") as input:
        pull_ids_input = input.readlines()
        pull_ids_str = str(pull_ids_input).replace("[", "").replace("]", "")
        pull_ids_list = pull_ids_str.split(", ")
        # print(from_branches)

    new_pull_id_list = []
    with open("new_pull_ids.txt", "w") as output:
        for pull_ids in pull_ids_list:  # Not sure why i have to iterate like this
            pull_id = re.sub("[^0-9a-zA-Z]+", "", pull_ids)
            if int(pull_id) not in range(start_id, end_id):
                new_pull_id_list.append(int(pull_id))
            else:
                continue
        removed_diff = len(pull_ids_list) - len(new_pull_id_list)
        print("      [*] Removed " + str(removed_diff) + " PRs")
        print("      [*] Removing old pull id file")
        os.remove("pull_ids.txt")
        print("      [*] Renaming to pull_ids.txt")
        os.rename("new_pull_ids.txt", "pull_ids.txt")
        output.write(str(new_pull_id_list))
        print("   [*] Finished")

def get_diff(headers, stats=False):
    running_total = 0
    print("   [*] Extracting Pull IDs")
    with open("pull_ids.txt", "r") as output:
        pull_ids = output.readlines()
        pull_ids_str = str(pull_ids).replace("[", "").replace("]", "")
        pull_ids_list = pull_ids_str.split(", ")

    print("   [*] Beginning Loop")
    for pull_ids in pull_ids_list:  # I'm aware that this is bad
        pull_ID = re.sub("[^0-9a-zA-Z]+", "", str(pull_ids))
        print("      [*] Pull ID: " + str(pull_ID))
        # print(type(pull_ID))
        # print(type(pull_ids))
        # print(pull_ID)

        commit_payload = json.dumps({
            "operationName": "PullDiffForTableList",
            "variables": {
                "ownerName": "dolthub",
                "repoName": "menus",
                "pullId": f"{pull_ID}"
                },
            "query":"query PullDiffForTableList($ownerName: String!, $repoName: String!, $pullId: String!) {\n  pullCommitDiff(repoName: $repoName, ownerName: $ownerName, pullId: $pullId) {\n    ...CommitDiffForTableList\n    __typename\n  }\n}\n\nfragment CommitDiffForTableList on CommitDiff {\n  toCommitId\n fromCommitId\n  }\n"
        })

        success1 = False
        try:
            print("      [*] PullDiffForTableList")
            commit_start = function_timer(stats)
            commit_response = requests.request("POST", url, headers=headers, data=commit_payload)
            commit_end = function_timer(stats)
            print("         [*] Finished ^")
            time_dif(stats, "PullDiffForTableList request time", commit_start, commit_end)

            print(commit_response.text)
            commit_json = json.loads(commit_response.text)
            pull_commit_diff = commit_json["data"]["pullCommitDiff"]
            to_commit_id = pull_commit_diff["toCommitId"]
            from_commit_id = pull_commit_diff["fromCommitId"]
            success1 = True

        except json.decoder.JSONDecodeError:
            print("      [*] Failed to decode")
            success1 = False
            fail_count += 1
            if fail_count > 2:
                print("      [!] Still not working, giving up....")
                break
            pass

        diff_payload = json.dumps({
            "operationName": "DiffSummaryAsync",
            "variables": {
                "initialReq": {
                    "fromRepoName": "menus",
                    "fromOwnerName": "dolthub",
                    "toRepoName": "menus",
                    "toOwnerName": "captainstabs",
                    "fromCommitId": f"{from_commit_id}",
                    "toCommitId": f"{to_commit_id}"
                }
            },
            "query": "query DiffSummaryAsync($initialReq: DiffSummaryReq, $resolvedReq: ResolvedDiffSummaryReq) {\n  diffSummaryAsync(initialReq: $initialReq, resolvedReq: $resolvedReq) {\n    resolvedReq {\n      fromCommitName\n      toCommitName\n      tableName\n      __typename\n    }\n    diffSummary {\n      ...DiffSummaryForDiffs\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment DiffSummaryForDiffs on DiffSummary {\n  rowsUnmodified\n  rowsAdded\n  rowsDeleted\n  rowsModified\n  cellsModified\n  rowCount\n  cellCount\n  __typename\n}\n"
        })

        if success1:
            success = False
            fail_count = 0
            while not success:
                try:
                    print("      [*] Getting DiffSummary")
                    diff_start = function_timer(stats)
                    diff_response = requests.request("POST", url, headers=headers, data=diff_payload)
                    diff_end = function_timer(stats)
                    time_dif(stats, "DiffSUmmary response time", diff_start, diff_end)
                    print(diff_response.text)

                    diff_parsed = json.loads(diff_response.text)
                    diff_data = diff_parsed["data"]["diffSummaryAsync"]["diffSummary"]
                    rows_added = diff_data["rowsAdded"]
                    running_total = running_total + int(rows_added)
                    print("      [*] Running total: " + str(running_total))
                    # print(to_commit_id)
                    time.sleep(0.5)
                    success = True

                except TypeError:
                    print("      [*] Whoops, trying again.")
                    success = False
                    fail_count += 1
                    if fail_count > 2:
                        print("      [!] Still not working, giving up....")
                        break
                    pass
        else:
            continue


# get_open_prs(payload, headers, url)
# remove_pulls(43644, 46122)
get_diff(headers, stats=True)
