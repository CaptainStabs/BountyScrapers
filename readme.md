# Order written (Just to help explain my mess)
1. fastfood_scraper
2. size_scraper
3. toasttab
4. toasttab_function
5. google_scraper
6. duck_scraper
7. csv_rety

# Uses
1. fastfood_scraper - Scrapes fastfoodnutrition.org, manual input
2. size_scraper - Scrapes sizes from fastfoodnutrition.org, manual input
3. toasttab - First version of non-function toasttab, manual input
4. toasttab_function - Semi automated toasttab scraper, automatically creates branch, can skip branches if they exist locally, and something about skipping something that exists, don't remember what.
5. google_scraper - Scrapes google for `site:toasttab` and iterates through them, sending them to `toasttab_function`
6. duck_scraper - Was supposed to scrape duckduckgo for any missed data, but the library duckduckpy didn't work how I needed it to.
7. csv_rety - Goes back through all the csvs in `./submited/`, tries to find the branch that the csv is related to, then attempts to write the data and open a pr if a pr is not already opened. contains two functions.
