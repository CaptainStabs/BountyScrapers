# Setup

1. Clone the repo, either via the command line, `git clone https://github.com/Police-Data-Accessibility-Project/Scrapers.git` or from the website.
2. `CD` into the `Scrapers` folder, and type `pip3 install -r requirements.txt`
3. Copy the extractor version you need, and the `configs.py` to the `COUNTRY/STATE/COUNTY` that you created for the precinct.
4. For example, Alameda county, California, would be placed into the folder `Scrapers/USA/CA/alameda/`.

   This **MUST** be placed within the `Scrapers` folder that you downloaded. See [here](https://github.com/Police-Data-Accessibility-Project/Scrapers/tree/master/USA/CA/alameda) for the example.

Open the `configs.py` file that you copied:
1. Set `webpage` to the page with the pdf lists

2. Open a few pdfs and get the common file path for them, and set that as `web_path`

3. Set the `domain` to the beginning of the document host.

4. On the page you want to scrape, open inspect element and using "Select an element", click the link to the pdf (once), and look at the element pane.

   If the `href` tag looks like the following, (without the domain, just a path), add the common portion of the path. In this case, it's `/Portals/24/Booking Log/` (Spaces *should* be properly dealt with in the script, but if not, just replace it with `%20`)


![image](https://user-images.githubusercontent.com/40151222/113303191-d5093200-92ce-11eb-8e42-0c23f70d9f47.png)

Also, if the `href` tag does not have a slash in front of it, like the following picture, please add one.

![image](https://user-images.githubusercontent.com/40151222/113487408-ffe9b680-9485-11eb-8942-b08fa7c1e528.png)

Make sure to add a slash to the end of the `domain`.
For example, `domain = "https://www.website.com"` would become `domain = "https://www.website.com/"`


 If the site has a set crawler time under it's `robots.txt`, set `sleep_time` to it's value. Otherwise, just leave it at `5`

If this does not make sense, try checking the comments within the code. (if you can find any)
 Working example can be found [here](https://github.com/Police-Data-Accessibility-Project/PDAP-Scrapers/blob/master/USA/CA/fresno_county/college/fresno/fresno_daily_scraper.py)

# Versions:
`list_pdf_extractor.py` : most basic of the scripts, mostly used for reference

`list_pdf_extractor_v2.py` : Uses imported `get_files` function. Useful for cases where a custom `get_files` is **not** needed. Function can be found [here](https://github.com/Police-Data-Accessibility-Project/PDAP-Scrapers/blob/master/common/utils/list_pdf_utils/get_files.py)

`list_pdf_extractor_v3.py` : Built off of V2, Allows for filtering links by common unwanted words. ~~See [golden_west_scraper.py](https://github.com/CaptainStabs/Scrapers/blob/master/USA/CA/golden_west_college/golden_west_scraper.py) for working example.~~


This script has two functions, the first, `extract_info`, extracts the links containing documents, and saves the url and the document name to a file called `links.txt`
The second function, `get_files`, reads the link and name from `links.txt` and downloads the files.  

#### Arguments:

As the `list_pdf_scrapers` all use a common modules, they accept the same arguments.

* `configs` : Required - comes with the template script, so no need to worry about it.
* `save_dir` : Required - comes with the template script, so no need to worry about it.

* `flavor` : Optional - Defaults to `stream`; (Used when `extract_tables` is True) accepted arguments are `stream` and `lattice`. Useful if the extracted data is jumbled (may not fix everything though).
* `extract_tables` : Optional - Defaults to False; if set to True, will attempt to extract tables from pdfs using [Camelot](https://camelot-py.readthedocs.io/en/master/).

The following 5 arguments are all passed to the `get_files` module. It's readme is located [here](https://github.com/Police-Data-Accessibility-Project/PDAP-Scrapers/blob/master/common/utils/list_pdf_utils/get_files_README.md)

* `name_in_url` : Optional - Defaults to True; As the name implies, if the document name is **NOT** in the url/path or in the `href`

* `extract_name` : Optional - Defaults to False; A different method of getting the document's name. Use if setting `name_in_url` to False did not work.

    Example of when to use: the `url_name.txt` file simply has something like `documentID?5311351`. Only works if the `href` contains a string, like `<a href="/DocumentID?">Annual Report 2020</a>` (This is of course, a highly simplified tag, there will be a lot more clutter on actual websites)
* `add_date` : Optional - Defaults to False; Use if a document is simply overwritten on a website without it's name being changed. Used in conjunction with `no_overwrite`
* `try_overwite` : Optional - Defaults to False; Mostly deprecated, check with a Director before using. Instead use `no_overwrite`
* `no_overwrite` : Optional - Defaults to False; Replaces `try_overwite`. Use in conjunction with `add_date`. As the name suggests, it prevents older documents from being overwritten, while still saving the new one if there are changes.

##### Arguments unique to V3

* `delete` : Optional - Defaults to True; if set to False, `url_name.txt` will not be deleted. This argument is also passed to `get_files` as it would delete the file once it was done with it.
* `important` : Optional - Defaults to False; if there are more files that you *don't* want than you do, you can filter out and only select items containing the keywords by setting to True. If set to True, rename `non_important` in the configs to `important` (it will work either way but not without complaining if it can't find `important`)


# More in depth explanations (Poorly explained, nerdy stuff)
 `extract_info` uses `urllib` to open the webpage, and then `BeautifulSoup4` to parse it. It then uses regex to find all links that end with pdf or doc. It needs a few lines to be replaced with regex.
