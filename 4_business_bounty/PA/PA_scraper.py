import requests
from lxml.html import fromstring
import csv
import pandas as pd
from utils.business_parser import business_type_parser
import os
import usaddress
from tqdm import tqdm

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

filename = "pa.csv"
if os.path.exists(filename) and os.stat(filename).st_size > 0:
    df = pd.read_csv(filename)
    df_columns = list(df.columns)
    data_columns = ",".join(map(str, df_columns))

    # Get the last row from df
    last_row = df.tail(1)
    # Access the corp_id
    last_id = last_row["filing_number"].values[0]
    last_id += 1
else:
    last_id = 1

with open(filename, "a", encoding="utf-8", newline="") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=columns)

    if os.stat(filename).st_size == 0:
        writer.writeheader()

    for corp_id in tqdm(range(last_id, 89999999)):
        print(f"   [*] Current ID: {corp_id}")
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
            'ctl00$MainContent$txtSearchTerms': corp_id,
            'ctl00$MainContent$ddlSearchType': '6' # Exact match search
        }


        # Get "Select Business Entity page"
        result_page = requests.request("POST", url, data=payload)

        # Get view stuff from this page, and buttons daat
        result_parser = fromstring(result_page.text)

        # Get aspx junk for step 2 request
        event_validation_2 = result_parser.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
        view_state_2 = result_parser.xpath('//*[@id="__VIEWSTATE"]/@value')[0]

        try:
            business_status = str(result_parser.xpath('//*[@id="lblBEStatus"]/text()')[0]).upper().strip()
            got_results = True
        except IndexError:
            # This is caused by no results being returned
            print("      [!] Business status not found!")
            got_results = False

        # Prevent rest of script from running
        if got_results:
            # Only want active businesses
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
                # print(entity_details)
                info_dict = entity_details.set_index(0).to_dict()

                business_info = {
                    "name": " ".join(str(business_parser.xpath('//td[@align="left"]/text()')[0]).strip().upper().split()),
                    "business_type": "CORPORATION", # This will get replaced if it is parsed
                    "state_registered": str(info_dict[1]["State Of Inc"]).upper().strip(),
                    "filing_number": str(info_dict[1]["Entity Number"]).strip()
                    }

                print("      [*] Name: " + str(business_parser.xpath('//td[@align="left"]/text()')[0]).strip())



                """Parse physical address"""

                raw_physical_address = str(info_dict[1]['Address']).upper().strip()
                business_info["raw_physical_address"] = raw_physical_address

                try:
                    parsed_address = usaddress.tag(raw_physical_address)
                    parse_success = True

                except usaddress.RepeatedLabelError as e:
                    print(e)
                    parse_success = False


                if parse_success:
                    print(parsed_address)

                    try:
                        street_physical = " ".join(str(raw_physical_address.split(parsed_address[0]["PlaceName"])[0]).strip(",").strip().upper().split())
                        business_info["street_physical"] = street_physical
                    except KeyError:
                        print("      [!] PlaceName was not parsed!")

                    try:
                        business_info["city_physical"] = " ".join(str(parsed_address[0]["PlaceName"]).strip(",").strip().upper().split())

                    except KeyError:
                        print("      [!] City physical key error!")

                    try:
                        business_info["zip5_physical"] = str(parsed_address[0]["ZipCode"]).strip()

                    except KeyError:
                        print("      [!] Zip code key error!")

                    try:
                        business_info["state_physical"] = str(parsed_address[0]["StateName"]).upper().strip()
                    except KeyError:
                        print("      [!] State physical key error!")

                # Registered agent will need a check to see if officer table exists
                if len(df) == 6:
                    agent_details = df[2]
                    agent_dict = agent_details.set_index(0).to_dict()

                    try:
                        business_info["agent_name"] = str(agent_dict[1]["Name"]).upper().strip()
                        business_info["agent_title"] = str(agent_dict[1]["Title"]).upper().strip()

                    except KeyError:
                        print("      [!] Agent name or agent title key error!")

                    raw_registered_address = " ".join(str(agent_dict[1]["Address"]).split()).upper().strip()
                    if raw_registered_address != "NAN":
                        business_info["raw_registered_address"] = raw_registered_address
                        try:
                            parsed_registered_address = usaddress.tag(raw_registered_address)
                            parse_success = True
                        except usaddress.RepeatedLabelError as e:
                            print("      [!] Registered address parsing failed!\n      " + str(e))
                            parse_success = False

                        if parse_success:
                            try:

                                street_registered = str(raw_registered_address).split(parsed_registered_address[0]["PlaceName"])[0]
                                street_registered = street_registered.strip(",").strip().upper()
                                business_info["street_registered"] = street_registered
                            except KeyError:
                                print("      [!] PlaceName parse failed!")

                            try:
                                business_info["city_registered"] = " ".join(str(parsed_registered_address[0]["PlaceName"]).strip(",").strip().upper().split())
                            except KeyError:
                                print("      [!] City Registered parse failure!")

                            try:
                                business_info["zip5_registered"] = str(parsed_address[0]["ZipCode"]).strip()

                            except KeyError:
                                print("      [!] zip5_registered parse failure!")

                    else:
                        print("      [!] Raw registered address is nan, skipping.")



                business_type_string = info_dict[1]["Entity Type"]
                business_info["business_type"] = business_type_parser(str(business_type_string).upper().strip())

                writer.writerow(business_info)


            else:
                print(f"      [!] Business not active: {business_status}")
