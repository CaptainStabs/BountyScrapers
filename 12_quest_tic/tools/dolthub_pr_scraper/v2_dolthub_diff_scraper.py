import requests
import json
import pandas as pd
import time
# import heartrate; heartrate.trace(browser=True, daemon=True)

from tqdm import tqdm
# Get's first 50 rows of diff & the next page token
def pull_diff(id, headers, url, file_urls):
    payload = json.dumps({
        "operationName": "PullDiffForTableList",
        "variables": {
        "ownerName": "dolthub",
        "repoName": "quest-v3",
        "pullId": str(id).strip("\n")
        },
        "query": "query PullDiffForTableList($ownerName: String!, $repoName: String!, $pullId: String!) {\n  pullCommitDiff(repoName: $repoName, ownerName: $ownerName, pullId: $pullId) {\n    ...CommitDiffForTableList\n    __typename\n  }\n}\n\nfragment CommitDiffForTableList on CommitDiff {\n  _id\n  toOwnerName\n  toRepoName\n  toCommitId\n  fromOwnerName\n  fromRepoName\n  fromCommitId\n  tableDiffs {\n    ...TableDiffForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment TableDiffForTableList on TableDiff {\n  oldTable {\n    ...TableForDiffTableList\n    __typename\n  }\n  newTable {\n    ...TableForDiffTableList\n    __typename\n  }\n  numChangedSchemas\n  rowDiffColumns {\n    ...ColumnForDiffTableList\n    __typename\n  }\n  rowDiffs {\n    ...RowDiffListForTableList\n    __typename\n  }\n  schemaDiff {\n    ...SchemaDiffForTableList\n    __typename\n  }\n  schemaPatch\n  __typename\n}\n\nfragment TableForDiffTableList on Table {\n  tableName\n  columns {\n    ...ColumnForDiffTableList\n    __typename\n  }\n  __typename\n}\n\nfragment ColumnForDiffTableList on Column {\n  name\n  isPrimaryKey\n  type\n  constraints {\n    notNull\n    __typename\n  }\n  __typename\n}\n\nfragment RowDiffListForTableList on RowDiffList {\n  list {\n    ...RowDiffForTableList\n    __typename\n  }\n  nextPageToken\n  filterByRowTypeRequest {\n    pageToken\n    filterByRowType\n    __typename\n  }\n  __typename\n}\n\nfragment RowDiffForTableList on RowDiff {\n  added {\n    ...RowForTableList\n    __typename\n  }\n  deleted {\n    ...RowForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment RowForTableList on Row {\n  columnValues {\n    ...ColumnValueForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment ColumnValueForTableList on ColumnValue {\n  displayValue\n  __typename\n}\n\nfragment SchemaDiffForTableList on TextDiff {\n  leftLines {\n    ...SchemaDiffLineForTableList\n    __typename\n  }\n  rightLines {\n    ...SchemaDiffLineForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment SchemaDiffLineForTableList on Line {\n  content\n  lineNumber\n  type\n  __typename\n}\n"
    })

    r = requests.request("POST", url, headers=headers, data=payload).json()
    
    r = r["data"]["pullCommitDiff"]["tableDiffs"]
    # Find nested dict that is the file one
    for i, dic in enumerate(r):
        old_table = dic["oldTable"]
        if old_table == None:
            if dic["newTable"]["tableName"] == "file":
               i = i
               break

        else:
            if old_table["tableName"] == "file":
                i = i
                break

    row_diffs = r[i]["rowDiffs"]["list"]
    
    next_page_token = r[i]["rowDiffs"]["nextPageToken"]

    for row in row_diffs:
        col_vals = row["added"]["columnValues"]
        for col_val in col_vals:
            display_val = col_val["displayValue"]
            if "https://" in display_val:
                if display_val not in file_urls:
                    file_urls.add(display_val)
                break
    return file_urls, next_page_token

def get_file_urls(row_list, file_urls):
    for row in row_list:
        col_vals = row["added"]["columnValues"]
        for col_val in col_vals:
            display_val = col_val["displayValue"]
            if "https://" in display_val:
                if display_val not in file_urls:
                    file_urls.add(display_val)
                break
    return file_urls

def next_page_row_diff(next_page_token, headers, url, file_urls) -> set:
    while next_page_token:
        # print("next_page_token is not none")
        payload = json.dumps({
            "operationName": "NextPageRowDiffs",
            "variables": {
                "pageToken": str(next_page_token)
            },
            "query": "query NextPageRowDiffs($pageToken: String!, $filterByRowType: DiffRowType) {\n  rowDiffs(pageToken: $pageToken, filterByRowType: $filterByRowType) {\n    ...RowDiffListForTableList\n    __typename\n  }\n}\n\nfragment RowDiffListForTableList on RowDiffList {\n  list {\n    ...RowDiffForTableList\n    __typename\n  }\n  nextPageToken\n  filterByRowTypeRequest {\n    pageToken\n    filterByRowType\n    __typename\n  }\n  __typename\n}\n\nfragment RowDiffForTableList on RowDiff {\n  added {\n    ...RowForTableList\n    __typename\n  }\n  deleted {\n    ...RowForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment RowForTableList on Row {\n  columnValues {\n    ...ColumnValueForTableList\n    __typename\n  }\n  __typename\n}\n\nfragment ColumnValueForTableList on ColumnValue {\n  displayValue\n  __typename\n}\n"
        })

        tries = 0
        while tries < 3:
            try:
                r = requests.request("POST", url, headers=headers, data=payload).json()
            except requests.exceptions.ConnectionError:
                time.sleep(2)
                tries +=1
            # API always returns 200 so error checking has to be done this way
            if r.get("errors"):
                print(f"Got an error,\n{next_page_token}")
                tries += 1 
                time.sleep(1)

            if r.get("data"):
                tries = 4
        try:
            r = r["data"]["rowDiffs"]
        except:
            print(r)
            raise
        
        row_list = r.get("list", [])

        file_urls = get_file_urls(row_list, file_urls)
        
        next_page_token = r.get("nextPageToken", None)
    return file_urls

def main(id, headers, url, file_urls):
    # Gets the first 50 rows, saves them in set
    file_urls, next_page_token = pull_diff(id, headers, url, file_urls)
    file_urls = next_page_row_diff(next_page_token, headers, url, file_urls)
    return file_urls

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
    
    with open("./prs/uhc_prs.csv", "r") as f:
        total = len(f.readlines())
        f.seek(0) # skip header
        
        for line in tqdm(f, total=total):
            id = line.split(",")[0].replace('"', '')
            file_url = main(id, headers, url, file_urls)
            file_urls = file_urls.union(file_url)
            print("\n", len(file_urls))

    with open("uhc_finished_files.txt", "a", newline="") as f:
        f.write("url\n") # Write header
        for url in file_urls:
            f.write(url + "\n")
            
