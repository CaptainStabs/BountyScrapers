import requests
import json
import pandas as pd


def pull_diff(id, headers, url, file_urls):
    payload = json.dumps({
        "operationName": "PullDiffForTableList",
        "variables": {
        "ownerName": "dolthub",
        "repoName": "quest-small",
        "pullId": str(id)
        },
        "query": "query PullDiffForTableList($ownerName: String!, $repoName: String!, $pullId: String!) {\n  pullCommitDiff(repoName: $repoName, ownerName: $ownerName, pullId: $pullId) {\n    ...CommitDiffForTableList\n    __typename\n  }\n}\n\nfragment CommitDiffForTableList on CommitDiff {\n  _id\n  toOwnerName\n  toRepoName\n  toCommitId\n  fromOwnerName\n  fromRepoName\n  fromCommitId\n  tableDiffs {\n    ...TableDiffForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment TableDiffForTableList on TableDiff {\n  oldTable {\n    ...TableForDiffTableList\n    __typename\n  }\n  newTable {\n    ...TableForDiffTableList\n    __typename\n  }\n  numChangedSchemas\n  rowDiffColumns {\n    ...ColumnForDiffTableList\n    __typename\n  }\n  rowDiffs {\n    ...RowDiffListForTableList\n    __typename\n  }\n  schemaDiff {\n    ...SchemaDiffForTableList\n    __typename\n  }\n  schemaPatch\n  __typename\n}\n\nfragment TableForDiffTableList on Table {\n  tableName\n  columns {\n    ...ColumnForDiffTableList\n    __typename\n  }\n  __typename\n}\n\nfragment ColumnForDiffTableList on Column {\n  name\n  isPrimaryKey\n  type\n  constraints {\n    notNull\n    __typename\n  }\n  __typename\n}\n\nfragment RowDiffListForTableList on RowDiffList {\n  list {\n    ...RowDiffForTableList\n    __typename\n  }\n  nextPageToken\n  filterByRowTypeRequest {\n    pageToken\n    filterByRowType\n    __typename\n  }\n  __typename\n}\n\nfragment RowDiffForTableList on RowDiff {\n  added {\n    ...RowForTableList\n    __typename\n  }\n  deleted {\n    ...RowForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment RowForTableList on Row {\n  columnValues {\n    ...ColumnValueForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment ColumnValueForTableList on ColumnValue {\n  displayValue\n  __typename\n}\n\nfragment SchemaDiffForTableList on TextDiff {\n  leftLines {\n    ...SchemaDiffLineForTableList\n    __typename\n  }\n  rightLines {\n    ...SchemaDiffLineForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment SchemaDiffLineForTableList on Line {\n  content\n  lineNumber\n  type\n  __typename\n}\n"
    })

    r = requests.request("POST", url, headers=headers, data=payload).json()
    
    r = r["data"]["pullCommitDiff"]["tableDiffs"]
    # Find nested dict that is the file one
    for i, dic in enumerate(r):
        if dic["oldTable"]["tableName"] == "file":
            i = i
            break
    row_diffs = r[i]["rowDiffs"]["list"]
    
    next_page_token = r[i]["rowDiffs"]["nextPageToken"]

    file_urls = []
    with open("finished_files.txt", "a", newline="") as f:
        for row in row_diffs:
            col_vals = row["added"]["columnValues"]
            for col_val in col_vals:
                display_val = col_val["displayValue"]
                if "https" in display_val or "http" in display_val:
                    # f.write(f"{display_val}\n")
                    break


if __name__ == "__main__":
    headers = {
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'accept': '*/*',
        'content-type': 'application/json',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'host': 'www.dolthub.com'
    }
    # df = pd.read_csv("prs.csv")
    url = "https://www.dolthub.com/graphql"

    file_urls = set()
    pull_diff(6, headers, url, file_urls)





