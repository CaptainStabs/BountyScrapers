import pandas as pd
import requests
import json
from tqdm import tqdm

tqdm = tqdm.pandas()

def get_url(url, s):
    id = url.split('/')[-1]
    url = "https://www.dolthub.com/graphql"

    # Get commits
    payload = json.dumps({
      "operationName": "PullDiffForTableList",
      "variables": {
        "ownerName": "dolthub",
        "repoName": "quest",
        "pullId": id
      },
      "query": "query PullDiffForTableList($ownerName: String!, $repoName: String!, $pullId: String!) {\n  pullCommitDiff(repoName: $repoName, ownerName: $ownerName, pullId: $pullId) {\n    ...CommitDiffForTableList\n    __typename\n  }\n}\n\nfragment CommitDiffForTableList on CommitDiff {\n  _id\n  toOwnerName\n  toRepoName\n  toCommitId\n  fromOwnerName\n  fromRepoName\n  fromCommitId\n}"
    })

    try:
        r = s.post(url, data=payload).json()
    except requests.exceptions.JSONDecodeError:
        return None, None, None, None
    
    try:
      cd = r["data"]["pullCommitDiff"]
      from_id, to_id = cd["fromCommitId"], cd["toCommitId"]
    except KeyError:
        return None, None, None, None

    payload = json.dumps({
      "operationName": "DiffSummaryAsync",
      "variables": {
        "initialReq": {
          "fromRepoName": "quest",
          "fromOwnerName": "dolthub",
          "toRepoName": "quest",
          "toOwnerName": "captainstabs",
          "fromCommitId": from_id,
          "toCommitId": to_id
        }
      },
      "query": "query DiffSummaryAsync($initialReq: DiffSummaryReq, $resolvedReq: ResolvedDiffSummaryReq) {\n  diffSummaryAsync(initialReq: $initialReq, resolvedReq: $resolvedReq) {\n    resolvedReq {\n      fromCommitName\n      toCommitName\n      tableName\n      __typename\n    }\n    diffSummary {\n      ...DiffSummaryForDiffs\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment DiffSummaryForDiffs on DiffSummary {\n  rowsUnmodified\n  rowsAdded\n  rowsDeleted\n  rowsModified\n  cellsModified\n  rowCount\n  cellCount\n  __typename\n}\n"
    })

    r = s.post(url, data=payload)
    try:
        if "rpc error: code" not in r.text and "diff summary timed out" not in r.text:
            da = r.json()["data"]["diffSummaryAsync"]["diffSummary"]
            if da:
              added_rows = da["rowsAdded"]
              deleted_rows = da["rowsDeleted"]
              modified_rows = da["rowsModified"]
              modified_cells = da["cellsModified"]

              return added_rows, deleted_rows, modified_rows, modified_cells
            else:
              print(r.json())
    except KeyError:
        return None, None, None, None

    return None, None, None, None

headers = {
  'content-type': 'application/json',
  'host': 'www.dolthub.com'
}

s = requests.Session()
s.headers.update(headers)

# print(get_url("https://www.dolthub.com/repositories/dolthub/us-housing-prices/pulls/229", s))

df = pd.read_csv('prs.csv')

df[["added_rows", "deleted_rows", "modified_rows", "modified_cells"]] = df.progress_apply(lambda x: get_url(x["url"], s), axis=1, result_type='expand')
df.to_csv('prs_data.csv', index=False)
