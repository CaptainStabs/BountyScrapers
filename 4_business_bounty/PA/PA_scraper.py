import requests
from lxml.html import fromstring
import csv
import pandas as pd
from utils.business_parser import business_type_parser

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

columns = ["name", "business_type", "state_registered", "street_registered", "city_registered", "zip5_registered", "state_physical", "street_physical", "city_physical", "zip5_physical", "filing_number"]

for corp_id in range(0,89999999):
    '''
    Step 1:
    Need to get the first search page to search for ID
    '''
    # Get search page
    url = "https://www.corporations.pa.gov/search/corpsearch"
    response = requests.request("GET", url, headers=headers)

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
        'ctl00$MainContent$txtSearchTerms': corp_id
        'ctl00$MainContent$ddlSearchType': '6' # Exact match search
    }


    # Get "Select Business Entity page"
    result_page = requests.request("POST", url, data=payload)

    # Get view stuff from this page, and buttons daat
    result_parser = fromstring(result_page.text)

    # Get aspx junk for step 2 request
    event_validation_2 = result_parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
    view_state_2 = result_parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]

    business_status = str(result_parser.xpath('//*[@id="lblBEStatus"]')[0]).upper().strip()
    if business_status == "ACTIVE":
        '''
        Step 2:
        After searching, we need to get the view_state and event_validation once again
        EVENTTARGET is from the result list link pointing to entity name
        This step (finally) gets the actual business info
        '''

        payload = {
            '__EVENTARGUMENT': '',
            '__EVENTTARGET': 'ctl00$MainContent$gvResults$ctl02$lnkBEName',
            '__EVENTVALIDATION': event_validation_2,
            '__VIEWSTATE': view_state_2
        }


        business_page = requests.request("POST", url, headers=headers, data=payload)
        business_parser = fromstring(business_page.text)

        df = pd.read_html(business_page.text)
        entity_details = df[1]
        info_dict = entity_details.set_index(0).to_dict()

        business_info = {
            "name": " ".join(str(business_parser.xpath('//td[@align="left"]/text()')[0]).strip().upper().split()),
            "business_type": "CORPORATION", # This will get replaced if it is parsed
            "state_registered": str(info_dict[1]["State of Inc"]).upper().strip(),
            "filing_number": str(info_dict[1]["Entity Number"]).strip()
            }

        print("   [*] Name: " + str(business_parser.xpath('//td[@align="left"]/text()')[0]).strip())



        """Parse physical address"""

        raw_physical_address = info_dict[1]['Address']

        try:
            parsed_address = usaddress.tag(raw_physical_address)
            parse_success = True

        except usaddress.RepeatedLabelError as e:
            print(e)
            parse_success = False


        if parse_success:
            street_physical = " ".join(str(raw_physical_address.split(parsed_address[0]["PlaceName"])[0]).strip(",").strip()..upper().split())

            business_info["street_physical"] = street_physical
            try:
                business_info["city_physical"] = " ".join(str(parsed_address[0]["PlaceName"]).strip(",").strip().upper().split())
            except KeyError:
                print("   [!] City physical key error!")

            try:
                business_info["zip5_physical"] = str(parsed_address[0]["ZipCode"]).strip()
            except KeyError:
                print("   [!] Zip code key error!")


        # Registered agent will need a check to see if officer table exists


        business_type_string = info_dict[1]["Entity Type"]
        business_info["business_type"] = business_type_parser(business_type_string)



    else:
        print(f"   [!] Business not active: {business_status}")
