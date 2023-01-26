import requests
import json
import argparse
from ._secrets import cookie

headers = {
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'accept': '*/*',
        'content-type': 'application/json',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'host': 'www.dolthub.com',
        'cookie': cookie
        }

def make_pr(title, branch):
    url = "https://www.dolthub.com/graphql"

    payload = json.dumps({
    "operationName": "CreatePullRequestWithForks",
    "variables": {
        "title": f"{title}",
        "description": "",
        "fromBranchName": f"{branch}",
        "toBranchName": "main",
        "fromBranchOwnerName": "captainstabs",
        "fromBranchRepoName": "quest-small",
        "toBranchOwnerName": "dolthub",
        "toBranchRepoName": "quest-small",
        "parentOwnerName": "dolthub",
        "parentRepoName": "quest-small",
        "allowMaintainerToEditFromBranch": False
    },
        "query": "mutation CreatePullRequestWithForks($title: String!, $description: String!, $fromBranchName: String!, $toBranchName: String!, $fromBranchRepoName: String!, $fromBranchOwnerName: String!, $toBranchRepoName: String!, $toBranchOwnerName: String!, $parentRepoName: String!, $parentOwnerName: String!, $allowMaintainerToEditFromBranch: Boolean) {\n  createPullWithForks(\n    title: $title\n    description: $description\n    fromBranchName: $fromBranchName\n    toBranchName: $toBranchName\n    fromBranchOwnerName: $fromBranchOwnerName\n    fromBranchRepoName: $fromBranchRepoName\n    toBranchOwnerName: $toBranchOwnerName\n    toBranchRepoName: $toBranchRepoName\n    parentRepoName: $parentRepoName\n    parentOwnerName: $parentOwnerName\n    allowMaintainerToEditFromBranch: $allowMaintainerToEditFromBranch\n  ) {\n    _id\n    pullId\n    __typename\n  }\n}\n"
        })


    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--title", type=str, required=True)
    parser.add_argument("-b", "--branch", type=str, required=True)
    args = parser.parse_args()
    make_pr(args.title, args.branch)
