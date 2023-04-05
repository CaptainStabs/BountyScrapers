import requests
import json
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
        "fromBranchRepoName": "hospital-prices-allpayers",
        "toBranchOwnerName": "dolthub",
        "toBranchRepoName": "hospital-prices-allpayers", 
        "parentOwnerName": "dolthub",
        "parentRepoName": "hospital-prices-allpayers",
        "allowMaintainerToEditFromBranch": False
    },
        "query": "mutation CreatePullRequestWithForks($title: String!, $description: String!, $fromBranchName: String!, $toBranchName: String!, $fromBranchRepoName: String!, $fromBranchOwnerName: String!, $toBranchRepoName: String!, $toBranchOwnerName: String!, $parentRepoName: String!, $parentOwnerName: String!, $allowMaintainerToEditFromBranch: Boolean) {\n  createPullWithForks(\n    title: $title\n    description: $description\n    fromBranchName: $fromBranchName\n    toBranchName: $toBranchName\n    fromBranchOwnerName: $fromBranchOwnerName\n    fromBranchRepoName: $fromBranchRepoName\n    toBranchOwnerName: $toBranchOwnerName\n    toBranchRepoName: $toBranchRepoName\n    parentRepoName: $parentRepoName\n    parentOwnerName: $parentOwnerName\n    allowMaintainerToEditFromBranch: $allowMaintainerToEditFromBranch\n  ) {\n    _id\n    pullId\n    __typename\n  }\n}"
        })


    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
