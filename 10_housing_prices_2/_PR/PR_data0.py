import pandas as pd
import requests
import json
from tqdm import tqdm

tqdm = tqdm.pandas()

def get_url(url, s):
    id = url.split('/')[-1]
    print("ID",id)
    url = "https://www.dolthub.com/graphql"

    # Get commits
    payload = json.dumps({
      "operationName": "PullDiffForTableList",
      "variables": {
        "ownerName": "dolthub",
        "repoName": "us-housing-prices",
        "pullId": id
      },
      "query": "query PullDiffForTableList($ownerName: String!, $repoName: String!, $pullId: String!) {\n  pullCommitDiff(repoName: $repoName, ownerName: $ownerName, pullId: $pullId) {\n    ...CommitDiffForTableList\n    __typename\n  }\n}\n\nfragment CommitDiffForTableList on CommitDiff {\n  _id\n  toOwnerName\n  toRepoName\n  toCommitId\n  fromOwnerName\n  fromRepoName\n  fromCommitId\n}"
    })

    try:
        success = 0
        while success < 5:
            try:
                r = s.post(url, data=payload).json()
                success = 6
            except requests.exceptions.JSONDecodeError:
                success += 1
    except requests.exceptions.JSONDecodeError:
        return None, None, None, None

    # print(r)
    cd = r["data"]["pullCommitDiff"]
    from_id, to_id = cd["fromCommitId"], cd["toCommitId"]

    payload = json.dumps({
      "operationName": "DiffSummaryAsync",
      "variables": {
        "initialReq": {
          "fromRepoName": "us-housing-prices",
          "fromOwnerName": "dolthub",
          "toRepoName": "us-housing-prices",
          "toOwnerName": cd["toOwnerName"],
          "fromCommitId": from_id,
          "toCommitId": to_id
        }
      },
      "query": "query DiffSummaryAsync($initialReq: DiffSummaryReq, $resolvedReq: ResolvedDiffSummaryReq) {\n  diffSummaryAsync(initialReq: $initialReq, resolvedReq: $resolvedReq) {\n    resolvedReq {\n      fromCommitName\n      toCommitName\n      tableName\n      __typename\n    }\n    diffSummary {\n      ...DiffSummaryForDiffs\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment DiffSummaryForDiffs on DiffSummary {\n  rowsUnmodified\n  rowsAdded\n  rowsDeleted\n  rowsModified\n  cellsModified\n  rowCount\n  cellCount\n  __typename\n}\n"
    })


    r = s.post(url, data=payload)
    # r = s.post(url, data=payload)

    try:
        if "rpc error: code" not in r.text and "diff summary timed out" not in r.text:
            da = r.json()["data"]["diffSummaryAsync"]["diffSummary"]
            if da:
                added_rows = da["rowsAdded"]
                deleted_rows = da["rowsDeleted"]
                modified_rows = da["rowsModified"]
                modified_cells = da["cellsModified"]

                return added_rows, deleted_rows, modified_rows, modified_cells
    except requests.exceptions.JSONDecodeError:
        return None, None, None, None

    return None, None, None, None

headers = {
  'content-type': 'application/json',
  'host': 'www.dolthub.com'
}

s = requests.Session()
s.headers.update(headers)

# print(get_url("https://www.dolthub.com/repositories/dolthub/us-housing-prices/pulls/229", s))

df = pd.read_csv('dolthub.csv')
#
df[["added_rows", "deleted_rows", "modified_rows", "modified_cells"]] = df.progress_apply(lambda x: get_url(x["url"], s), axis=1, result_type='expand')
df.to_csv('prs_data2.csv', index=False)
