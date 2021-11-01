import requests
from lxml.html import fromstring
import csv
import pandas as pd
from utils.business_parser import business_type_parser
import os
import usaddress
from tqdm import tqdm
from random import randrange

headers = {
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document'
}

columns = ["name", "business_type", "state_registered", "street_registered", "city_registered", "zip5_registered", "state_physical", "street_physical", "city_physical", "zip5_physical", "filing_number", "agent_name", "agent_title", "raw_physical_address", "raw_registered_address"]
s = requests.Session()
s.headers.update(headers)

last_id = 7389000
j = last_id
with open("max.txt", "a", newline="") as f:
    for corp_id in tqdm(range(last_id, 7900000)):
        corp_id_2 = corp_id + randrange(13)
        print(j, corp_id, corp_id_2)
        if j > corp_id_2:
            while corp_id_2 < j:
                corp_id_2 = corp_id + randrange(13)
                print(corp_id_2)
        j = corp_id_2
        print(j, corp_id, corp_id_2)

        print(f"   [*] Current ID: {corp_id_2}")
        '''
        Step 1:
        Need to get the first search page to search for ID
        '''

        # Get search page
        url = "https://www.corporations.pa.gov/search/corpsearch"
        response = s.request("GET", url, headers=headers)

        # Parse raw html with lxml
        parser = fromstring(response.text)

        event_validation = parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
        view_state = parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]

        # Setup payload
        payload = {
            '__EVENTTARGET': '',
            '__EVENTVALIDATION': event_validation,
            '__VIEWSTATE': view_state,
            'ctl00$MainContent$btnSearch': 'Search',
            'ctl00$MainContent$ddlSearchType': '1',
            'ctl00$MainContent$txtSearchTerms': corp_id_2,
            'ctl00$MainContent$ddlSearchType': '6' # Exact match search
        }


        # Get "Select Business Entity page"
        result_page = s.request("POST", url, data=payload)

        # Get view stuff from this page, and buttons daat
        result_parser = fromstring(result_page.text)

        # Get aspx junk for step 2 request
        event_validation_2 = result_parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
        view_state_2 = result_parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]

        try:
            business_status = str(result_parser.xpath('//*[@id="lblBEStatus"]/text()')[0]).upper().strip()
            print("    [*] Name: " + str(result_parser.xpath('//*[@id="lnkBEName"]/text()')[0]).strip())
            print(f"      [*] Business Status: {business_status}")
            got_results = True
        except IndexError:
            # This is caused by no results being returned
            print("    [!] Business status not found!")
            got_results = False

        # Prevent rest of script from running
        if got_results:
            print(f"         [!!!] Found business! ID: {corp_id_2}")
            f.write(str(corp_id) + "\n")
