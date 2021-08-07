import duckduckpy

query =  duckduckpy.query("site:toasttab.com")


for results in query:
    # print("All result: " + results
    # print("   All result: " + results)
    print(dir(results))
    try:
        print("Scraping")
        toast_tab_scraper(results[results], skip_existing=True, pull_master=False,  local_branches=False)
    except:
        # print(exception)
        pass
