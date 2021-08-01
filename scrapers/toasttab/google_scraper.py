import googlesearch as google
from toasttab_function import toast_tab_scraper

search_query = "site:https://www.toasttab.com/"
ignored_domains = ["google"]
remove_words = ["?mode=create"]
print("   [*] Loop start")
# with open("urls.txt", "a") as output:
#     for results in google.search(search_query, tld="com", lang="en", num=10, start=0, stop=None, pause=2.0):
#         # print("All result: " + results)
#         if not any(ignored_domain in results for ignored_domain in ignored_domains):
#             # print("   All result: " + results)
#             print(results)
#             try:
#                 print("Scraping")
#                 toast_tab_scraper(results)
#             except exception:
#                 print(exception)
#                 pass


for results in google.search(search_query, tld="com", lang="en", num=100, start=0, stop=None, pause=0.3):
    # print("All result: " + results
    # print("   All result: " + results)
    print(results)
    try:
        print("Scraping")
        toast_tab_scraper(results, skip_existing=True, pull_master=False,  local_branches=False)
    except:
        # print(exception)
        pass
