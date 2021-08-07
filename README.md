# Order written (Just to help explain my mess)
1. fastfood_scraper.py
2. size_scraper.py
3. toasttab.py
4. toasttab_function.py
5. google_scraper.py
6. duck_scraper.py
7. csv_rety.py
8. chownow.py
9. submit_chownow.py
10. upserve.py
11. upserve_google_scraper.py
12. submit_all.py

# Uses
1. fastfood_scraper - Scrapes fastfoodnutrition.org, manual input
2. size_scraper - Scrapes sizes from fastfoodnutrition.org, manual input
3. toasttab - First version of non-function toasttab, manual input
4. toasttab_function - Semi automated toasttab scraper, automatically creates branch, can skip branches if they exist locally, and something about skipping something that exists, don't remember what.
5. google_scraper - Scrapes google for `site:toasttab` and iterates through them, sending them to `toasttab_function`
6. duck_scraper - Was supposed to scrape duckduckgo for any missed data, but the library duckduckpy didn't work how I needed it to.
7. csv_rety - Goes back through all the csvs in `./submited/`, tries to find the branch that the csv is related to, then attempts to write the data and open a pr if a pr is not already opened. contains two functions.
8. chownow - Scrape ChowNow website, and does pretty much the same workflow as toasttab_function
9. submit_chownow.py - Went through `/submited/` and did the same thing as csv_rety, but better.
10. upserve - Scrape upserve hosted menus.
11. upserve_google_scraper - Scrape google for `allinanchor:  "/s/" site:app.upserve.com` to find restaurants that use upserve as there was no way to find them through upserve's API or website (that I found, at least).
12. submit_all - After the bounty was closed early, we all had data left over that we would need to write to our master to open a PR with in the bounty v2. This is just a modified `submit_chownow` that does not create new branches or open PRs
