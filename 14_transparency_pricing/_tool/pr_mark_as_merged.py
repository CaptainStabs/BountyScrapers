import requests
import json
import argparse


def mark_as_merged(pull_id):
    dolthub_token = ''


    headers = {
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'accept': '*/*',
    'content-type': 'application/json',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'host': 'www.dolthub.com',
    'Cookie': f'dolthubToken={dolthub_token}'
    }


    url = "https://www.dolthub.com/graphql"

    payload = json.dumps({
    "operationName": "PullForPullDetailsQuery",
    "variables": {
        "ownerName": "dolthub",
        "repoName": "transparency-in-pricing",
        "pullId": pull_id
    },
    "query": "query PullForPullDetailsQuery($repoName: String!, $ownerName: String!, $pullId: String!) {\n  pull(repoName: $repoName, ownerName: $ownerName, pullId: $pullId) {\n    ...PullForPullDetails\n    __typename\n  }\n}\n\nfragment PullForPullDetails on Pull {\n  _id\n  pullId\n  state\n  title\n  description\n  fromBranchName\n  fromBranchOwnerName\n  fromBranchRepoName\n  toBranchName\n  toBranchOwnerName\n  toBranchRepoName\n  creatorName\n  isFork\n  createdAt\n  allowMaintainerToEditFromBranch\n  __typename\n}"
    })

    response = requests.request("POST", url, headers=headers, data=payload)



    jd = response.json()


    jd = jd['data']['pull']
    title = jd['title']
    description = jd['description']


    payload = json.dumps({
    "operationName": "UpdatePullInfo",
    "variables": {
        "_id": f"repositoryOwners/dolthub/repositories/transparency-in-pricing/pulls/{pull_id}",
        "state": "Merged",
        "title": title,
        "description": description,
        "allowMaintainerToEditFromBranch": False
    },
    "query": "mutation UpdatePullInfo($_id: String!, $title: String!, $description: String!, $state: PullState!, $allowMaintainerToEditFromBranch: Boolean!) {\n  updatePull(\n    _id: $_id\n    title: $title\n    description: $description\n    state: $state\n    allowMaintainerToEditFromBranch: $allowMaintainerToEditFromBranch\n  ) {\n    _id\n    __typename\n  }\n}\n"
    })

    requests.request("POST", url, headers=headers, data=payload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pull_id", type=str)
    args = parser.parse_args()
    mark_as_merged(args.pull_id)


