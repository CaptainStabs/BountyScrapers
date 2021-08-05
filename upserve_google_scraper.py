import googlesearch as google
from upserve import upserve_scraper
from utils.interrupt_handler import GracefulInterruptHandler
import json
from _cookie import dolt_cookie
import time

search_query = 'allinanchor:  "/s/" site:app.upserve.com'
ignored_domains = ["google"]
remove_words = ["?mode=create"]
payload = {}
headers = {
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'DNT':  '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
}

user_agent = google.get_random_user_agent()
print(user_agent)

print("\n   [*] Loop start")
with GracefulInterruptHandler() as h:
    for results in google.search(search_query, lang="en", num=10, start=0, stop=None, pause=5, user_agent=user_agent):
        if h.interrupted:
            print("   [!] Interrupted, exiting.")
            break
        # print("All result: " + results
        # print("   All result: " + results)
        print("\n" + str(results))
        print("Scraping")
        upserve_scraper(results, headers, payload)
        time.sleep(1)
        # try:
        #     print("Scraping")
        #     upserve_scraper(results, headers, payload)
        # except Exception as e:
        #     print("   [!] Unable to scrape. Error: " + str(e))
        #     pass
