import requests
import json
import pandas as pd


def pull_diff(id, headers, url):
    payload = json.dumps({
        "operationName": "PullDiffForTableList",
        "variables": {
            "ownerName": "dolthub",
            "repoName": "quest",
            "pullId": f"{id}"
        },
        "query": "query PullDiffForTableList($ownerName: String!, $repoName: String!, $pullId: String!) {\n  pullCommitDiff(repoName: $repoName, ownerName: $ownerName, pullId: $pullId) {\n    ...CommitDiffForTableList\n    __typename\n  }\n}\n\nfragment CommitDiffForTableList on CommitDiff {\n  _id\n  toOwnerName\n  toRepoName\n  toCommitId\n  fromOwnerName\n  fromRepoName\n  fromCommitId\n  tableDiffs {\n    ...TableDiffForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment TableDiffForTableList on TableDiff {\n  oldTable {\n    ...TableForDiffTableList\n    __typename\n  }\n  newTable {\n    ...TableForDiffTableList\n    __typename\n  }\n  numChangedSchemas\n  rowDiffColumns {\n    ...ColumnForDiffTableList\n    __typename\n  }\n  rowDiffs {\n    ...RowDiffListForTableList\n    __typename\n  }\n  schemaDiff {\n    ...SchemaDiffForTableList\n    __typename\n  }\n  schemaPatch\n  __typename\n}\n\nfragment TableForDiffTableList on Table {\n  tableName\n  columns {\n    ...ColumnForDiffTableList\n    __typename\n  }\n  __typename\n}\n\nfragment ColumnForDiffTableList on Column {\n  name\n  isPrimaryKey\n  type\n  constraints {\n    notNull\n    __typename\n  }\n  __typename\n}\n\nfragment RowDiffListForTableList on RowDiffList {\n  list {\n    ...RowDiffForTableList\n    __typename\n  }\n  nextPageToken\n  filterByRowTypeRequest {\n    pageToken\n    filterByRowType\n    __typename\n  }\n  __typename\n}\n\nfragment RowDiffForTableList on RowDiff {\n  added {\n    ...RowForTableList\n    __typename\n  }\n  deleted {\n    ...RowForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment RowForTableList on Row {\n  columnValues {\n    ...ColumnValueForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment ColumnValueForTableList on ColumnValue {\n  displayValue\n  __typename\n}\n\nfragment SchemaDiffForTableList on TextDiff {\n  leftLines {\n    ...SchemaDiffLineForTableList\n    __typename\n  }\n  rightLines {\n    ...SchemaDiffLineForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment SchemaDiffLineForTableList on Line {\n  content\n  lineNumber\n  type\n  __typename\n}\n"
        })

    r = requests.request("POST", url, headers=headers, data=payload).json()
    r = r["data"]["pullCommitDiff"]
    to_commit = r["toCommitId"]
    from_commit = r["fromCommitId"]
    return to_commit, from_commit


def next_page_token(owner_name, headers, url):
    payload = json.dumps({
    "operationName": "RowsForDataTableQuery",
    "variables": {
        "ownerName": f"{owner_name}",
        "repoName": "quest-small",
        "refName": "main",
        "tableName": "file",
        "revisionType": "RefName"
    },
    "query": "query RowsForDataTableQuery($ownerName: String!, $repoName: String!, $refName: String!, $revisionType: RevisionType!, $tableName: String!, $pageToken: String) {\n  rows(\n    ownerName: $ownerName\n    repoName: $repoName\n    revisionName: $refName\n    tableName: $tableName\n    revisionType: $revisionType\n    pageToken: $pageToken\n  ) {\n    ...RowListRows\n    __typename\n  }\n}\n\nfragment RowListRows on RowList {\n  nextPageToken\n  prevPageToken\n  list {\n    ...RowForDataTable\n    __typename\n  }\n  __typename\n}\n\nfragment RowForDataTable on Row {\n  columnValues {\n    displayValue\n    __typename\n  }\n  __typename\n}\n"
    })

    r = requests.request("POST", url, headers=headers, data=payload).json()
    print(r)
    r = r["data"]["rows"]
    next_page_token = r.get("nextPageToken")
    return next_page_token

def get_file_urls(row_list, file_urls):
    for row in row_list:
        file_url = row["added"]["columnValues"][1]
        if file_url not in file_urls:
            file_urls.add(file_url)
    return file_urls

# This will require a while loop that loops while there is still a next page token
def next_page_row_diff(next_page_token, headers, url) -> set:
    file_urls = set()
    while next_page_token is not None:
        payload = json.dumps({
            "operationName": "NextPageRowDiffs",
            "variables": {
                "pageToken": str(next_page_token)
            },
            "query": "query NextPageRowDiffs($pageToken: String!, $filterByRowType: DiffRowType) {\n  rowDiffs(pageToken: $pageToken, filterByRowType: $filterByRowType) {\n    ...RowDiffListForTableList\n    __typename\n  }\n}\n\nfragment RowDiffListForTableList on RowDiffList {\n  list {\n    ...RowDiffForTableList\n    __typename\n  }\n  nextPageToken\n  filterByRowTypeRequest {\n    pageToken\n    filterByRowType\n    __typename\n  }\n  __typename\n}\n\nfragment RowDiffForTableList on RowDiff {\n  added {\n    ...RowForTableList\n    __typename\n  }\n  deleted {\n    ...RowForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment RowForTableList on Row {\n  columnValues {\n    ...ColumnValueForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment ColumnValueForTableList on ColumnValue {\n  displayValue\n  __typename\n}\n"
        })

        r = requests.request("POST", url, headers=headers, data=payload).json()
        r = r["data"]["rowDiffs"]
        
        row_list = r.get("list", [])

        file_urls = get_file_urls(row_list, file_urls)
        
        next_page_token = r.get("nextPageToken", None)
        print(file_urls)
    return file_urls

    def get_pr_info(id, username, headers):
        url = "https://www.dolthub.com/graphql"

        to_commit, from_commit =  pull_diff(id, headers, url)






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
    npt = next_page_token("captainstabs", headers, url)


    f = next_page_row_diff(npt, headers, url)

    






