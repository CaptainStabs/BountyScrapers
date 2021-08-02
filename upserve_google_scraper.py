import googlesearch as google
from upserve import upserve_scraper
from utils.interrupt_handler import GracefulInterruptHandler
import json
from _cookie import dolt_cookie

search_query = 'allinanchor:  "/s/" site:app.upserve.com'
ignored_domains = ["google"]
remove_words = ["?mode=create"]
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

user_agent = google.get_random_user_agent()
print(user_agent)

print("   [*] Loop start")
with GracefulInterruptHandler() as h:
    for results in google.search(search_query, lang="en", num=10, start=0, stop=None, pause=5, user_agent=user_agent):
        if h.interrupted:
            print("   [!] Interrupted, exiting.")
            break
        # print("All result: " + results
        # print("   All result: " + results)
        print(results)
        print("Scraping")
        upserve_scraper(results, headers, payload)
        # try:
        #     print("Scraping")
        #     upserve_scraper(results, headers, payload)
        # except Exception as e:
        #     print("   [!] Unable to scrape. Error: " + str(e))
        #     pass
